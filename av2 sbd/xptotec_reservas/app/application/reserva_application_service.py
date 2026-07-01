from __future__ import annotations

from uuid import UUID

from app.application.dto.criar_reserva_command import CriarReservaCommand
from app.domain.exception.reserva_exception import ReservaException
from app.domain.model.reserva import Reserva
from app.domain.port.inbound.criar_reserva_use_case import CriarReservaUseCase
from app.domain.port.inbound.registrar_no_show_use_case import (
    NoShowResult,
    RegistrarNoShowUseCase,
)
from app.domain.port.outbound.cliente_repository import ClienteRepository
from app.domain.port.outbound.profissional_repository import ProfissionalRepository
from app.domain.port.outbound.reserva_repository import ReservaRepository
from app.domain.port.outbound.servico_repository import ServicoRepository
from uuid import uuid4


class ReservaApplicationService(CriarReservaUseCase, RegistrarNoShowUseCase):

    def __init__(
        self,
        reserva_repository: ReservaRepository,
        cliente_repository: ClienteRepository,
        profissional_repository: ProfissionalRepository,
        servico_repository: ServicoRepository,
    ):
        self.reserva_repository = reserva_repository
        self.cliente_repository = cliente_repository
        self.profissional_repository = profissional_repository
        self.servico_repository = servico_repository

    def criar_reserva(self, command: CriarReservaCommand) -> Reserva:
        cliente = self.cliente_repository.buscar_por_id(command.cliente_id)
        if cliente is None:
            raise ReservaException(f"Cliente não encontrado: {command.cliente_id}")

        profissional = None
        if command.profissional_id is not None:
            profissional = self.profissional_repository.buscar_por_id(command.profissional_id)
            if profissional is None:
                raise ReservaException(
                    f"Profissional não encontrado: {command.profissional_id}"
                )

        servicos = self.servico_repository.buscar_por_ids(command.servico_ids)
        if len(servicos) != len(command.servico_ids):
            raise ReservaException("Um ou mais serviços não foram encontrados.")

        reserva = Reserva.nova(
            uuid4(),
            cliente,
            profissional,
            servicos,
            command.horario_inicio,
        )

        if profissional is not None:
            agenda_ocupada = self.reserva_repository.buscar_slots_por_profissional_e_periodo(
                profissional.id,
                command.horario_inicio,
                reserva.horario_fim,
            )
            reserva.validar_disponibilidade(agenda_ocupada)

        reserva.confirmar()
        return self.reserva_repository.salvar(reserva)

    def registrar_no_show(self, reserva_id: UUID) -> NoShowResult:
        reserva = self.reserva_repository.buscar_por_id(reserva_id)
        if reserva is None:
            raise ReservaException(f"Reserva não encontrada: {reserva_id}")

        credito_gerado = reserva.registrar_no_show()
        valor_retido = reserva.valor_total.percentual(50)
        self.reserva_repository.salvar(reserva)
        self.cliente_repository.salvar(reserva.cliente)

        return NoShowResult(
            reserva_id=reserva.id,
            status=reserva.status.value,
            valor_retido=valor_retido.valor,
            credito_gerado=credito_gerado.valor,
            credito_total_cliente=reserva.cliente.credito_disponivel.valor,
            mensagem=(
                f"No-show registrado. 50% retido ({valor_retido}) "
                f"e 50% convertido em crédito ({credito_gerado})."
            ),
        )

    def buscar_por_id(self, id: UUID) -> Reserva:
        reserva = self.reserva_repository.buscar_por_id(id)
        if reserva is None:
            raise ReservaException(f"Reserva não encontrada: {id}")
        return reserva
