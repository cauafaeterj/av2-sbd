from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.adapter.inbound.rest.dto.criar_reserva_request import CriarReservaRequest
from app.adapter.inbound.rest.dto.no_show_response import NoShowResponse
from app.adapter.inbound.rest.dto.reserva_response import ReservaResponse
from app.adapter.inbound.rest.rest_mapper import ReservaRestMapper
from app.application.reserva_application_service import ReservaApplicationService
from app.config.dependencies import get_reserva_application_service, get_rest_mapper

router = APIRouter(prefix="/api/reservas", tags=["reservas"])


@router.post("", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
def criar_reserva(
    request: CriarReservaRequest,
    service: ReservaApplicationService = Depends(get_reserva_application_service),
    mapper: ReservaRestMapper = Depends(get_rest_mapper),
) -> ReservaResponse:
    command = mapper.to_command(request)
    reserva = service.criar_reserva(command)
    return mapper.to_response(reserva)


@router.get("/{id}", response_model=ReservaResponse)
def buscar_reserva(
    id: UUID,
    service: ReservaApplicationService = Depends(get_reserva_application_service),
    mapper: ReservaRestMapper = Depends(get_rest_mapper),
) -> ReservaResponse:
    reserva = service.buscar_por_id(id)
    return mapper.to_response(reserva)


@router.post("/{id}/no-show", response_model=NoShowResponse)
def registrar_no_show(
    id: UUID,
    service: ReservaApplicationService = Depends(get_reserva_application_service),
    mapper: ReservaRestMapper = Depends(get_rest_mapper),
) -> NoShowResponse:
    result = service.registrar_no_show(id)
    return mapper.to_no_show_response(result)
