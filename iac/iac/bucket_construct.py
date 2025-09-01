import os
import uuid

from constructs import Construct

from aws_cdk import (
    Duration,
    aws_s3,
    RemovalPolicy,
    aws_iam as iam, aws_cloudfront
)


class BucketConstruct(Construct):


    def __init__(self, scope: Construct, **kwargs) -> None:
        
        super().__init__(scope, "BucketConstruct")
        
        self.github_ref_name = os.environ.get("GITHUB_REF_NAME")
        self.aws_region = os.environ.get("AWS_REGION")

        REMOVAL_POLICY = RemovalPolicy.RETAIN if 'prod' in self.github_ref_name else RemovalPolicy.DESTROY

        self.subject_bucket = aws_s3.Bucket(
            self, "SubjectBucket",
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=REMOVAL_POLICY
        )
        
        # Novo bucket para armazenar os planos de ensino
        
        self.plans_bucket = aws_s3.Bucket(
            self, "PlansBucket",
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.RETAIN # a removal policy tera de sempre ser retain pois nao queremos perder os planos de ensino
        )

        oac = aws_cloudfront.CfnOriginAccessControl(
            self, "OAC", origin_access_control_config={
                "name": f"DevMedias Subject Bucket OAC {self.github_ref_name}",
                "originAccessControlOriginType": "s3",
                "signingBehavior": "always",
                "signingProtocol": "sigv4"
            }
        )

        cache_policy_subjects = aws_cloudfront.CachePolicy(
            self,
            "S3CachePolicy",
            cache_policy_name=f"DevMediasS3CachingOptimized-{self.github_ref_name}",
            comment=f"DevMedias Policy for {self.github_ref_name}. Supports Gzip and Brotli.",
            min_ttl=Duration.seconds(1),
            max_ttl=Duration.days(365),
            default_ttl=Duration.minutes(10), # precisamos mesmos de um time to live? 
            enable_accept_encoding_gzip=True,
            enable_accept_encoding_brotli=True
        )
        
        cache_policy_plans = aws_cloudfront.CachePolicy(
            self,
            "S3CachePolicy",
            cache_policy_name=f"DevMediasS3CachingOptimized-{self.github_ref_name}",
            comment=f"DevMedias Policy for {self.github_ref_name}. Supports Gzip and Brotli.",
            min_ttl=Duration.seconds(1),
            max_ttl=Duration.days(365),
            default_ttl=Duration.minutes(0),
            enable_accept_encoding_gzip=True,
            enable_accept_encoding_brotli=True
        )
        
        origin_request_policy = aws_cloudfront.OriginRequestPolicy(
            self,
            "S3OriginRequestPolicy",
            comment=f"DevMedias Policy for S3 origin with CORS {self.github_ref_name}",
            origin_request_policy_name=f"CORS-S3Origin-{self.github_ref_name}",
            header_behavior=aws_cloudfront.OriginRequestHeaderBehavior.allow_list(
                "Origin",
                "Access-Control-Request-Headers",
                "Access-Control-Request-Method"
            )
        )
        
        response_headers_policy = aws_cloudfront.ResponseHeadersPolicy.CORS_ALLOW_ALL_ORIGINS_WITH_PREFLIGHT

        cloudFrontWebDistribution = aws_cloudfront.CloudFrontWebDistribution(
            self, "CloudFrontWebDistribution",
            comment=f"DevMedias S3 CDN {self.github_ref_name}",
            price_class=aws_cloudfront.PriceClass.PRICE_CLASS_ALL,
            viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            origin_configs=[
                # --- ORIGEM 1: self.bucket (Comportamento Padrão) ---
                aws_cloudfront.SourceConfiguration(
                    s3_origin_source=aws_cloudfront.S3OriginConfig(
                        s3_bucket_source=self.subject_bucket,
                    ),
                    behaviors=[aws_cloudfront.Behavior(
                        is_default_behavior=True, # Trata todo o tráfego que não corresponder a outros behaviors
                        compress=True,
                        allowed_methods=aws_cloudfront.CloudFrontAllowedMethods.GET_HEAD_OPTIONS,
                        cached_methods=aws_cloudfront.CloudFrontAllowedCachedMethods.GET_HEAD_OPTIONS,
                        viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                        # Usando as políticas criadas acima
                        cache_policy=cache_policy_subjects,
                        origin_request_policy=origin_request_policy,
                        response_headers_policy=response_headers_policy
                    )]
                ),
                # --- NOVO: ORIGEM 2: plans_bucket (Comportamento para /plans/*) ---
                aws_cloudfront.SourceConfiguration(
                    s3_origin_source=aws_cloudfront.S3OriginConfig(
                        s3_bucket_source=self.plans_bucket,
                    ),
                    behaviors=[aws_cloudfront.Behavior(
                        is_default_behavior=False, # Não é o comportamento padrão
                        path_pattern="/plans/*", # IMPORTANTE: Define o caminho para esta origem
                        compress=True,
                        allowed_methods=aws_cloudfront.CloudFrontAllowedMethods.GET_HEAD_OPTIONS,
                        cached_methods=aws_cloudfront.CloudFrontAllowedCachedMethods.GET_HEAD_OPTIONS,
                        viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                        # Reutilizando as mesmas políticas
                        cache_policy=cache_policy_plans,
                        origin_request_policy=origin_request_policy,
                        response_headers_policy=response_headers_policy
                    )]
                )
            ]
        )
        
        cfn_distribution = cloudFrontWebDistribution.node.default_child
        
        cfn_distribution.add_property_override(
            "DistributionConfig.Origins.0.OriginAccessControlId",
            oac.get_att("Id")
        )
        
        cfn_distribution.add_property_override(
            "DistributionConfig.Origins.0.S3OriginConfig.OriginAccessIdentity", ""
        )
        
        cfn_distribution.add_property_override(
            "DistributionConfig.Origins.1.OriginAccessControlId",
            oac.get_att("Id")
        )
        
        cfn_distribution.add_property_override(
            "DistributionConfig.Origins.1.S3OriginConfig.OriginAccessIdentity", ""
        )
        
        bucket_policy_statement = iam.PolicyStatement(
            actions=["s3:GetObject"],
            principals=[iam.ServicePrincipal("cloudfront.amazonaws.com")],
            conditions={
                "StringEquals": {
                    # Garante que apenas esta distribuição CloudFront pode acessar o bucket
                    "AWS:SourceArn": f"arn:aws:cloudfront::{self.account}:distribution/{cloudFrontWebDistribution.distribution_id}"
                }
            }
        )
        
        self.subject_bucket.add_to_resource_policy(iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[self.subject_bucket.arn_for_objects("*")],
            principals=[iam.ServicePrincipal("cloudfront.amazonaws.com")],
            conditions={
                "StringEquals": {
                    "AWS:SourceArn": f"arn:aws:cloudfront::{self.account}:distribution/{cloudFrontWebDistribution.distribution_id}"
                }
            }
        ))
        
        self.plans_bucket.add_to_resource_policy(iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[self.plans_bucket.arn_for_objects("*")],
            principals=[iam.ServicePrincipal("cloudfront.amazonaws.com")],
            conditions={
                "StringEquals": {
                    "AWS:SourceArn": f"arn:aws:cloudfront::{self.account}:distribution/{cloudFrontWebDistribution.distribution_id}"
                }
            }
        ))
        
        
        