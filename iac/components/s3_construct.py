
from constructs import Construct
from aws_cdk import Duration, RemovalPolicy, Stack
from aws_cdk import aws_cloudfront, aws_iam as iam, aws_s3
import random

class S3Construct(Construct):
    plans_bucket: aws_s3.Bucket
    subject_bucket: aws_s3.Bucket
    cloudfront_distribution_plans: aws_cloudfront.CloudFrontWebDistribution
    cloudfront_distribution_subjects: aws_cloudfront.CloudFrontWebDistribution
    
    def _build_distribution(
        self,
        distribution_id: str,
        bucket: aws_s3.Bucket,
        stage: str,
    ) -> aws_cloudfront.CloudFrontWebDistribution:
        return aws_cloudfront.CloudFrontWebDistribution(
            self,
            id=distribution_id,
            comment=f"DevMedias {distribution_id} S3 CDN {stage}",
            origin_configs=[
                aws_cloudfront.SourceConfiguration(
                    s3_origin_source=aws_cloudfront.S3OriginConfig(
                        s3_bucket_source=bucket,
                    ),
                    behaviors=[
                        aws_cloudfront.Behavior(
                            is_default_behavior=True,
                            compress=True,
                            allowed_methods=aws_cloudfront.CloudFrontAllowedMethods.GET_HEAD_OPTIONS,
                            cached_methods=aws_cloudfront.CloudFrontAllowedCachedMethods.GET_HEAD_OPTIONS,
                            viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                            forwarded_values=aws_cloudfront.CfnDistribution.ForwardedValuesProperty(
                                query_string=True,
                                headers=[
                                    "Origin",
                                    "Access-Control-Request-Headers",
                                    "Access-Control-Request-Method",
                                ],
                            ),
                        )
                    ],
                )
            ],
            price_class=aws_cloudfront.PriceClass.PRICE_CLASS_ALL,
            viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        )

    def _attach_cloudfront_bucket_policy(
        self,
        bucket: aws_s3.Bucket,
        distribution: aws_cloudfront.CloudFrontWebDistribution
    ) -> None:
        account_id = Stack.of(self).account
        source_arn = f"arn:aws:cloudfront::{account_id}:distribution/{distribution.distribution_id}"
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[f"arn:aws:s3:::{bucket.bucket_name}/*"],
                principals=[iam.ServicePrincipal("cloudfront.amazonaws.com")],
                conditions={"StringEquals": {"AWS:SourceArn": source_arn}},
            )
        )

    def create_bucket_with_distribution(
        self,   
        *,
        resource_prefix: str,
        bucket_name: str,
        default_ttl: Duration,
        stage: str,
    ) -> tuple[aws_s3.Bucket, aws_cloudfront.CloudFrontWebDistribution]:
        bucket = aws_s3.Bucket(
            self,
            f"{resource_prefix}Bucket",
            bucket_name=bucket_name,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=self.removal_policy,
            auto_delete_objects=self.removal_policy == RemovalPolicy.DESTROY,
        )

        oac = aws_cloudfront.CfnOriginAccessControl(
            self,
            f"{resource_prefix}OAC",
            origin_access_control_config={
                "name": f"{resource_prefix} OAC {stage}",
                "originAccessControlOriginType": "s3",
                "signingBehavior": "always",
                "signingProtocol": "sigv4",
            },
        )

        distribution = self._build_distribution(
            distribution_id=f"CloudFrontWebDistribution{resource_prefix}",
            bucket=bucket,
            stage=stage,
        )

        cache_policy = aws_cloudfront.CachePolicy(
            self,
            f"{resource_prefix}CachePolicy",
            cache_policy_name=f"DevMedias-{resource_prefix}-Cache-{stage}",
            comment=f"Cache policy for {resource_prefix} bucket",
            min_ttl=Duration.seconds(1),
            max_ttl=Duration.days(365),
            default_ttl=default_ttl,
            enable_accept_encoding_gzip=True,
            enable_accept_encoding_brotli=True,
        )

        origin_request_policy = aws_cloudfront.OriginRequestPolicy(
            self,
            f"{resource_prefix}OriginRequestPolicy",
            origin_request_policy_name=f"DevMedias-{resource_prefix}-ORP-{stage}",
            comment=f"Origin request policy for {resource_prefix} bucket",
            header_behavior=aws_cloudfront.OriginRequestHeaderBehavior.allow_list(
                "Origin",
                "Access-Control-Request-Headers",
                "Access-Control-Request-Method",
            ),
        )

        cfn_distribution = distribution.node.default_child
        cfn_distribution.add_property_override(
            "DistributionConfig.Origins.0.OriginAccessControlId",
            oac.get_att("Id"),
        )
        cfn_distribution.add_property_override(
            "DistributionConfig.DefaultCacheBehavior.CachePolicyId",
            cache_policy.cache_policy_id,
        )
        cfn_distribution.add_property_override(
            "DistributionConfig.DefaultCacheBehavior.OriginRequestPolicyId",
            origin_request_policy.origin_request_policy_id,
        )
        cfn_distribution.add_property_override(
            "DistributionConfig.DefaultCacheBehavior.ResponseHeadersPolicyId",
            aws_cloudfront.ResponseHeadersPolicy.CORS_ALLOW_ALL_ORIGINS_WITH_PREFLIGHT.response_headers_policy_id,
        )

        self._attach_cloudfront_bucket_policy(bucket, distribution)
        return bucket, distribution

    def __init__(self, scope: Construct, construct_id: str, stage: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.stage = stage
        self.removal_policy = RemovalPolicy.RETAIN if stage == "PROD" else RemovalPolicy.DESTROY
        
        identifier = "2026-after-refactoring"

        self.plans_bucket, self.cloudfront_distribution_plans = self.create_bucket_with_distribution(
            resource_prefix="Plans",
            bucket_name=f"devmedias-plans-{self.stage.lower()}-{identifier}",
            default_ttl=Duration.seconds(30),
            stage=stage,
        )

        self.subject_bucket, self.cloudfront_distribution_subjects = self.create_bucket_with_distribution(
            resource_prefix="Subjects",
            bucket_name=f"devmedias-subjects-{self.stage.lower()}-{identifier}",
            default_ttl=Duration.seconds(86400),
            stage=stage,
        )
