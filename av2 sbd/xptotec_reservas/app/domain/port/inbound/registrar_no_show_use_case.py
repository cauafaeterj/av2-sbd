from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class NoShowResult:

    reserva_id: UUID
    status: str
    valor_retido: Decimal
    credito_gerado: Decimal
    credito_total_cliente: Decimal
    mensagem: str


class RegistrarNoShowUseCase(ABC):

    @abstractmethod
    def registrar_no_show(self, reserva_id: UUID) -> NoShowResult:
        ...
