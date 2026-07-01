from __future__ import annotations

import logging
from decimal import Decimal

from sqlalchemy.orm import Session

from app.adapter.outbound.persistence.entity.cliente_entity import ClienteEntity
from app.adapter.outbound.persistence.entity.profissional_entity import (
    ProfissionalEntity,
)
from app.adapter.outbound.persistence.entity.servico_entity import ServicoEntity

log = logging.getLogger("xptotec.data_initializer")


def init_database(db: Session) -> None:

    log.info("Iniciando carga de dados iniciais via ORM...")

    clientes = [
        ClienteEntity(
            id="550e8400-e29b-41d4-a716-446655440001",
            nome="Maria Silva",
            email="maria.silva@email.com",
            telefone="11999990001",
            credito_disponivel=Decimal("0.00"),
        ),
        ClienteEntity(
            id="550e8400-e29b-41d4-a716-446655440002",
            nome="João Santos",
            email="joao.santos@email.com",
            telefone="11999990002",
            credito_disponivel=Decimal("50.00"),
        ),
        ClienteEntity(
            id="550e8400-e29b-41d4-a716-446655440003",
            nome="Ana Oliveira",
            email="ana.oliveira@email.com",
            telefone="11999990003",
            credito_disponivel=Decimal("0.00"),
        ),
    ]
    db.add_all(clientes)
    db.commit()
    log.info("  → %d clientes inseridos.", db.query(ClienteEntity).count())

    profissionais = [
        ProfissionalEntity(
            id="550e8400-e29b-41d4-a716-446655440010",
            nome="Ana Costa",
            especialidades="CABELO,ESTETICA",
        ),
        ProfissionalEntity(
            id="550e8400-e29b-41d4-a716-446655440011",
            nome="Carlos Lima",
            especialidades="UNHA,DEPILACAO",
        ),
        ProfissionalEntity(
            id="550e8400-e29b-41d4-a716-446655440012",
            nome="Beatriz Mendes",
            especialidades="MAQUIAGEM,MASSAGEM",
        ),
    ]
    db.add_all(profissionais)
    db.commit()
    log.info("  → %d profissionais inseridos.", db.query(ProfissionalEntity).count())

    servicos = [
        ServicoEntity(
            id="550e8400-e29b-41d4-a716-446655440100",
            nome="Corte Feminino",
            especialidade="CABELO",
            duracao_minutos=60,
            preco=Decimal("120.00"),
        ),
        ServicoEntity(
            id="550e8400-e29b-41d4-a716-446655440101",
            nome="Escova Progressiva",
            especialidade="CABELO",
            duracao_minutos=60,
            preco=Decimal("130.00"),
        ),
        ServicoEntity(
            id="550e8400-e29b-41d4-a716-446655440102",
            nome="Manicure Gel",
            especialidade="UNHA",
            duracao_minutos=45,
            preco=Decimal("80.00"),
        ),
        ServicoEntity(
            id="550e8400-e29b-41d4-a716-446655440103",
            nome="Pedicure Completa",
            especialidade="UNHA",
            duracao_minutos=50,
            preco=Decimal("90.00"),
        ),
        ServicoEntity(
            id="550e8400-e29b-41d4-a716-446655440104",
            nome="Limpeza de Pele",
            especialidade="ESTETICA",
            duracao_minutos=90,
            preco=Decimal("200.00"),
        ),
        ServicoEntity(
            id="550e8400-e29b-41d4-a716-446655440105",
            nome="Maquiagem Noiva",
            especialidade="MAQUIAGEM",
            duracao_minutos=120,
            preco=Decimal("350.00"),
        ),
        ServicoEntity(
            id="550e8400-e29b-41d4-a716-446655440106",
            nome="Depilação Completa",
            especialidade="DEPILACAO",
            duracao_minutos=60,
            preco=Decimal("150.00"),
        ),
        ServicoEntity(
            id="550e8400-e29b-41d4-a716-446655440107",
            nome="Massagem Relaxante",
            especialidade="MASSAGEM",
            duracao_minutos=60,
            preco=Decimal("180.00"),
        ),
    ]
    db.add_all(servicos)
    db.commit()
    log.info("  → %d serviços inseridos.", db.query(ServicoEntity).count())

    log.info("Carga de dados iniciais concluída com sucesso!")
