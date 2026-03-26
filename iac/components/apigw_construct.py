from aws_cdk import aws_apigateway as apigateway
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors, CorsOptions

class ApigwConstruct(Construct):
    rest_api: RestApi
    
    def __init__(self, scope: Construct, construct_id: str, stage: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        self.stage = stage
        
        cors_options = CorsOptions(
            allow_origins=Cors.ALL_ORIGINS,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=Cors.DEFAULT_HEADERS
        )
        
        self.rest_api = RestApi(
            self, 
            id=f"DevMedias_RestApi_{self.stage}",
            rest_api_name=f"DevMedias_RestApi_{self.stage}",
            description=f"This is the DevMedias RestApi for {self.stage}",
            deploy_options=apigateway.StageOptions(
                stage_name=stage.lower(),
                logging_level=apigateway.MethodLoggingLevel.OFF,
                data_trace_enabled=False,
                metrics_enabled=True,
            ),
            default_cors_preflight_options=cors_options,
        )
        

        self.api_gateway_resource = self.rest_api.root.add_resource(
            path_part="mss-medias",
            default_cors_preflight_options=cors_options
        )