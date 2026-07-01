from enum import Enum


class StatusReserva(str, Enum):
    PENDENTE = "PENDENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    NO_SHOW = "NO_SHOW"
    CONCLUIDA = "CONCLUIDA"
