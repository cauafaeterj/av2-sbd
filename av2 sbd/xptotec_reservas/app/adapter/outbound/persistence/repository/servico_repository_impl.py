from __future__ import annotations

from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.adapter.outbound.persistence.entity.servico_entity import ServicoEntity
from app.adapter.outbound.persistence.mapper.reserva_persistence_mapper import (
    ReservaPersistenceMapper,
)
from app.domain.model.servico import Servico
from app.domain.port.outbound.servico_repository import ServicoRepository


class ServicoRepositoryImpl(ServicoRepository):

    def __init__(self, session: Session, mapper: ReservaPersistenceMapper):
        self.session = session
        self.mapper = mapper

    def buscar_por_ids(self, ids: List[UUID]) -> List[Servico]:
        ids_str = [str(i) for i in ids]
        stmt = select(ServicoEntity).where(ServicoEntity.id.in_(ids_str))
        entities = self.session.execute(stmt).scalars().all()
        return [self.mapper.servico_to_domain(e) for e in entities]
