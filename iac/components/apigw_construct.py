from aws_cdk import aws_apigateway as apigateway
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors, CorsOptions

from components.stack_generation import name_segment, normalize_generation


class ApigwConstruct(Construct):
    rest_api: RestApi
    
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stage: str,
        stack_generation: str = "",
        **kwargs,
    ):
        super().__init__(scope, construct_id, **kwargs)
        
        self.stage = stage
        gen = name_segment(stack_generation)
        gen_label = normalize_generation(stack_generation) or "legacy"
        
        cors_options = CorsOptions(
            allow_origins=Cors.ALL_ORIGINS,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            # X-Device-Id: identity for custom disciplinas (no login)
            allow_headers=list(dict.fromkeys([*Cors.DEFAULT_HEADERS, "X-Device-Id"])),
        )
        
        self.rest_api = RestApi(
            self, 
            id=f"DevMedias_RestApi_{gen}{self.stage}",
            rest_api_name=f"DevMedias_RestApi_{gen}{self.stage}",
            description=f"This is the DevMedias RestApi for {gen_label}/{self.stage}",
            deploy_options=apigateway.StageOptions(
                stage_name=stage.lower(),
                logging_level=apigateway.MethodLoggingLevel.OFF,
                data_trace_enabled=False,
                metrics_enabled=True,
            ),
            default_cors_preflight_options=cors_options,
        )
        
        # implementação de uma key para mínima proteção de rotas abertas como create_curso
        
        api_key = self.rest_api.add_api_key(
            id="AdminApiKey",
            api_key_name=f"admin-key-{gen}{stage.lower()}",
        )
        
        plan = self.rest_api.add_usage_plan("UsagePlan",
            name=f"AdminPlan-{gen}{stage}",
            api_stages=[apigateway.UsagePlanPerApiStage(
                api=self.rest_api,
                stage=self.rest_api.deployment_stage,
            )]
        )
        plan.add_api_key(api_key)

        self.api_gateway_resource = self.rest_api.root.add_resource(
            path_part="mss-medias",
            default_cors_preflight_options=cors_options
        )
