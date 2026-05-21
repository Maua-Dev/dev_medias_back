from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

from .create_curso_controller import CreateCursoController
from .create_curso_usecase import CreateCursoUsecase

repository = Environments.get_curso_repo()
usecase = CreateCursoUsecase(repository)
controller = CreateCursoController(usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()
