from src.shared.environments import Environments
from .get_all_disciplinas_controller import GetAllDisciplinasController
from .get_all_disciplinas_usecase import GetAllDisciplinasUsecase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repository = Environments.get_disciplina_repo()
usecase = GetAllDisciplinasUsecase(repository)
controller = GetAllDisciplinasController(usecase)


def lambda_handler(event, context):

    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()

