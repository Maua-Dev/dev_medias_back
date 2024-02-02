import os
from aws_cdk import (
    Stack,
)
from constructs import Construct

from .lambda_stack import LambdaStack
from aws_cdk.aws_apigateway import RestApi, Cors

from .subject_stack import SubjectStack


class IacStack(Stack):
    lambda_stack: LambdaStack

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.github_ref_name = os.environ.get("GITHUB_REF_NAME")
        self.aws_region = os.environ.get("AWS_REGION")
        self.s3_assets_cdn = os.environ.get("S3_ASSETS_CDN")

        self.rest_api = RestApi(self, f"DevMedias_RestApi_{self.github_ref_name}",
                                rest_api_name=f"DevMedias_RestApi_{self.github_ref_name}",
                                description="This is the DevMedias RestApi",
                                default_cors_preflight_options=
                                {
                                    "allow_origins": Cors.ALL_ORIGINS,
                                    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                                    "allow_headers": ["*"]
                                },
                                )

        api_gateway_resource = self.rest_api.root.add_resource("mss-medias", default_cors_preflight_options=
        {
            "allow_origins": Cors.ALL_ORIGINS,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": Cors.DEFAULT_HEADERS
        }
                                                               )
        if 'prod' in self.github_ref_name:
            stage = 'PROD'

        elif 'homolog' in self.github_ref_name:
            stage = 'HOMOLOG'

        else:
            stage = 'DEV'

        ENVIRONMENT_VARIABLES = {
            "STAGE": stage,
        }

        self.lambda_stack = LambdaStack(self, api_gateway_resource=api_gateway_resource,
                                        environment_variables=ENVIRONMENT_VARIABLES)

        self.subject_stack = SubjectStack(self)
