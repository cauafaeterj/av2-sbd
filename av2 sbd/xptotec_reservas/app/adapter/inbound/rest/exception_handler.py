from __future__ import annotations

from datetime import datetime

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.domain.exception.horario_indisponivel_exception import (
    HorarioIndisponivelException,
)
from app.domain.exception.reserva_exception import ReservaException


def _build_response(status_code: int, mensagem: str) -> JSONResponse:
    reason_phrases = {
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_409_CONFLICT: "Conflict",
    }
    body = {
        "timestamp": datetime.now().isoformat(),
        "status": status_code,
        "erro": reason_phrases.get(status_code, "Error"),
        "mensagem": mensagem,
    }
    return JSONResponse(status_code=status_code, content=body)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(HorarioIndisponivelException)
    async def handle_horario_indisponivel(
        request: Request, exc: HorarioIndisponivelException
    ) -> JSONResponse:
        return _build_response(status.HTTP_409_CONFLICT, exc.mensagem)

    @app.exception_handler(ReservaException)
    async def handle_reserva_exception(
        request: Request, exc: ReservaException
    ) -> JSONResponse:
        return _build_response(status.HTTP_400_BAD_REQUEST, exc.mensagem)

    @app.exception_handler(ValueError)
    async def handle_value_error(request: Request, exc: ValueError) -> JSONResponse:
        return _build_response(status.HTTP_400_BAD_REQUEST, str(exc))

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        erros = "; ".join(
            f"{'.'.join(str(loc) for loc in e['loc'] if loc != 'body')}: {e['msg']}"
            for e in exc.errors()
        )
        return _build_response(status.HTTP_400_BAD_REQUEST, erros)
