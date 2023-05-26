import json
from src.modules.grade_optimizer.app.grade_optmizer_presenter import lambda_handler


class Test_GradeOptmizerPresenter:
    def test_grade_optmizer_presenter(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
            "cookies": [
                "cookie1",
                "cookie2"
            ],
            "headers": {
                "header1": "value1",
                "header2": "value1,value2"
            },
            "queryStringParameters": None,
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "iam": {
                        "accessKey": "AKIA...",
                        "accountId": "111122223333",
                        "callerId": "AIDA...",
                        "cognitoIdentity": None,
                        "principalOrgId": None,
                        "userArn": "arn:aws:iam::111122223333:user/example-user",
                        "userId": "AIDA..."
                    }
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "POST",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390
            },
            "body": {
                'notas_que_tenho':[
                    {
                        'valor':6.0,
                        'peso':0.12
                    },
                    {
                        'valor':6.0,
                        'peso':0.08
                    },
                    {
                        'valor':6.0,
                        'peso':0.08
                    },
                ],
                'notas_que_quero':[
                    {
                        'valor':None,
                        'peso':0.12
                    },
                    {
                        'valor':None,
                        'peso':0.18
                    },
                    {
                        'valor':None,
                        'peso':0.12
                    },
                    {
                        'valor':None,
                        'peso':0.18
                    },
                    {
                        'valor':None,
                        'peso':0.12
                    }
                ],
                'media_desejada':6.0
            },
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 200
        assert json.loads(response["body"])["message"] == "the algorithm retrieved a possible combination of grades successfully"