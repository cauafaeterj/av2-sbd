from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.model.cliente import Cliente


class ClienteRepository(ABC):

    @abstractmethod
    def buscar_por_id(self, id: UUID) -> Optional[Cliente]:
        ...

    @abstractmethod
    def salvar(self, cliente: Cliente) -> Cliente:
        ...
