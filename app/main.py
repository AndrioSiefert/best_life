from fastapi import FastAPI
from app.routers import customer

app = FastAPI(
    title="Loja Online API",
    description="Uma loja online quer enviar mensagens semanais aos clientes, de acordo com o perfil de compra de cada um.",
    version="1.0.0"
)

app.include_router(customer.router)


@app.get("/")
async def health_check():
    return {"status": "OK"}