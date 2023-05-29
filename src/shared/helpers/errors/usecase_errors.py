from src.shared.helpers.errors.base_error import BaseError

class NoItemsFound(BaseError):
    def __init__(self, message: str):
        super().__init__(f'No items found for {message}')

class DuplicatedItem(BaseError):
    def __init__(self, message: str):
        super().__init__(f'The item alredy exists for this {message}')

class InvalidInput(BaseError):
    def __init__(self, parameter: str, message: str):
        super().__init__(f'Parâmetro {parameter} está inválido: {message}')        

class ForbiddenAction(BaseError):
    def __init__(self, message: str):
        super().__init__(f'That action is forbidden for this {message}')

