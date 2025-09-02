from aws_cdk import (
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_lambda_event_sources as lambda_event_sources,
    Duration
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration


class LambdaStack(Construct):

    functions_that_need_dynamo_permissions = []

    def create_lambda_api_gateway_integration(self, module_name: str, method: str, api_resource: Resource, environment_variables: dict = {"STAGE": "TEST"}):
        function = lambda_.Function(
            self, module_name.title(),
            code=lambda_.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(30)
        )

        api_resource.add_resource(module_name.replace("_", "-")).add_method(method,
                                                                            integration=LambdaIntegration(
                                                                                function))

        return function
    
    def create_lambda_s3_object_creation_deletion_trigger_integration(
        self,
        module_name: str,
        bucket: s3.Bucket,
        environment_variables: dict
    ):
        
        function = lambda_.Function(
            self,
            module_name.title(),
            code=lambda_.Code.from_asset(f"../src/modules/{ module_name }"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(30)
        )
        
        bucket.add_event_notification(
            [s3.EventType.OBJECT_CREATED, s3.EventType.OBJECT_REMOVED_DELETE],
            s3n.LambdaDestination(function)
        )
        
        

    def __init__(
        self, 
        scope: Construct, 
        api_gateway_resource: Resource,
        plans_bucket: s3.Bucket,
        environment_variables: dict
    ) -> None:
        
        super().__init__(scope, "DevMediasLambda")

        self.lambda_layer = lambda_.LayerVersion(self, "DevMedias_Layer",
                                                 code=lambda_.Code.from_asset("./lambda_layer_out_temp"),
                                                 compatible_runtimes=[lambda_.Runtime.PYTHON_3_9]
                                                )

        self.grade_optimizer_function = self.create_lambda_api_gateway_integration("grade_optmizer",
                                                                                   "POST",
                                                                                   api_resource=api_gateway_resource,
                                                                                   environment_variables=environment_variables)
        
        self.calculate_mean_function = self.create_lambda_api_gateway_integration("calculate_mean",
                                                                                   "POST",
                                                                                   api_resource=api_gateway_resource,
                                                                                   environment_variables=environment_variables)

        self.plans_extractor_function = self.create_lambda_s3_object_creation_deletion_trigger_integration(
            module_name="plans_extractor",
            bucket=plans_bucket,
            environment_variables=environment_variables
        )