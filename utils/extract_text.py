import fitz  # PyMuPDF

def extract_text_with_positions(pdf_path):
    doc = fitz.open(pdf_path)
    extracted_data = []

    for page_num, page in enumerate(doc):
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
