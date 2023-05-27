from src.shared.helpers.errors.base_error import BaseError


class FunctionInputError(BaseError):
    def __init__(self, function_name: str, message: str):
        super().__init__(f"Erro na função {function_name}: {message}")