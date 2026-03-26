import os
from aws_cdk import (
    Stack
)
from constructs import Construct

from ..components.lambda_construct import LambdaConstruct
from ..components.apigw_construct import ApigwConstruct
from ..components.s3_construct import S3Construct

class IacStack(Stack):
    lambda_construct: LambdaConstruct

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.github_ref_name = os.environ.get("GITHUB_REF_NAME", "")
        self.aws_region = os.environ.get("AWS_REGION")
        self.s3_assets_cdn = os.environ.get("S3_ASSETS_CDN")
        
        if 'prod' in self.github_ref_name:
            stage = 'PROD'

        elif 'homolog' in self.github_ref_name:
            stage = 'HOMOLOG'

        else:
            stage = 'DEV'
        
        self.apigw_construct = ApigwConstruct(self, stage=stage, construct_id="DevMediasApiGateway")
        
        self.s3_construct = S3Construct(self, construct_id="DevMediasS3", stage=stage)
        
        ENVIRONMENT_VARIABLES = {
            "STAGE": stage,
            "PLANS_BUCKET_NAME": self.s3_construct.plans_bucket.bucket_name,
            "SUBJECT_BUCKET_NAME": self.s3_construct.subject_bucket.bucket_name,
            "FROM_EMAIL": os.environ.get("FROM_EMAIL"),
            "REPLY_TO_EMAIL": os.environ.get("REPLY_TO_EMAIL"),
            "HIDDEN_COPY": os.environ.get("HIDDEN_COPY"),
        }

        self.lambda_construct = LambdaConstruct(
            self, 
            api_gateway_resource=self.apigw_construct.api_gateway_resource,
            plans_bucket=self.s3_construct.plans_bucket,
            subject_bucket=self.s3_construct.subject_bucket,
            environment_variables=ENVIRONMENT_VARIABLES
        )
        
