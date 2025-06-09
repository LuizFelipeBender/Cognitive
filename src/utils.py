import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import Union, Tuple

def display_image(image: np.ndarray, title: str = "Image", figsize: Tuple[int, int] = (8, 8)):
    """
    Exibe uma imagem usando matplotlib
    
    Args:
        image: Imagem no formato numpy array (BGR ou RGB)
        title: Título da imagem
        figsize: Tamanho da figura
    """
    plt.figure(figsize=figsize)
    if len(image.shape) == 3 and image.shape[2] == 3:  # Se for imagem colorida
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    else:  # Se for imagem em escala de cinza
        plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

def analyze_image_properties(image: np.ndarray) -> dict:
    """
    Analisa propriedades básicas de uma imagem
    
    Args:
        image: Imagem no formato numpy array
        
    Returns:
        Dicionário com propriedades da imagem
    """
    return {
        'shape': image.shape,
        'dtype': str(image.dtype),
        'min': float(image.min()),
        'max': float(image.max()),
        'mean': float(image.mean()),
        'std': float(image.std())
    }

def read_image(file_path: str) -> np.ndarray:
    """
    Lê uma imagem do disco em formato BGR
    
    Args:
        file_path: Caminho para o arquivo de imagem
        
    Returns:
        Imagem no formato numpy array (BGR)
    """
    return cv2.imread(file_path)

def prepare_image_for_aws(image: np.ndarray) -> bytes:
    """
    Prepara imagem para envio aos serviços AWS
    
    Args:
        image: Imagem no formato numpy array
        
    Returns:
        Bytes da imagem no formato JPEG
    """
    success, encoded_image = cv2.imencode('.jpg', image)
    if not success:
        raise ValueError("Falha ao codificar imagem")
    return encoded_image.tobytes()

def draw_bounding_boxes(image: np.ndarray, boxes: list, color: Tuple[int, int, int] = (0, 255, 0), thickness: int = 2) -> np.ndarray:
    """
    Desenha retângulos em uma imagem
    
    Args:
        image: Imagem original
        boxes: Lista de bounding boxes no formato [(x1, y1, x2, y2), ...]
        color: Cor do retângulo (BGR)
        thickness: Espessura da linha
        
    Returns:
        Imagem com os retângulos desenhados
    """
    img_with_boxes = image.copy()
    for box in boxes:
        x1, y1, x2, y2 = box
        cv2.rectangle(img_with_boxes, (x1, y1), (x2, y2), color, thickness)
    return img_with_boxes