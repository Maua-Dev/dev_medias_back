import os
from aws_cdk import (
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_logs as logs,
    Stack
)

from constructs import Construct

from .plans_stack import PlansStack


from .lambda_stack import LambdaStack
from aws_cdk.aws_apigateway import RestApi, Cors

from .subject_stack import SubjectStack
from .lambda_contact_us_stack import LambdaContactUsStack

import json

class IacStack(Stack):
    lambda_stack: LambdaStack

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.github_ref_name = os.environ.get("GITHUB_REF_NAME")
        self.aws_region = os.environ.get("AWS_REGION")
        self.s3_assets_cdn = os.environ.get("S3_ASSETS_CDN")
        
        if 'prod' in self.github_ref_name:
            stage = 'PROD'

        elif 'homolog' in self.github_ref_name:
            stage = 'HOMOLOG'

        else:
            stage = 'DEV'
        
        log_group = logs.LogGroup(self, f"DevMedias_ApiGateway_AccessLogs_{stage}")

        self.rest_api = RestApi(self, f"DevMedias_RestApi_{self.github_ref_name}",
                                rest_api_name=f"DevMedias_RestApi_{self.github_ref_name}",
                                description="This is the DevMedias RestApi",
                                default_cors_preflight_options=
                                {
                                    "allow_origins": Cors.ALL_ORIGINS,
                                    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                                    "allow_headers": ["*"]
                                },
                                deploy_options=apigateway.StageOptions(
                                    stage_name="prod",  # deixar como o padrao que estava errado, tem que comunicar que para arrumar aqui é apenas trocar pela variavel stage
                                    access_log_destination=apigateway.LogGroupLogDestination(log_group),
                                    access_log_format=apigateway.AccessLogFormat.custom(
                                        json.dumps({
                                            "requestId": "$context.requestId",
                                            "ip": "$context.identity.sourceIp",
                                            "caller": "$context.identity.caller",
                                            "user": "$context.identity.user",
                                            "requestTime": "$context.requestTime",
                                            "httpMethod": "$context.httpMethod",
                                            "resourcePath": "$context.resourcePath",
                                            "status": "$context.status",
                                            "protocol": "$context.protocol",
                                            "responseLength": "$context.responseLength",
                                            "queryString": "$context.requestOverride.path.querystring"
                                        })
                                    ),
                                    logging_level=apigateway.MethodLoggingLevel.INFO, 
                                    data_trace_enabled=True, 
                                    metrics_enabled=True 
                                )
        )

        api_gateway_resource = self.rest_api.root.add_resource("mss-medias", default_cors_preflight_options=
        {
            "allow_origins": Cors.ALL_ORIGINS,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": Cors.DEFAULT_HEADERS
        }
        )
                                                               
        ENVIRONMENT_VARIABLES = {
            "STAGE": stage,
        }

        self.lambda_stack = LambdaStack(
            self, 
            api_gateway_resource=api_gateway_resource,
            environment_variables=ENVIRONMENT_VARIABLES
        )

        self.contact_us_lambda_stack = LambdaContactUsStack(self, api_gateway_resource=api_gateway_resource,
                                                            lambda_layer=self.lambda_stack.lambda_layer,
                                                            stage=stage)
        
        self.subject_stack = SubjectStack(self)
        self.plans_stack = PlansStack(self)
