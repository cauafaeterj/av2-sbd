from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.adapter.outbound.persistence.entity.reserva_entity import ReservaEntity
from app.adapter.outbound.persistence.entity.servico_entity import ServicoEntity
from app.adapter.outbound.persistence.mapper.reserva_persistence_mapper import (
    ReservaPersistenceMapper,
)
from app.domain.model.reserva import Reserva
from app.domain.model.slot_horario import SlotHorario
from app.domain.model.status_reserva import StatusReserva
from app.domain.port.outbound.reserva_repository import ReservaRepository


class ReservaRepositoryImpl(ReservaRepository):

    def __init__(self, session: Session, mapper: ReservaPersistenceMapper):
        self.session = session
        self.mapper = mapper

    def salvar(self, reserva: Reserva) -> Reserva:
        entity = self.session.get(ReservaEntity, str(reserva.id))
        if entity is None:
            entity = self.mapper.reserva_to_entity(reserva)
            self.session.add(entity)
        else:
            entity.cliente_id = str(reserva.cliente.id)
            entity.profissional_id = (
                str(reserva.profissional.id) if reserva.profissional else None
            )
            entity.horario_inicio = reserva.horario_inicio
            entity.horario_fim = reserva.horario_fim
            entity.valor_total = reserva.valor_total.valor
            entity.status = reserva.status.value

        servico_ids = [str(s.id) for s in reserva.servicos]
        stmt = select(ServicoEntity).where(ServicoEntity.id.in_(servico_ids))
        entity.servicos = list(self.session.execute(stmt).scalars().all())

        self.session.commit()
        self.session.refresh(entity)
        return self.mapper.reserva_to_domain(entity)

    def buscar_por_id(self, id: UUID) -> Optional[Reserva]:
        entity = self.session.get(ReservaEntity, str(id))
        return self.mapper.reserva_to_domain(entity) if entity else None

    def buscar_slots_por_profissional_e_periodo(
        self, profissional_id: UUID, inicio: datetime, fim: datetime
    ) -> List[SlotHorario]:
        status_excluidos = (StatusReserva.CANCELADA.value, StatusReserva.NO_SHOW.value)
        stmt = select(ReservaEntity).where(
            ReservaEntity.profissional_id == str(profissional_id),
            ~ReservaEntity.status.in_(status_excluidos),
            ReservaEntity.horario_inicio < fim,
            ReservaEntity.horario_fim > inicio,
        )
        conflitantes = self.session.execute(stmt).scalars().all()
        return [SlotHorario(r.horario_inicio, r.horario_fim) for r in conflitantes]
