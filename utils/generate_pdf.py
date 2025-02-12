import fitz  # PyMuPDF
import matplotlib.font_manager as fm

def normalize_color(color):
    # Se a cor for um valor inteiro no formato RGB
    if isinstance(color, int):
        # Extraímos as componentes R, G e B do valor inteiro (24 bits)
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        # Retorna os valores normalizados
        return (r / 255, g / 255, b / 255)
    
    # Se a cor for uma tupla RGB ou RGBA
    elif isinstance(color, tuple) and len(color) == 3:
        return (color[0] / 255, color[1] / 255, color[2] / 255)
    elif isinstance(color, tuple) and (len(color) == 4 or len(color) == 3):
        return color

    # Caso a cor não seja reconhecida, retorna preto
    return (0, 0, 0)  # Preto como fallback


def get_valid_font(original_font):
    available_fonts = [f.name for f in fm.fontManager.ttflist]

    if original_font in available_fonts:
        return original_font  # A fonte original está disponível
    else:
        print(f"⚠️ Fonte '{original_font}' não encontrada. Usando uma alternativa...")
        return "helvetica"  # Defina uma fonte substituta

def split_text_into_lines(text, max_width, max_height, fontsize, fontname):
    """Divide o texto em múltiplas linhas, ajustando dinamicamente a fonte se necessário."""
    font = fitz.Font(fontname=fontname)  
    lines = []
    current_line = ""
    
    while True:  # Loop para tentar ajustar a fonte caso o texto não caiba
        lines.clear()
        current_line = ""
        y_used = 0  # Altura total usada pelas linhas

        for word in text.split(' '):
            test_line = current_line + (" " if current_line else "") + word
            width = font.text_length(test_line, fontsize=fontsize)

            if width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                y_used += fontsize * 1.2  # Considera um espaço entre linhas
                current_line = word

        if current_line:
            lines.append(current_line)
            y_used += fontsize * 1.2  

        if y_used <= max_height:
            break  # Se couber no espaço disponível, finaliza
        else:
            fontsize *= 0.9  # Reduz a fonte em 10% para tentar encaixar
    
    return lines, fontsize

def replace_text_in_pdf(input_pdf, translated_blocks, output_pdf):
    doc = fitz.open(input_pdf)

    for block in translated_blocks:
        page = doc[block["page"]]
        x0, y0, x1, y1 = block["pos"]
        fontsize = block["fontsize"]
        fontname = get_valid_font(block["font"])  
        color = normalize_color(block["color"]) 


        max_width = x1 - x0
        max_height = y1 - y0  

        translated_text = block.get("text", "") or ""

         # Captura a cor de fundo original
        background_color = page.get_pixmap(clip=(x0, y0, x1, y1)).samples[:3]
        background_color = tuple(c / 255 for c in background_color)  # Normaliza de 0-255 para 0-1

        # Divide o texto respeitando a área disponível
        lines, adjusted_fontsize = split_text_into_lines(translated_text, max_width, max_height, fontsize, fontname)

        # Apaga o texto original
        page.draw_rect([x0, y0, x1, y1], color=background_color, fill=background_color)

        # Captura a rotação do texto (não da página)
        rotation = block["rotation"]  # Pega a rotação do texto (em graus)

        print(f"⚠️ Rotation do texto '{rotation}'")

         # Aplica a rotação apenas se o valor for diferente de 0
        if rotation != 0:
            text_matrix = fitz.Matrix(1, 0, 0, 1, 0, 0).pre_rotate(rotation)  # Aplica a rotação ao texto
        else:
            text_matrix = fitz.Matrix(1, 0, 0, 1, 0, 0)  # Sem rotação

         # Insere o texto ajustado mantendo a rotação
        y_offset = y0
        for line in lines:
            point = fitz.Point(x0, y_offset)
            transformed_point = point * text_matrix
            page.insert_text(
                transformed_point, 
                line, 
                fontsize=adjusted_fontsize, 
                color=color, 
                fontname=fontname
            )
            y_offset += adjusted_fontsize * 1.2  # Adiciona espaçamento entre as linhas

    doc.save(output_pdf)
