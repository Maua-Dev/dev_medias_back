from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

from .get_all_cursos_controller import GetAllCursosController
from .get_all_cursos_usecase import GetAllCursosUsecase

repository = Environments.get_curso_repo()
usecase = GetAllCursosUsecase(repository)
controller = GetAllCursosController(usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()
