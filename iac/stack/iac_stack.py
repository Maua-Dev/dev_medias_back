import os
from aws_cdk import (
    Stack
)
from constructs import Construct

from components.apigw_construct import ApigwConstruct
from components.dynamo_construct import DynamoConstruct
from components.lambda_construct import LambdaConstruct
from components.s3_construct import S3Construct
from components.ssm_construct import SsmConstruct

class IacStack(Stack):
    lambda_construct: LambdaConstruct

    def __init__(
        self, 
        scope: Construct,
        stack_id: str,
        stack_name: str,
        stage: str,
        **kwargs
    ) -> None:
        super().__init__(scope, stack_id, **kwargs)

        self.github_ref_name = os.environ.get("GITHUB_REF_NAME", "")
        self.aws_region = os.environ.get("AWS_REGION")
        self.s3_assets_cdn = os.environ.get("S3_ASSETS_CDN")

        self.apigw_construct = ApigwConstruct(
            self, 
            construct_id=f"{stack_name}Apigw", 
            stage=stage
        )
        
        self.s3_construct = S3Construct(
            self, 
            construct_id=f"{stack_name}S3", 
            stage=stage
        )

        self.dynamo_construct = DynamoConstruct(
            self,
            construct_id=f"{stack_name}Dynamo",
            stack_name=stack_name,
            stage=stage,
        )

        ENVIRONMENT_VARIABLES = {
            "STAGE": stage.upper(),
            "PLANS_BUCKET_NAME": self.s3_construct.plans_bucket.bucket_name,
            "SUBJECT_BUCKET_NAME": self.s3_construct.subject_bucket.bucket_name,
            "ACADEMIC_CATALOG_TABLE_NAME": self.dynamo_construct.academic_catalog_table.table_name,
            "FROM_EMAIL": os.environ.get("FROM_EMAIL"),
            "REPLY_TO_EMAIL": os.environ.get("REPLY_TO_EMAIL"),
            "HIDDEN_COPY": os.environ.get("HIDDEN_COPY"),
        }

        self.lambda_construct = LambdaConstruct(
            self, 
            construct_id=f"{stack_name}Lambda",
            api_gateway_resource=self.apigw_construct.api_gateway_resource,
            stage=stage,
            stack_name=stack_name,
            plans_bucket=self.s3_construct.plans_bucket,
            subject_bucket=self.s3_construct.subject_bucket,
            environment_variables=ENVIRONMENT_VARIABLES
        )
        
        for function in self.lambda_construct.funtions_that_need_dynamo_db_access:
            self.dynamo_construct.academic_catalog_table.grant_read_write_data(function)
        
        # nova instância SSM manager para passar automaticamente variáveis a um hub de segredos
        # da prórpia conta, evitando ter que manualmente passa-las para o github secrets
        
        # isso evita problemas de discrepância nos endpoints
        
        # atenção aqui, isso deve suprir ao que estamos precisando / pegando de variáveis de 
        # ambiente no CD do front
        
        self.ssm_construct = SsmConstruct(
            self, 
            construct_id=f"{stack_name}Ssm",
            mss_name_identification_for_path="devmedias",
            api=self.apigw_construct.rest_api,
            api_gateway_resource=self.apigw_construct.api_gateway_resource,
            buckets=None, # o que deve ser salvo são os CDNs, visto que os buckets bloqueiam acesso pela URL publica
            extra_params={
                "cdn/subjects": self.s3_construct.cloudfront_distribution_subjects.distribution_domain_name
            },
            stage=stage
        )
