from __future__ import annotations

from app.adapter.inbound.rest.dto.criar_reserva_request import CriarReservaRequest
from app.adapter.inbound.rest.dto.no_show_response import NoShowResponse
from app.adapter.inbound.rest.dto.reserva_response import ReservaResponse
from app.application.dto.criar_reserva_command import CriarReservaCommand
from app.domain.model.reserva import Reserva
from app.domain.port.inbound.registrar_no_show_use_case import NoShowResult


class ReservaRestMapper:

    def to_command(self, request: CriarReservaRequest) -> CriarReservaCommand:
        return CriarReservaCommand(
            cliente_id=request.cliente_id,
            profissional_id=request.profissional_id,
            servico_ids=request.servico_ids,
            horario_inicio=request.horario_inicio,
        )

    def to_response(self, reserva: Reserva) -> ReservaResponse:
        return ReservaResponse(
            id=reserva.id,
            clienteNome=reserva.cliente.nome,
            profissionalNome=reserva.profissional.nome if reserva.profissional else None,
            servicos=[s.nome for s in reserva.servicos],
            horarioInicio=reserva.horario_inicio,
            horarioFim=reserva.horario_fim,
            valorTotal=reserva.valor_total.valor,
            status=reserva.status.value,
        )

    def to_no_show_response(self, result: NoShowResult) -> NoShowResponse:
        return NoShowResponse(
            reservaId=result.reserva_id,
            status=result.status,
            valorRetido=result.valor_retido,
            creditoGerado=result.credito_gerado,
            creditoTotalCliente=result.credito_total_cliente,
            mensagem=result.mensagem,
        )
