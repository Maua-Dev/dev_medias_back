import json
from src.modules.grade_optmizer.app.grade_optmizer_presenter import lambda_handler


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
                'provas_que_tenho':[
                    {
                        'valor':6.0,
                        'peso':0.12
                    }
                ],
                'trabalhos_que_tenho':[
                    {
                        'valor':6.0,
                        'peso':0.08
                    },
                    {
                        'valor':6.0,
                        'peso':0.08
                    },
                ],
                'provas_que_quero':[
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
                        'peso':0.18
                    },
                ],
                'trabalhos_que_quero':[
                    {
                        'valor':None,
                        'peso':0.12
                    },
                    {
                        'valor':None,
                        'peso':0.12
                    }
                ],
                'media_desejada':6
            },
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 200
        assert json.loads(response["body"])["message"] == "O algoritmo retornou uma combinação válida de notas"
        
    def test_grade_optmizer_presenter_2(self):
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
                'provas_que_tenho':[
                    {
                        'valor':6.0,
                        'peso':0.12
                    }
                ],
                'trabalhos_que_tenho':[
                    {
                        'valor':6.0,
                        'peso':0.08
                    },
                    {
                        'valor':6.0,
                        'peso':0.08
                    },
                ],
                'provas_que_quero':[
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
                        'peso':0.18
                    },
                ],
                'trabalhos_que_quero':[
                    {
                        'valor':None,
                        'peso':0.12
                    },
                    {
                        'valor':None,
                        'peso':0.12
                    }
                ],
                'media_desejada':9.9
            },
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 404
        assert json.loads(response["body"]) == "O algoritmo não encontrou uma combinação possível de notas"
        
    def test_grade_optmizer_presenter_3(self):
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
                'provas_que_tenho':[
                    {
                        'valor':9.5,
                        'peso':0.5*0.6
                    },
                ],
                'trabalhos_que_tenho':[
                    {
                        'valor':9,
                        'peso':0.25*0.4
                    },
                    {
                        'valor':9.5,
                        'peso':0.25*0.4
                    },
                ],
                'provas_que_quero':[
                    {
                        'valor':None,
                        'peso':0.5*0.6
                    }
                ],
                'trabalhos_que_quero':[
                    {
                        'valor':None,
                        'peso':0.25*0.4
                    },
                    {
                        'valor':None,
                        'peso':0.25*0.4
                    }
                ],
                'media_desejada':6.0
            },
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
        for i in range(400):
            response = lambda_handler(event=event, context=None)
            assert response["statusCode"] == 200
        
    def test_grade_optmizer_presenter_bad_request(self):
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
                'provas_que_tenho':[
                    {
                        'valor':6.0,
                        'peso':0.12
                    }
                ],
                'trabalhos_que_tenho':[
                    {
                        'valor':6.0,
                        'peso':0.08
                    },
                    {
                        'valor':6.0,
                        'peso':0.08
                    },
                ],
                'provas_que_quero':[
                    {
                        'valor':None,
                        'peso':0.12
                    },
                    {
                        'valor':None,
                        'peso':0.19
                    },
                    {
                        'valor':None,
                        'peso':0.18
                    },
                ],
                'trabalhos_que_quero':[
                    {
                        'valor':None,
                        'peso':0.12
                    },
                    {
                        'valor':None,
                        'peso':0.12
                    }
                ],
                'media_desejada':6
            },
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == "A soma dos pesos das notas passadas deve ser 1"
  
    def test_grade_optmizer_presenter_bad_request_2(self):
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
                'provas_que_tenho':[
                    {
                        'valor':6.0,
                        'peso':0.12
                    }
                ],
                'trabalhos_que_tenho':[
                    {
                        'valor':6.0,
                        'peso':0.08
                    },
                    {
                        'valor':6.0,
                        'peso':0.08
                    },
                ],
                'provas_que_quero':[
                ],
                'trabalhos_que_quero':[
                ],
                'media_desejada':6
            },
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == "Parâmetro provas_que_quero e trabalhos_que_quero está(ão) inválido(s): Não podem ser listas vazias"
  