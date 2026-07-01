from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapter.outbound.persistence.entity.cliente_entity import ClienteEntity
from app.adapter.outbound.persistence.entity.profissional_entity import (
    ProfissionalEntity,
)
from app.adapter.outbound.persistence.entity.servico_entity import ServicoEntity
from app.config.database import Base

reserva_servicos = Table(
    "reserva_servicos",
    Base.metadata,
    Column("reserva_id", String(36), ForeignKey("reservas.id"), primary_key=True),
    Column("servico_id", String(36), ForeignKey("servicos.id"), primary_key=True),
)


class ReservaEntity(Base):

    __tablename__ = "reservas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    cliente_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("clientes.id"), nullable=False
    )
    cliente: Mapped[ClienteEntity] = relationship(ClienteEntity, lazy="joined")

    profissional_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("profissionais.id"), nullable=True
    )
    profissional: Mapped[ProfissionalEntity | None] = relationship(
        ProfissionalEntity, lazy="joined"
    )

    servicos: Mapped[list[ServicoEntity]] = relationship(
        ServicoEntity, secondary=reserva_servicos, lazy="joined"
    )

    horario_inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    horario_fim: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    valor_total: Mapped[Numeric] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
