from aws_cdk import (
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    Duration
)
from aws_cdk import aws_iam as iam
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration


class LambdaConstruct(Construct):
    
    stage: str
    stack_name: str

    def create_lambda_api_gateway_integration(
        self, 
        module_name: str, 
        method: str, 
        api_resource: Resource, 
        environment_variables: dict = {"STAGE": "TEST"},
        public: bool = False
    ) -> lambda_.Function:
        function = lambda_.Function(
            self, module_name.title(),
            code=lambda_.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            function_name=f"{module_name}-{self.stack_name}-{self.stage}"[:63],
            runtime=lambda_.Runtime.PYTHON_3_13,
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(30)
        )

        if public:
            api_resource.add_resource("public").add_resource(module_name.replace("_", "-")).add_method(
                method,
                integration=LambdaIntegration(function)
            )
        else:
            api_resource.add_resource(module_name.replace("_", "-")).add_method(
                method,
                integration=LambdaIntegration(function)
            )

        return function
    
    def create_lambda_s3_object_creation_deletion_trigger_integration(
        self,
        module_name: str,
        bucket_plans: s3.Bucket,
        bucket_subjects: s3.Bucket,
        environment_variables: dict
    ) -> lambda_.Function:
        
        function = lambda_.Function(
            self,
            module_name.title(),
            code=lambda_.Code.from_asset(f"../src/modules/{ module_name }"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            function_name=f"{module_name}-{self.stack_name}-{self.stage}"[:63],
            runtime=lambda_.Runtime.PYTHON_3_13,
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(90) # increased time for excel and bedrock
        )
        
        bucket_plans.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(function)
        )
                
        # bucket.add_event_notification(
        #     s3.EventType.OBJECT_REMOVED_DELETE,
        #     s3n.LambdaDestination(function)
        # )
        
        bucket_plans.grant_read(function) # read the plans
        bucket_subjects.grant_read(function) # read all subjects
        bucket_subjects.grant_write(function) # write all subjects
        
        return function
        

    def __init__(
        self, 
        scope: Construct,
        construct_id: str,
        stage: str,
        stack_name: str,
        api_gateway_resource: Resource,
        plans_bucket: s3.Bucket,
        subject_bucket: s3.Bucket,
        environment_variables: dict,
        **kargs
    ) -> None:
        
        super().__init__(scope, construct_id, **kargs)
        
        self.stage = stage
        self.stack_name = stack_name

        self.lambda_layer = lambda_.LayerVersion(
            self, 
            id=f"{stack_name}_LambdaLayer_{stage}",
            layer_version_name=f"{stack_name}-LambdaLayer-{self.stage}",
            # a pasta .build foi obtida do adjust layer directory, certifique-se de que a configuração da pasta layer gerada la esta igual
            code=lambda_.Code.from_asset("./build"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_13]
        )
        
        self.contact_us = self.create_lambda_api_gateway_integration(
            module_name="contact_us",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            public=True
        )
        
        ses_send_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["ses:SendEmail"],
            resources=["*"],
            conditions={
                "StringEquals": {
                    "ses:FromAddress": environment_variables.get("FROM_EMAIL")
                }
            }
        )
        self.contact_us.add_to_role_policy(ses_send_policy)

        self.grade_optimizer_function = self.create_lambda_api_gateway_integration(
            module_name="grade_optmizer",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables
        )
        
        self.genetic_algorithm_function = self.create_lambda_api_gateway_integration(
            module_name="genetic_algorithm",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables
        )
        
        self.calculate_mean_function = self.create_lambda_api_gateway_integration(
            module_name="calculate_mean",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables
        )

        self.plans_extractor_function = self.create_lambda_s3_object_creation_deletion_trigger_integration(
            module_name="plans_extractor",
            bucket_plans=plans_bucket,
            bucket_subjects=subject_bucket,
            environment_variables=environment_variables
        )
        
        bedrock_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "bedrock:InvokeModel",
                "aws-marketplace:ViewSubscriptions",
                "aws-marketplace:Subscribe"
            ],
            resources=["*"]
        )
        
        self.plans_extractor_function.add_to_role_policy(
            bedrock_policy
        )
        