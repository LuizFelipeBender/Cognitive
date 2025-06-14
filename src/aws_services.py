import boto3
import os
from dotenv import load_dotenv

# Caminho relativo ao arquivo atual (aws_services.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, '.env')

load_dotenv(dotenv_path)

def get_rekognition_client():
    return boto3.client(
        'rekognition',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

def get_textract_client():
    """
    Cria e retorna um cliente para o serviço Amazon Textract
    Requer variáveis de ambiente AWS configuradas
    """
    return boto3.client(
        'textract',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

def get_s3_client():
    """
    Cria e retorna um cliente para o serviço Amazon S3 (útil para armazenar imagens)
    """
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )