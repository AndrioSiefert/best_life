from fastapi import FastAPI
from app.db import init_db
from app.routers import customer

init_db()
app = FastAPI(
    title="Best Life",
    description="Trilhas e envios simulados",
    version="1.0.0",
)
app.include_router(customer.router)


@app.get("/")
def health_check() -> dict:
    return {"status": "OK"}
