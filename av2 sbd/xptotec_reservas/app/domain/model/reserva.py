from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID

from app.domain.exception.horario_indisponivel_exception import (
    HorarioIndisponivelException,
)
from app.domain.exception.reserva_exception import ReservaException
from app.domain.model.cliente import Cliente
from app.domain.model.dinheiro import Dinheiro
from app.domain.model.profissional import Profissional
from app.domain.model.servico import Servico
from app.domain.model.slot_horario import SlotHorario
from app.domain.model.status_reserva import StatusReserva


class Reserva:

    def __init__(
        self,
        id: UUID,
        cliente: Cliente,
        profissional: Optional[Profissional],
        servicos: List[Servico],
        horario_inicio: datetime,
        horario_fim: datetime,
        valor_total: Dinheiro,
        status: StatusReserva,
    ):
        self._id = id
        self.cliente = cliente
        self.profissional = profissional
        self._servicos = list(servicos)
        self.horario_inicio = horario_inicio
        self.horario_fim = horario_fim
        self.valor_total = valor_total
        self.status = status

    @classmethod
    def nova(
        cls,
        id: UUID,
        cliente: Cliente,
        profissional: Optional[Profissional],
        servicos: List[Servico],
        horario_inicio: datetime,
    ) -> "Reserva":
        cls._validar_criacao(id, cliente, servicos, horario_inicio)
        valor_total = cls._calcular_valor_total(servicos)
        horario_fim = cls._calcular_horario_fim(servicos, horario_inicio)
        return cls(
            id,
            cliente,
            profissional,
            servicos,
            horario_inicio,
            horario_fim,
            valor_total,
            StatusReserva.PENDENTE,
        )

    def confirmar(self) -> None:
        if self.status != StatusReserva.PENDENTE:
            raise ReservaException(
                f"Apenas reservas pendentes podem ser confirmadas. Status atual: {self.status.value}"
            )
        self.status = StatusReserva.CONFIRMADA

    def registrar_no_show(self) -> Dinheiro:
        if self.status != StatusReserva.CONFIRMADA:
            raise ReservaException(
                "No-show só pode ser registrado para reservas confirmadas. "
                f"Status atual: {self.status.value}"
            )
        credito_gerado = self.valor_total.percentual(50)
        self.cliente.adicionar_credito(credito_gerado)
        self.status = StatusReserva.NO_SHOW
        return credito_gerado

    def concluir(self) -> None:
        if self.status != StatusReserva.CONFIRMADA:
            raise ReservaException("Apenas reservas confirmadas podem ser concluídas.")
        self.status = StatusReserva.CONCLUIDA

    def cancelar(self) -> None:
        if self.status in (StatusReserva.CONCLUIDA, StatusReserva.NO_SHOW):
            raise ReservaException(
                "Não é possível cancelar uma reserva já concluída ou com no-show."
            )
        self.status = StatusReserva.CANCELADA

    def validar_disponibilidade(self, agenda_ocupada: List[SlotHorario]) -> None:
        slot_reserva = SlotHorario(self.horario_inicio, self.horario_fim)
        conflito = any(slot_reserva.conflita_com(s) for s in agenda_ocupada)
        if conflito:
            raise HorarioIndisponivelException(
                f"O horário {slot_reserva} conflita com outra reserva existente na agenda."
            )

    def esta_dentro_tolerancia_atraso(self, horario_chegada: datetime) -> bool:
        limite_tolerancia = self.horario_inicio + timedelta(minutes=15)
        return not horario_chegada > limite_tolerancia

    @staticmethod
    def _calcular_valor_total(servicos: List[Servico]) -> Dinheiro:
        total = Dinheiro.ZERO
        for servico in servicos:
            total = total.somar(servico.preco)
        return total

    @staticmethod
    def _calcular_horario_fim(servicos: List[Servico], horario_inicio: datetime) -> datetime:
        duracao_total = timedelta()
        for servico in servicos:
            duracao_total += servico.duracao
        return horario_inicio + duracao_total

    @staticmethod
    def _validar_criacao(
        id: UUID,
        cliente: Cliente,
        servicos: List[Servico],
        horario_inicio: datetime,
    ) -> None:
        if id is None:
            raise ReservaException("ID da reserva é obrigatório.")
        if cliente is None:
            raise ReservaException("Cliente é obrigatório para criar uma reserva.")
        if not servicos:
            raise ReservaException("Pelo menos um serviço deve ser selecionado.")
        if horario_inicio is None:
            raise ReservaException("Horário de início é obrigatório.")
        if horario_inicio < datetime.now():
            raise ReservaException("Não é possível criar reserva para um horário no passado.")

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def servicos(self) -> List[Servico]:
        return list(self._servicos)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Reserva):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"Reserva{{id={self._id}, status={self.status.value}, valor={self.valor_total}}}"
