from __future__ import annotations

from datetime import timedelta
from uuid import UUID

from app.domain.model.dinheiro import Dinheiro
from app.domain.model.especialidade import Especialidade


class Servico:

    def __init__(
        self,
        id: UUID,
        nome: str,
        especialidade: Especialidade,
        duracao: timedelta,
        preco: Dinheiro,
    ):
        if id is None:
            raise ValueError("ID do serviço é obrigatório.")
        if not nome or not nome.strip():
            raise ValueError("Nome do serviço é obrigatório.")
        if especialidade is None:
            raise ValueError("Especialidade do serviço é obrigatória.")
        if duracao is None or duracao.total_seconds() <= 0:
            raise ValueError("Duração do serviço deve ser positiva.")
        if preco is None:
            raise ValueError("Preço do serviço é obrigatório.")
        self._id = id
        self.nome = nome
        self.especialidade = especialidade
        self.duracao = duracao
        self.preco = preco

    @property
    def id(self) -> UUID:
        return self._id

    def __eq__(self, other) -> bool:
        if not isinstance(other, Servico):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        minutos = int(self.duracao.total_seconds() // 60)
        return f"Servico{{id={self._id}, nome='{self.nome}', preco={self.preco}, duracao={minutos}min}}"
