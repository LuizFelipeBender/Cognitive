import os
import sys
from pathlib import Path
import cv2
import streamlit as st
from dotenv import load_dotenv
# Ajuste dos caminhos do projeto
project_root = os.path.abspath(os.path.join(os.getcwd(), '..'))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

dotenv_path = os.path.join(src_path, '.env')
print(f"Carregando .env de: {dotenv_path}")
load_dotenv(dotenv_path)
# Adiciona o diretório raiz do projeto ao PATH
project_root = Path(__file__).parent.parent.parent  # Ajuste conforme sua estrutura
sys.path.append(str(project_root))

# Carrega variáveis de ambiente
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path)

# Agora as importações devem funcionar
from src.aws_services import get_rekognition_client
from src.face_processing import extract_faces, compare_faces
from src.text_processing import extract_document_text

def image_to_bytes(image, ext='.jpg'):
    _, buffer = cv2.imencode(ext, image)
    return buffer.tobytes()

def main():
    st.title("Análise de Documento e Selfie com AWS Rekognition")

    doc_file = st.file_uploader("Envie a imagem do documento", type=["jpg", "jpeg", "png"])
    selfie_file = st.file_uploader("Envie a selfie", type=["jpg", "jpeg", "png"])

    if doc_file and selfie_file:
        # Carregar imagens com OpenCV
        doc_bytes = doc_file.read()
        selfie_bytes = selfie_file.read()

        doc_np = cv2.imdecode(np.frombuffer(doc_bytes, np.uint8), cv2.IMREAD_COLOR)
        selfie_np = cv2.imdecode(np.frombuffer(selfie_bytes, np.uint8), cv2.IMREAD_COLOR)

        # Mostrar imagens
        col1, col2 = st.columns(2)
        with col1:
            st.image(doc_np, caption="Documento", channels="BGR")
        with col2:
            st.image(selfie_np, caption="Selfie", channels="BGR")

        rekognition = get_rekognition_client()

        # Extração de faces
        doc_faces = extract_faces(image_to_bytes(doc_np), rekognition_client=rekognition)
        selfie_faces = extract_faces(image_to_bytes(selfie_np), rekognition_client=rekognition)

        if doc_faces and selfie_faces:
            similarity = compare_faces(doc_faces[0], selfie_faces[0], rekognition_client=rekognition, threshold=90)
            st.success(f"Similaridade: {similarity:.2f}%")
        else:
            st.error("Não foi possível detectar faces em uma das imagens.")

        # Extração de texto
        extracted_text = extract_document_text(image_to_bytes(doc_np))
        st.subheader("Texto extraído do documento:")
        for key, value in extracted_text.items():
            st.write(f"**{key}**: {value}")

if __name__ == "__main__":
    import numpy as np
    main()
