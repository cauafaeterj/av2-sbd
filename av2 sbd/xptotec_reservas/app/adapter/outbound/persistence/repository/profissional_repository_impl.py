from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.adapter.outbound.persistence.entity.profissional_entity import (
    ProfissionalEntity,
)
from app.adapter.outbound.persistence.mapper.reserva_persistence_mapper import (
    ReservaPersistenceMapper,
)
from app.domain.model.profissional import Profissional
from app.domain.port.outbound.profissional_repository import ProfissionalRepository


class ProfissionalRepositoryImpl(ProfissionalRepository):

    def __init__(self, session: Session, mapper: ReservaPersistenceMapper):
        self.session = session
        self.mapper = mapper

    def buscar_por_id(self, id: UUID) -> Optional[Profissional]:
        entity = self.session.get(ProfissionalEntity, str(id))
        return self.mapper.profissional_to_domain(entity) if entity else None
