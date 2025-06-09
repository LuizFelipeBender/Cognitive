"""
Pacote principal do sistema de validação de documentos

Módulos:
- aws_services: Configuração dos clientes AWS
- face_processing: Processamento e comparação facial
- text_processing: Extração e validação de texto
- utils: Funções auxiliares
"""

# Importações principais para facilitar o acesso
from .aws_services import get_rekognition_client, get_textract_client
from .face_processing import extract_faces, compare_faces
from .text_processing import extract_document_text, validate_name

# Versão do pacote
__version__ = '1.0.0'

# Exporta apenas o que deve ser acessível externamente
__all__ = [
    'get_rekognition_client',
    'get_textract_client',
    'extract_faces',
    'compare_faces',
    'extract_document_text',
    'validate_name'
]