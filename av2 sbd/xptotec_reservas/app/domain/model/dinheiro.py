from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Union

Numero = Union[int, float, str, Decimal]


class Dinheiro:

    __slots__ = ("_valor",)

    def __init__(self, valor: Decimal):
        if valor is None:
            raise ValueError("Valor monetário não pode ser nulo.")
        if not isinstance(valor, Decimal):
            valor = Decimal(str(valor))
        self._valor = valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @staticmethod
    def of(valor: Numero) -> "Dinheiro":
        if isinstance(valor, Decimal):
            return Dinheiro(valor)
        return Dinheiro(Decimal(str(valor)))

    def somar(self, outro: "Dinheiro") -> "Dinheiro":
        return Dinheiro(self._valor + outro._valor)

    def subtrair(self, outro: "Dinheiro") -> "Dinheiro":
        return Dinheiro(self._valor - outro._valor)

    def percentual(self, porcentagem: int) -> "Dinheiro":
        fator = (Decimal(porcentagem) / Decimal(100)).quantize(
            Decimal("0.0001"), rounding=ROUND_HALF_UP
        )
        return Dinheiro(self._valor * fator)

    def is_maior_que(self, outro: "Dinheiro") -> bool:
        return self._valor > outro._valor

    def is_menor_que(self, outro: "Dinheiro") -> bool:
        return self._valor < outro._valor

    @property
    def valor(self) -> Decimal:
        return self._valor

    def __eq__(self, other) -> bool:
        if not isinstance(other, Dinheiro):
            return NotImplemented
        return self._valor == other._valor

    def __hash__(self) -> int:
        return hash(self._valor.normalize())

    def __repr__(self) -> str:
        return f"R${self._valor}"

    def __str__(self) -> str:
        return f"R${self._valor}"


Dinheiro.ZERO = Dinheiro(Decimal("0"))
