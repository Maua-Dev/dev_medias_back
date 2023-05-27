from src.shared.helpers.errors.base_error import BaseError


class EntityError(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Parâmetro {message} não é válido')

class EntityParameterError(BaseError):
    def __init__(self, message: str):
        super().__init__(message)

class EntityParameterTypeError(EntityError):
    def __init__(self, message: str):
        super().__init__(message)
        self.__message = message

    @property
    def message(self):
        return self.__message


    @property
    def message(self):
        return self.__message
