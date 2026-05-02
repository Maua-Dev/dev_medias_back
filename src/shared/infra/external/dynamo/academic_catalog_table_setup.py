"""
Cria a tabela single-table do catálogo acadêmico (pk + sk), se ainda não existir.

Usado pelo DynamoDB local (Docker) e pode ser importado pelos loaders em `iac/local/docker/dynamo/`.

Requer `Environments` configurado (ex.: `STAGE=TEST`, `ENDPOINT_URL`, opcionalmente `ENTITY_TABLE_NAME`).
"""

from __future__ import annotations

import os

import boto3

from src.shared.environments import Environments


def ensure_academic_catalog_table() -> str:
    """
    Garante que a tabela em `Environments.entity_table_name` exista
    (partition key `pk`, sort key `sk`).
    Retorna o nome da tabela.
    """
    envs = Environments.get_envs()
    table_name = envs.entity_table_name
    endpoint = envs.endpoint_url
    if not endpoint:
        raise RuntimeError("endpoint_url não configurado (ex.: ENDPOINT_URL=http://localhost:8000).")

    print(f"DynamoDB: tabela '{table_name}' em '{endpoint}' (região {envs.region})")

    client = boto3.client(
        "dynamodb",
        endpoint_url=endpoint,
        region_name=envs.region,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "local"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "local"),
    )

    existing = client.list_tables().get("TableNames", [])
    if table_name in existing:
        print(f"Tabela '{table_name}' já existe.")
        return table_name

    print(f"Criando tabela '{table_name}'...")
    client.create_table(
        TableName=table_name,
        BillingMode="PAY_PER_REQUEST",
        KeySchema=[
            {"AttributeName": "pk", "KeyType": "HASH"},
            {"AttributeName": "sk", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "pk", "AttributeType": "S"},
            {"AttributeName": "sk", "AttributeType": "S"},
        ],
    )
    client.get_waiter("table_exists").wait(TableName=table_name)
    print(f"Tabela '{table_name}' criada.")
    return table_name
