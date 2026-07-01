from app.domain.exception.reserva_exception import ReservaException


class HorarioIndisponivelException(ReservaException):

    def __init__(self, mensagem: str):
        super().__init__(mensagem)
