from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.adapter.inbound.rest.exception_handler import register_exception_handlers
from app.adapter.inbound.rest.reserva_controller import router as reserva_router
from app.config.data_initializer import init_database
from app.config.database import Base, SessionLocal, engine

from app.adapter.outbound.persistence.entity import (
    cliente_entity,
    profissional_entity,
    reserva_entity,
    servico_entity,
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("xptotec.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        init_database(db)
    finally:
        db.close()

    log.info("xptotec-reservas iniciado.")
    yield
    log.info("xptotec-reservas finalizado.")


app = FastAPI(
    title="xptotec-reservas",
    description="Sistema de reservas (agendamentos) — convertido de Java/Spring Boot para Python/FastAPI + SQLAlchemy.",
    version="1.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)
app.include_router(reserva_router)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "aplicacao": "xptotec-reservas"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
