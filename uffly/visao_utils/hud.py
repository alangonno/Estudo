import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def escrever_texto_pillow(frame_bgr, texto, x, y, tamanho=24, cor=(255, 255, 255), stroke=0, stroke_cor=(0, 0, 0)):
    """
    Desenha texto em um frame OpenCV utilizando a biblioteca Pillow.
    Isso permite usar fontes TTF completas e suporta acentuação (diferente do cv2.putText).
    
    Argumentos:
        frame_bgr: array numpy (imagem OpenCV).
        texto: string a ser desenhada.
        x, y: coordenadas do canto superior esquerdo do texto.
        tamanho: tamanho da fonte.
        cor: tupla BGR com a cor do texto.
        stroke: espessura do contorno do texto.
        stroke_cor: tupla BGR com a cor do contorno.
        
    Retorna:
        array numpy (imagem OpenCV) com o texto desenhado.
    """
    img_pil = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    
    try:
        fonte = ImageFont.truetype("arial.ttf", tamanho)
    except IOError:
        # Fallback caso a fonte não exista no sistema
        fonte = ImageFont.load_default()
        
    cor_rgb = (cor[2], cor[1], cor[0]) if len(cor) == 3 else cor
    str_rgb = (stroke_cor[2], stroke_cor[1], stroke_cor[0]) if stroke > 0 and len(stroke_cor) == 3 else stroke_cor

    # Desenha o contorno se stroke > 0
    if stroke > 0:
        for dx in range(-stroke, stroke + 1):
            for dy in range(-stroke, stroke + 1):
                if dx == 0 and dy == 0:
                    continue
                draw.text((x + dx, y + dy), texto, font=fonte, fill=str_rgb)

    # Texto principal
    draw.text((x, y), texto, font=fonte, fill=cor_rgb)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def interagir_hub_principal(frame, texto, ancora_x, ancora_y, cor_fonte=(255, 255, 0)):
    """
    Auxiliar encapsulado do HUD para manter a compatibilidade do leitor_aruco_isolado
    sem espalhar números mágicos de formatação por todo canto.
    """
    return escrever_texto_pillow(
        frame_bgr=frame, 
        texto=texto, 
        x=ancora_x, 
        y=ancora_y, 
        tamanho=24, 
        cor=cor_fonte, 
        stroke=2, stroke_cor=(0, 0, 0)
    )
