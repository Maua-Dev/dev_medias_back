from src.shared.environments import Environments
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.usecase_errors import InvalidInput
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.http.device_id import require_device_id

from .update_custom_disciplina_controller import UpdateCustomDisciplinaController
from .update_custom_disciplina_usecase import UpdateCustomDisciplinaUsecase


def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    try:
        device_id = require_device_id(http_request.headers)
    except (MissingParameters, InvalidInput) as error:
        return LambdaHttpResponse(status_code=400, body=error.message).toDict()

    repository = Environments.get_disciplina_repo(user_id=device_id)
    usecase = UpdateCustomDisciplinaUsecase(repository)
    controller = UpdateCustomDisciplinaController(usecase)
    response = controller(http_request)
    return LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers,
    ).toDict()
