from __future__ import annotations

from typing import FrozenSet, Optional, Set
from uuid import UUID

from app.domain.model.especialidade import Especialidade


class Profissional:

    def __init__(self, id: UUID, nome: str, especialidades: Optional[Set[Especialidade]]):
        if id is None:
            raise ValueError("ID do profissional é obrigatório.")
        if not nome or not nome.strip():
            raise ValueError("Nome do profissional é obrigatório.")
        self._id = id
        self.nome = nome
        self._especialidades = set(especialidades) if especialidades else set()

    def possui_especialidade(self, especialidade: Especialidade) -> bool:
        return especialidade in self._especialidades

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def especialidades(self) -> FrozenSet[Especialidade]:
        return frozenset(self._especialidades)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Profissional):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"Profissional{{id={self._id}, nome='{self.nome}', especialidades={self._especialidades}}}"
