import httpx
import json
from pathlib import Path
from datetime import datetime


BASE_URL = "https://dummyjson.com"
PAGE_SIZE = 100
RAW_DIR = Path("data/raw")

def fetch_all(resource: str) -> list[dict]:
    items = []
    skip = 0
    while True:
        response = httpx.get(
            f"{BASE_URL}/{resource}", 
            params={"limit": PAGE_SIZE, "skip": skip},
        )
        response.raise_for_status() #200=ok, 404=não achou, 500=erro
        data = response.json()
        items.extend(data[resource])
        skip += PAGE_SIZE
        if skip >= data["total"]: #208
            break
    return items


def save_raw(resource: str, items: list[dict], moment: datetime) -> Path:
    folder = RAW_DIR / moment.strftime("%Y-%m-%d")
    folder.mkdir(parents=True, exist_ok=True)
    filename = f"{resource}_{moment.strftime("%Y-%m-%d_%H-%M-%S")}.json"
    path = folder / filename
    with open(path, "x", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    return path

def main() -> None:
    moment = datetime.now()
    try:
        users = fetch_all("users")
        carts = fetch_all("carts")
    except Exception as error:
        print(f"Erro ao buscar dados da API: {error}")
        return
    users_path = save_raw("users", users, moment)
    carts_path = save_raw("carts", carts, moment)
    print(f"Dados salvos com sucesso em {users_path} e {carts_path}")

if __name__ == "__main__":
    main()