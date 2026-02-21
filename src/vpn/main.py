from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.vpn.api.routes import peers, users
from src.vpn.db.base import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запущено")
    yield
    print("Приложение остановлено")
    await engine.despose()


app = FastAPI(
    title="VPN Service",
    version="0.1.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    return {"message": "VPN Service API"}


app.include_router(peers.router)
app.include_router(users.router)
app.include_router(peers.admin_router)
app.include_router(users.admin_router)


