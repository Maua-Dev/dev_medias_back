from .genetic_algorithm_controller import GeneticAlgorithmController
from .genetic_algorithm_usecase import GeneticAlgorithmUsecase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse


usecase = GeneticAlgorithmUsecase()
controller = GeneticAlgorithmController(usecase)

def lambda_handler(event, context):

    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()

