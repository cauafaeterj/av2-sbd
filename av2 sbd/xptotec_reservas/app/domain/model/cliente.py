from __future__ import annotations

from uuid import UUID

from app.domain.model.dinheiro import Dinheiro


class Cliente:

    def __init__(
        self,
        id: UUID,
        nome: str,
        email: str,
        telefone: str | None,
        credito_disponivel: Dinheiro | None = None,
    ):
        if id is None:
            raise ValueError("ID do cliente é obrigatório.")
        if not nome or not nome.strip():
            raise ValueError("Nome do cliente é obrigatório.")
        if not email or not email.strip():
            raise ValueError("Email do cliente é obrigatório.")
        self._id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.credito_disponivel = (
            credito_disponivel if credito_disponivel is not None else Dinheiro.ZERO
        )

    def adicionar_credito(self, valor: Dinheiro) -> None:
        if valor is None or valor.is_menor_que(Dinheiro.ZERO):
            raise ValueError("Valor de crédito deve ser positivo.")
        self.credito_disponivel = self.credito_disponivel.somar(valor)

    def debitar_credito(self, valor: Dinheiro) -> None:
        if valor.is_maior_que(self.credito_disponivel):
            raise ValueError("Saldo de crédito insuficiente.")
        self.credito_disponivel = self.credito_disponivel.subtrair(valor)

    @property
    def id(self) -> UUID:
        return self._id

    def __eq__(self, other) -> bool:
        if not isinstance(other, Cliente):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"Cliente{{id={self._id}, nome='{self.nome}', credito={self.credito_disponivel}}}"
