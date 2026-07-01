from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.domain.model.reserva import Reserva

if TYPE_CHECKING:
    from app.application.dto.criar_reserva_command import CriarReservaCommand


class CriarReservaUseCase(ABC):

    @abstractmethod
    def criar_reserva(self, command: "CriarReservaCommand") -> Reserva:
        ...
