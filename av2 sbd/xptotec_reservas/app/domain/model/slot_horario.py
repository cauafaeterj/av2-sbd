from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SlotHorario:

    inicio: datetime
    fim: datetime

    def __post_init__(self):
        if self.inicio is None or self.fim is None:
            raise ValueError("Início e fim do slot são obrigatórios.")
        if not self.fim > self.inicio:
            raise ValueError("O fim do slot deve ser posterior ao início.")

    def conflita_com(self, outro: "SlotHorario") -> bool:
        return self.inicio < outro.fim and self.fim > outro.inicio

    def __str__(self) -> str:
        return f"{self.inicio} → {self.fim}"
