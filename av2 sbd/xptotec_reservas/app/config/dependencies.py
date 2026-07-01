from __future__ import annotations

from sqlalchemy.orm import Session

from app.adapter.inbound.rest.rest_mapper import ReservaRestMapper
from app.adapter.outbound.persistence.mapper.reserva_persistence_mapper import (
    ReservaPersistenceMapper,
)
from app.adapter.outbound.persistence.repository.cliente_repository_impl import (
    ClienteRepositoryImpl,
)
from app.adapter.outbound.persistence.repository.profissional_repository_impl import (
    ProfissionalRepositoryImpl,
)
from app.adapter.outbound.persistence.repository.reserva_repository_impl import (
    ReservaRepositoryImpl,
)
from app.adapter.outbound.persistence.repository.servico_repository_impl import (
    ServicoRepositoryImpl,
)
from app.application.reserva_application_service import ReservaApplicationService
from app.config.database import get_db
from fastapi import Depends


_persistence_mapper = ReservaPersistenceMapper()
_rest_mapper = ReservaRestMapper()


def get_rest_mapper() -> ReservaRestMapper:
    return _rest_mapper


def get_reserva_application_service(
    db: Session = Depends(get_db),
) -> ReservaApplicationService:
    reserva_repository = ReservaRepositoryImpl(db, _persistence_mapper)
    cliente_repository = ClienteRepositoryImpl(db, _persistence_mapper)
    profissional_repository = ProfissionalRepositoryImpl(db, _persistence_mapper)
    servico_repository = ServicoRepositoryImpl(db, _persistence_mapper)
    return ReservaApplicationService(
        reserva_repository=reserva_repository,
        cliente_repository=cliente_repository,
        profissional_repository=profissional_repository,
        servico_repository=servico_repository,
    )
