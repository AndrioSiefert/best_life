import json
from datetime import date
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.db import get_connection
from app.services.classification import classify
from app.services.schedule import TRACKS, WEEKDAYS, make_schedule
from app.services.whatsapp import build_request

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


def schedule_data() -> tuple[list[dict], int]:
    with get_connection() as conn:
        setting = conn.execute(
            "SELECT value FROM settings WHERE name = 'weekday'"
        ).fetchone()
        weekday = 0
        if setting:
            weekday = int(setting["value"])

        customers = conn.execute("""
            SELECT customers.*, decisions.tracks, decisions.confirmed_at
            FROM customers
            JOIN decisions ON customers.id = decisions.customer_id
        """).fetchall()

    events = make_schedule(customers, weekday)
    return events, weekday


@router.get("/customers")
def list_customers(request: Request, track: str = ""):
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM customers ORDER BY id").fetchall()

    customers = []
    for row in rows:
        suggestions = classify(row["total_value"], row["total_items"], row["age"])
        names = []
        for name, reason in suggestions:
            names.append(name)

        if track and track not in names:
            continue
        customers.append({"data": row, "tracks": names})

    return templates.TemplateResponse(
        request,
        "customers.html",
        {"customers": customers, "all_tracks": TRACKS, "selected": track},
    )


@router.get("/customers/{customer_id}")
def customer_detail(request: Request, customer_id: int):
    with get_connection() as conn:
        customer = conn.execute(
            "SELECT * FROM customers WHERE id = ?", (customer_id,)
        ).fetchone()
        decision = conn.execute(
            "SELECT * FROM decisions WHERE customer_id = ?", (customer_id,)
        ).fetchone()

    if customer is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    suggestions = classify(customer["total_value"], customer["total_items"], customer["age"])
    selected = []
    if decision:
        selected = decision["tracks"].split("|")
    else:
        for name, reason in suggestions:
            selected.append(name)

    return templates.TemplateResponse(
        request,
        "customer.html",
        {
            "customer": customer,
            "suggestions": suggestions,
            "tracks": TRACKS,
            "selected": selected,
            "decision": decision,
        },
    )


@router.post("/customers/{customer_id}")
async def save_decision(request: Request, customer_id: int) -> RedirectResponse:
    form = await request.form()
    selected = form.getlist("tracks")

    if not selected:
        raise HTTPException(status_code=400, detail="Selecione ao menos uma trilha.")
    for track in selected:
        if track not in TRACKS:
            raise HTTPException(status_code=400, detail="Trilha inválida.")
    if "Geral" in selected and len(selected) > 1:
        raise HTTPException(status_code=400, detail="Geral deve ser escolhida sozinha.")

    ordered = []
    for track in TRACKS:
        if track in selected:
            ordered.append(track)
    tracks_text = "|".join(ordered)

    with get_connection() as conn:
        customer = conn.execute(
            "SELECT id FROM customers WHERE id = ?", (customer_id,)
        ).fetchone()
        if not customer:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        previous = conn.execute(
            "SELECT tracks FROM decisions WHERE customer_id = ?", (customer_id,)
        ).fetchone()
        if not previous or previous["tracks"] != tracks_text:
            conn.execute(
                "INSERT OR REPLACE INTO decisions VALUES (?, ?, ?)",
                (customer_id, tracks_text, date.today().isoformat()),
            )

    return RedirectResponse(f"/customers/{customer_id}", status_code=303)


@router.get("/schedule")
def schedule(request: Request):
    events, weekday = schedule_data()
    upcoming = []
    today = date.today().isoformat()
    for event in events:
        if event["date"] >= today:
            upcoming.append(event)

    return templates.TemplateResponse(
        request,
        "schedule.html",
        {"events": upcoming, "weekday": weekday, "weekdays": WEEKDAYS},
    )


@router.post("/schedule")
async def save_weekday(request: Request) -> RedirectResponse:
    form = await request.form()
    try:
        weekday = int(form.get("weekday", ""))
    except ValueError:
        raise HTTPException(status_code=400, detail="Dia da semana inválido")

    if weekday not in range(7):
        raise HTTPException(status_code=400, detail="Dia da semana inválido")

    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO settings VALUES ('weekday', ?)",
            (str(weekday),),
        )
    return RedirectResponse("/schedule", status_code=303)


@router.post("/simulate")
def simulate() -> RedirectResponse:
    events, weekday = schedule_data()
    today = date.today().isoformat()

    with get_connection() as conn:
        for event in events:
            if event["date"] != today:
                continue
            payload = build_request(event["phone"], event["message"])
            request_json = json.dumps(payload, ensure_ascii=False, indent=2)
            conn.execute(
                """
                INSERT OR IGNORE INTO history
                    (customer_id, customer_name, track, message_index,
                     scheduled_date, message, request)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event["customer_id"],
                    event["name"],
                    event["track"],
                    event["index"],
                    today,
                    event["message"],
                    request_json,
                ),
            )
    return RedirectResponse("/history", status_code=303)


@router.get("/history")
def history(request: Request):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM history ORDER BY scheduled_date DESC, id DESC"
        ).fetchall()

    return templates.TemplateResponse(request, "history.html", {"history": rows})
