from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.adapter.outbound.persistence.entity.cliente_entity import ClienteEntity
from app.adapter.outbound.persistence.mapper.reserva_persistence_mapper import (
    ReservaPersistenceMapper,
)
from app.domain.model.cliente import Cliente
from app.domain.port.outbound.cliente_repository import ClienteRepository


class ClienteRepositoryImpl(ClienteRepository):

    def __init__(self, session: Session, mapper: ReservaPersistenceMapper):
        self.session = session
        self.mapper = mapper

    def buscar_por_id(self, id: UUID) -> Optional[Cliente]:
        entity = self.session.get(ClienteEntity, str(id))
        return self.mapper.cliente_to_domain(entity) if entity else None

    def salvar(self, cliente: Cliente) -> Cliente:
        entity = self.session.get(ClienteEntity, str(cliente.id))
        if entity is None:
            entity = self.mapper.cliente_to_entity(cliente)
            self.session.add(entity)
        else:
            entity.nome = cliente.nome
            entity.email = cliente.email
            entity.telefone = cliente.telefone
            entity.credito_disponivel = cliente.credito_disponivel.valor
        self.session.commit()
        self.session.refresh(entity)
        return self.mapper.cliente_to_domain(entity)
