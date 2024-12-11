from .calculate_mean_controller import CalculateMeanController
from .calculate_mean_usecase import CalculateMeanUsecase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse


usecase = CalculateMeanUsecase()
controller = CalculateMeanController(usecase)

def lambda_handler(event, context):

    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()

