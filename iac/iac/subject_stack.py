import os

from constructs import Construct

from aws_cdk import (
    Duration,
    aws_s3,
    RemovalPolicy,
    aws_iam as iam, aws_cloudfront
)


class SubjectStack(Construct):

    def __init__(self, scope: Construct, **kwargs) -> None:
        super().__init__(scope, "SubjectStack")
        self.github_ref_name = os.environ.get("GITHUB_REF_NAME")
        self.aws_region = os.environ.get("AWS_REGION")
        self.aws_account_id = os.environ.get("AWS_ACCOUNT_ID")

        REMOVAL_POLICY = RemovalPolicy.RETAIN if 'prod' in self.github_ref_name else RemovalPolicy.DESTROY

        self.bucket = aws_s3.Bucket(
            self, "SubjectBucket",
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=REMOVAL_POLICY
        )

        oac = aws_cloudfront.CfnOriginAccessControl(
            self, "OAC", origin_access_control_config={
                "name": f"DevMedias Subject Bucket OAC {self.github_ref_name}",
                "originAccessControlOriginType": "s3",
                "signingBehavior": "always",
                "signingProtocol": "sigv4"
            }
        )

        cloudFrontWebDistribution = aws_cloudfront.CloudFrontWebDistribution(
            self, "CloudFrontWebDistribution",
            comment=f"DevMedias Subject S3 CDN {self.github_ref_name}",
            origin_configs=[
                aws_cloudfront.SourceConfiguration(
                    s3_origin_source=aws_cloudfront.S3OriginConfig(
                        s3_bucket_source=self.bucket,

                    ),
                    behaviors=[aws_cloudfront.Behavior(
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
                                "Access-Control-Request-Method"
                            ]
                        ),
                    )]
                )
            ],
            price_class=aws_cloudfront.PriceClass.PRICE_CLASS_ALL,
            viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        )

        cfn_distribution = cloudFrontWebDistribution.node.default_child
        cfn_distribution.add_property_override(
            'DistributionConfig.Origins.0.OriginAccessControlId',
            oac.get_att('Id')
        )

        cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6"

        cachePolicy = aws_cloudfront.CachePolicy(
            self, cache_policy_id,
            cache_policy_name="CachingOptimized",
            comment=f"DevMedias Policy for {self.github_ref_name}. Policy with caching enabled. Supports Gzip and Brotli compression.",
            min_ttl=Duration.seconds(1),
            max_ttl=Duration.days(365),
            default_ttl=Duration.seconds(86400),
            enable_accept_encoding_gzip=True,
            enable_accept_encoding_brotli=True
        )

        cfn_distribution.add_property_override(
            "DistributionConfig.DefaultCacheBehavior.CachePolicyId",
            cachePolicy.cache_policy_id
        )

        origin_request_policy_id = "88a5eaf4-2fd4-4709-b370-b4c650ea3fcf"

        originRequestPolicy = aws_cloudfront.OriginRequestPolicy(
            self,
            origin_request_policy_id,
            comment=f"DevMedias Policy for S3 origin with CORS {self.github_ref_name}",
            origin_request_policy_name="CORS-S3Origin",
            header_behavior=aws_cloudfront.OriginRequestHeaderBehavior.allow_list(
                "Origin",
                "Access-Control-Request-Headers",
                "Access-Control-Request-Method"
            )
        )

        cfn_distribution.add_property_override(
            "DistributionConfig.DefaultCacheBehavior.OriginRequestPolicyId",
            originRequestPolicy.origin_request_policy_id
        )

        response_headers_policy = aws_cloudfront.ResponseHeadersPolicy.CORS_ALLOW_ALL_ORIGINS_WITH_PREFLIGHT()

        cfn_distribution.add_property_override(
            "DistributionConfig.DefaultCacheBehavior.ResponseHeadersPolicyId",
            response_headers_policy.response_headers_policy_id
        )

        self.bucket.add_to_resource_policy(iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[f"arn:aws:s3:::{self.bucket.bucket_name}/*"],
            principals=[iam.ServicePrincipal(
                f"cloudfront.amazonaws.com"
            )],
        ))
