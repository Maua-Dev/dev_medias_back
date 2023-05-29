from src.shared.helpers.errors.base_error import BaseError


class MissingParameters(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Parâmetro {message} não existe')
class WrongTypeParameter(BaseError):
    def __init__(self, fieldName: str, fieldTypeExpected: str, fieldTypeReceived: str):
        super().__init__(f'Parâmetro {fieldName} não possui tipo correto.\n Recebido: {fieldTypeReceived}.\n Esperado: {fieldTypeExpected}')