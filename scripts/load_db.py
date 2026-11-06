import json
import sqlite3
from pathlib import Path

RAW_DIR = Path("data/raw")
DB_PATH = Path("data/best_life.db")

def latest_file(resource: str) -> Path:
    files = sorted(RAW_DIR.glob(f"*/{resource}_*.json"))
    if not files:
        raise FileNotFoundError(f"Nenhum arquivo de {resource} em {RAW_DIR}. Rode scripts/extract.py primeiro.")
    return files[-1]

def read_json(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sum_carts(carts: list[dict]) -> dict[int, dict]:
    totals = {}
    for cart in carts:
        user_id = cart["userId"]
        if user_id not in totals:
            totals[user_id] = {"value": 0.0, "items": 0}
        totals[user_id]["value"] += cart["total"]
        totals[user_id]["items"] += cart["totalQuantity"]
    return totals


def build_rows(users: list[dict], totals: dict[int, dict]) -> list[tuple]:
    rows = []
    for user in users:
        t = totals.get(user["id"], {"value": 0.0, "items": 0})
        rows.append((
            user["id"],
            f"{user['firstName']} {user['lastName']}",
            user["age"],
            user["gender"],
            user["address"]["state"],
            user["phone"],
            round(t["value"], 2),
            t["items"],
        ))
    return rows


def save_customers(rows: list[tuple]) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                age INTEGER,
                gender TEXT,
                state TEXT,
                phone TEXT,
                total_value REAL,
                total_items INTEGER
            )
        """)
        conn.executemany(
            "INSERT OR REPLACE INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            rows,
        )


def main() -> None:
    users = read_json(latest_file("users"))
    carts = read_json(latest_file("carts"))
    rows = build_rows(users, sum_carts(carts))
    save_customers(rows)
    print(f"{len(rows)} clientes gravados em {DB_PATH}")


if __name__ == "__main__":
    main()