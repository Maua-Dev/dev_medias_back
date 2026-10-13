#!/usr/bin/env python3
import os

import aws_cdk as cdk

from adjust_layer_directory import adjust_layer_directory
from stack.iac_stack import IacStack

print("Starting the CDK")

print("Adjusting the layer directory")
adjust_layer_directory()
print("Finished adjusting the layer directory")


app = cdk.App()

aws_region = os.environ.get("AWS_REGION")
aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
stack_name = os.environ.get("STACK_NAME")
stack_generation = (os.environ.get("STACK_GENERATION") or "").strip().lower()

stage = os.environ.get("GITHUB_REF_NAME").capitalize()
stack_name = os.environ.get("STACK_NAME")

tags = {
    'project': 'DevMedias',
    'stage': stage,
    'stack': stack_name,
    'owner': 'DevCommunity',
    'generation': stack_generation or 'legacy',
}

IacStack(
    app, 
    stack_id=stack_name, 
    stack_name=stack_name,
    stage=stage,
    stack_generation=stack_generation,
    env=cdk.Environment(
        account=aws_account_id,
        region=aws_region
        ), 
    tags=tags
)

app.synth()
