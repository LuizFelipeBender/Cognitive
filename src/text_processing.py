from aws_services import get_textract_client

def extract_document_text(image_bytes):
    """Extrai texto estruturado de um documento usando AWS Textract"""
    textract = get_textract_client()
    
    response = textract.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS']
    )
    
    # Mapear blocos por ID
    blocks = {block['Id']: block for block in response['Blocks']}
    
    key_map = {}
    value_map = {}
    kvs = {}

    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'KEY' in block['EntityTypes']:
                key_map[block['Id']] = block
            elif 'VALUE' in block['EntityTypes']:
                value_map[block['Id']] = block

    def get_text(block):
        text = ""
        if 'Relationships' in block:
            for rel in block['Relationships']:
                if rel['Type'] == 'CHILD':
                    for child_id in rel['Ids']:
                        word = blocks[child_id]
                        if word['BlockType'] == 'WORD':
                            text += word['Text'] + ' '
        return text.strip()

    for key_id, key_block in key_map.items():
        value_block = None
        for rel in key_block.get('Relationships', []):
            if rel['Type'] == 'VALUE':
                for value_id in rel['Ids']:
                    value_block = value_map.get(value_id)
        if value_block:
            key_text = get_text(key_block)
            value_text = get_text(value_block)
            kvs[key_text] = value_text

    return kvs

def validate_name(extracted_name, expected_name):
    """Valida se o nome extraído corresponde ao esperado"""
    return extracted_name.lower() == expected_name.lower()
