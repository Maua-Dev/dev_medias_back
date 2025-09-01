import json
import boto3
import urllib.parse
import os


def lambda_handler(event, context):
    """
    Função principal da Lambda que é acionada por um evento do S3.
    """
    print("Evento recebido:", json.dumps(event))

    