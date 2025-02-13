

import fitz  # PyMuPDF

def extract_text_with_positions(file_path):
    doc = fitz.open(file_path)
    extracted_data = []

    # Processar o PDF página por página
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Extração de texto simples da página
        text = page.get_text("text")
        
        # Se você precisa das informações com posição, usa o formato "dict"
    for block in page.get_text("dict")["blocks"]:  # Obtém blocos de texto no formato de dicionário
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        x0, y0, x1, y1 = span["bbox"]  # Coordenadas
                        text = span["text"]  # Texto
                        fontsize = span["size"]  # Tamanho da fonte
                        font = span["font"]  # Nome da fonte (por exemplo, "Helvetica", "Arial", etc.)
                        color = span["color"]  # Cor do texto (em formato RGB)
                        rotation = span.get("angle", 0)  # Captura a rotação do texto
                        extracted_data.append({
                            "page": page_num,
                            "text": text.strip(),
                            "pos": (x0, y0, x1, y1),
                            "fontsize": fontsize,
                            "font": font,
                            "color": color,
                            "rotation": rotation  # Inclui a rotação do texto
                        })
    
    return extracted_data
