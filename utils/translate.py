from deep_translator import GoogleTranslator

def translate_texts(text_blocks, target_lang="pt"):
    translated_blocks = []
    
    for block in text_blocks:
        # Realiza a tradução
        translated_text = GoogleTranslator(source='auto', target=target_lang).translate(block["text"])
        
        # Exibe a tradução de cada bloco
        print(f"Original text: {block['text']}")
        print(f"Translated text: {translated_text}")
        
        # Adiciona o bloco traduzido à lista
        translated_blocks.append({
            "page": block["page"],
            "text": translated_text,
            "pos": block["pos"],
            "fontsize": block["fontsize"], 
            "font": block["font"],          
            "color": block["color"],
            "rotation": block["rotation"] 
        })
    
    return translated_blocks
