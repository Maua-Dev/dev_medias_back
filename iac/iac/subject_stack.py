import os

from constructs import Construct
from aws_cdk import (
    aws_s3,
    RemovalPolicy,
    aws_iam as iam,
    aws_cloudfront,
    aws_cloudfront_origins,
    Stack
)
from aws_cdk import App


class SubjectStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.github_ref_name = os.environ.get("GITHUB_REF_NAME")
        self.aws_region = os.environ.get("AWS_REGION")
        self.aws_account_id = os.environ.get("AWS_ACCOUNT_ID")

        REMOVAL_POLICY = RemovalPolicy.RETAIN if 'prod' in self.github_ref_name else RemovalPolicy.DESTROY

        self.bucket = aws_s3.Bucket(self, "SubjectBucket", block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
                                    removal_policy=REMOVAL_POLICY)

        oac = aws_cloudfront.CfnOriginAccessControl(self, "OAC", origin_access_control_config={
            "name": f"DevMedias Subject Bucket OAC {self.github_ref_name}",
            "originAccessControlOriginType": "s3",
            "signingBehavior": "always",
            "signingProtocol": "sigv4"
        })

        cloudFrontWebDistribution = aws_cloudfront.Distribution(self, "CloudFrontWebDistribution",
                                                                default_behavior=aws_cloudfront.BehaviorOptions(
                                                                    origin=aws_cloudfront_origins.S3Origin(self.bucket),
                                                                    allowed_methods=aws_cloudfront.AllowedMethods.ALLOW_ALL,
                                                                    viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                                                    response_headers_policy=aws_cloudfront.ResponseHeadersPolicy.CORS_ALLOW_ALL_ORIGINS
                                                                ),
                                                                comment=f"DevMedias Subject S3 CDN {self.github_ref_name}",
                                                                price_class=aws_cloudfront.PriceClass.PRICE_CLASS_ALL,
                                                                default_root_object="index.html"
                                                                )

        cfn_distribution = cloudFrontWebDistribution.node.default_child
        cfn_distribution.add_property_override('DistributionConfig.Origins.0.OriginAccessControlId', oac.get_att('Id'))

        self.bucket.add_to_resource_policy(iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[f"arn:aws:s3:::{self.bucket.bucket_name}/*"],
            principals=[iam.ServicePrincipal(
                f"cloudfront.amazonaws.com"
            )],
        ))


app = App()
SubjectStack(app, "SubjectStack")
app.synth()