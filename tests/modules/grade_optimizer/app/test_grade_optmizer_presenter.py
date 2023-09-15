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
        event = {'resource': '/mss-medias/grade-optmizer', 'path': '/mss-medias/grade-optmizer', 'httpMethod': 'POST', 'headers': {'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'pt-BR,pt;q=0.9', 'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-ASN': '262572', 'CloudFront-Viewer-Country': 'BR', 'content-type': 'application/x-www-form-urlencoded', 'Host': '6y6t219val.execute-api.us-east-1.amazonaws.com', 'User-Agent': 'dev_medias_front_rn/13 CFNetwork/1399 Darwin/22.1.0', 'Via': '2.0 f3d66dd6903122e5440aadd45dc50cc4.cloudfront.net (CloudFront)', 'X-Amz-Cf-Id': 'AfLnC3mA1yN6jdQlm8sQV2Ay1uMGueheaDKSDSXRvZY3Lt37eWDPHQ==', 'X-Amzn-Trace-Id': 'Root=1-65049ed9-19583a3f770e787702731a1e', 'X-Forwarded-For': '177.73.176.61, 15.158.37.228', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['application/json, text/plain, */*'], 'Accept-Encoding': ['gzip, deflate, br'], 'Accept-Language': ['pt-BR,pt;q=0.9'], 'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'], 'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'], 'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-ASN': ['262572'], 'CloudFront-Viewer-Country': ['BR'], 'content-type': ['application/x-www-form-urlencoded'], 'Host': ['6y6t219val.execute-api.us-east-1.amazonaws.com'], 'User-Agent': ['dev_medias_front_rn/13 CFNetwork/1399 Darwin/22.1.0'], 'Via': ['2.0 f3d66dd6903122e5440aadd45dc50cc4.cloudfront.net (CloudFront)'], 'X-Amz-Cf-Id': ['AfLnC3mA1yN6jdQlm8sQV2Ay1uMGueheaDKSDSXRvZY3Lt37eWDPHQ=='], 'X-Amzn-Trace-Id': ['Root=1-65049ed9-19583a3f770e787702731a1e'], 'X-Forwarded-For': ['177.73.176.61, 15.158.37.228'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'efmcxg', 'resourcePath': '/mss-medias/grade-optmizer', 'httpMethod': 'POST', 'extendedRequestId': 'LT3CDEbAIAMFhaA=', 'requestTime': '15/Sep/2023:18:13:45 +0000', 'path': '/prod/mss-medias/grade-optmizer', 'accountId': '264055331071', 'protocol': 'HTTP/1.1', 'stage': 'prod', 'domainPrefix': '6y6t219val', 'requestTimeEpoch': 1694801625664, 'requestId': '6268e957-9a15-4113-9235-d80770cb6939', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '177.73.176.61', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'dev_medias_front_rn/13 CFNetwork/1399 Darwin/22.1.0', 'user': None}, 'domainName': '6y6t219val.execute-api.us-east-1.amazonaws.com', 'apiId': '6y6t219val'}, 'body': '{"provas_que_tenho":[{"valor":9.5,"peso":0.3}],"provas_que_quero":[{"peso":0.3}],"trabalhos_que_tenho":[{"valor":9,"peso":0.1},{"valor":9.5,"peso":0.1}],"trabalhos_que_quero":[{"peso":0.1},{"peso":0.1}],"media_desejada":6}', 'isBase64Encoded': False}

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
  