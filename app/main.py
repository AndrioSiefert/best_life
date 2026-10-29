from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Loja Online API",
    description="Uma loja online quer enviar mensagens semanais aos clientes, de acordo com o perfil de compra de cada um.",
    version="1.0.0"
)

@app.get("/")
async def health_check():
    return {"status": "OK"}