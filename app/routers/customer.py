from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.db import get_connection
from app.services.classification import classify

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")

# Trilhas em ordem de prioridade (usadas no filtro da tela)
TRACKS = ["Alto valor", "Compra em quantidade", "Incentivo", "Público jovem", "Geral"]


@router.get("/customers")
def list_customers(request: Request, track: str = ""):
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM customers ORDER BY id").fetchall()

    customers = []
    for row in rows:
        tracks = classify(row["total_value"], row["total_items"], row["age"])
        names = [name for name, reason in tracks]
        if track and track not in names:
            continue
        customers.append({"data": row, "tracks": names})

    return templates.TemplateResponse(
        request,
        "customers.html",
        {"customers": customers, "all_tracks": TRACKS, "selected": track},
    )
