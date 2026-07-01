from __future__ import annotations

from datetime import timedelta
from uuid import UUID

from app.adapter.outbound.persistence.entity.cliente_entity import ClienteEntity
from app.adapter.outbound.persistence.entity.profissional_entity import (
    ProfissionalEntity,
)
from app.adapter.outbound.persistence.entity.reserva_entity import ReservaEntity
from app.adapter.outbound.persistence.entity.servico_entity import ServicoEntity
from app.domain.model.cliente import Cliente
from app.domain.model.dinheiro import Dinheiro
from app.domain.model.especialidade import Especialidade
from app.domain.model.profissional import Profissional
from app.domain.model.reserva import Reserva
from app.domain.model.servico import Servico
from app.domain.model.status_reserva import StatusReserva


class ReservaPersistenceMapper:

    def cliente_to_domain(self, entity: ClienteEntity) -> Cliente:
        return Cliente(
            UUID(entity.id),
            entity.nome,
            entity.email,
            entity.telefone,
            Dinheiro.of(entity.credito_disponivel),
        )

    def cliente_to_entity(self, domain: Cliente) -> ClienteEntity:
        return ClienteEntity(
            id=str(domain.id),
            nome=domain.nome,
            email=domain.email,
            telefone=domain.telefone,
            credito_disponivel=domain.credito_disponivel.valor,
        )

    def profissional_to_domain(self, entity: ProfissionalEntity) -> Profissional:
        especialidades = {
            Especialidade(nome.strip())
            for nome in entity.especialidades.split(",")
            if nome.strip()
        }
        return Profissional(UUID(entity.id), entity.nome, especialidades)

    def profissional_to_entity(self, domain: Profissional) -> ProfissionalEntity:
        csv = ",".join(e.value for e in domain.especialidades)
        return ProfissionalEntity(id=str(domain.id), nome=domain.nome, especialidades=csv)

    def servico_to_domain(self, entity: ServicoEntity) -> Servico:
        return Servico(
            UUID(entity.id),
            entity.nome,
            Especialidade(entity.especialidade),
            timedelta(minutes=entity.duracao_minutos),
            Dinheiro.of(entity.preco),
        )

    def servico_to_entity(self, domain: Servico) -> ServicoEntity:
        return ServicoEntity(
            id=str(domain.id),
            nome=domain.nome,
            especialidade=domain.especialidade.value,
            duracao_minutos=int(domain.duracao.total_seconds() // 60),
            preco=domain.preco.valor,
        )

    def reserva_to_domain(self, entity: ReservaEntity) -> Reserva:
        cliente = self.cliente_to_domain(entity.cliente)
        profissional = (
            self.profissional_to_domain(entity.profissional)
            if entity.profissional is not None
            else None
        )
        servicos = [self.servico_to_domain(s) for s in entity.servicos]
        return Reserva(
            UUID(entity.id),
            cliente,
            profissional,
            servicos,
            entity.horario_inicio,
            entity.horario_fim,
            Dinheiro.of(entity.valor_total),
            StatusReserva(entity.status),
        )

    def reserva_to_entity(self, domain: Reserva) -> ReservaEntity:
        entity = ReservaEntity()
        entity.id = str(domain.id)
        entity.cliente_id = str(domain.cliente.id)
        entity.profissional_id = (
            str(domain.profissional.id) if domain.profissional is not None else None
        )
        entity.horario_inicio = domain.horario_inicio
        entity.horario_fim = domain.horario_fim
        entity.valor_total = domain.valor_total.valor
        entity.status = domain.status.value
        return entity
