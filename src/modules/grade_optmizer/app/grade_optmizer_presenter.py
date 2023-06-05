from .grade_optmizer_controller import GradeOptmizerController
from .grade_optmizer_usecase import GradeOptimizerUsecase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse


usecase = GradeOptimizerUsecase()
controller = GradeOptmizerController(usecase)

def lambda_handler(event, context):

    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()

