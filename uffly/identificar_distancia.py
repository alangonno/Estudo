
# -*- coding: utf-8 -*-
"""
Detector de Formas e Cores com Texto (acentuação via Pillow) + Estimativa/Filtro de Distância

Recursos:
- Formas: círculo, triângulo, quadrado, retângulo, pentágono, hexágono, polígonos
- Cores: HSV (vermelho, laranja, amarelo, verde, ciano, azul, púrpura, preto, branco, cinza)
- Texto com acentuação correta (Pillow)
- Estimativa de distância por visão monocular
- Filtro por distância (ex.: até 20 cm)
- Calibração da distância focal (automática por imagem ou tecla 'K' no modo câmera)

Autor: ANDRE + M365 Copilot
"""

import cv2
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont

# ==============================
# Configurações Gerais
# ==============================
USE_CAMERA = True                      # True para webcam; False para imagem
IMAGE_PATH = "exemplo_formas_cores.jpg" # caminho da imagem quando USE_CAMERA=False

# Detecção geométrica
AREA_MIN = 300                          # área mínima do contorno para ignorar ruído
CIRCULARITY_MIN = 0.89                  # limiar rigoroso para considerar "círculo"

# Desenho
THICKNESS = 2
COLOR_BOX = (0, 255, 0)
COLOR_CONTOUR = (255, 0, 0)
COLOR_TEXT = (255, 255, 255)

# Distância (visão monocular)
ATIVAR_FILTRO_DISTANCIA = True          # habilita/ desabilita filtro por distância
DISTANCIA_MAX_CM = 30.0                 # ex.: detectar apenas até 20 cm

# Tamanho REAL do objeto (em cm) para estimativa de distância
# - Se você souber tamanhos diferentes por forma, preencha aqui (opcional).
TAMANHO_PADRAO_OBJETO_CM = 5.0          # usado quando a forma não está no mapa abaixo
MAPA_TAMANHO_REAL_CM = {
    "círculo": 5.0,                     # diâmetro real (cm)
    "quadrado": 5.0,                    # lado real (cm)
    "retângulo": 6.0,                   # larg/alt média (ajuste conforme necessário)
    "triângulo": 5.0,                   # lado/altura característica (aproximação)
    "pentágono": 5.0,
    "hexágono": 5.0
}

# Distância focal (f) - defina após calibrar (ou deixe None e use a calibração integrada)
FOCAL_LENGTH = None                     # ex.: 720 após calibrar

# Calibração automática
CALIBRAR_AUTOMATICAMENTE = True         # calcula f a partir da primeira imagem com 1 objeto
CALIBRACAO_OBJETO_CM = 5.0              # tamanho real do objeto usado na calibração (cm)
CALIBRACAO_DISTANCIA_CM = 30.0          # distância conhecida do objeto à câmera (cm)

# ==============================
# Utilidades de Texto (Pillow)
# ==============================
def _carregar_fonte(tamanho: int = 26):
    """
    Tenta carregar uma fonte TrueType com suporte a acentos.
    Cai para default se não encontrar.
    """
    fontes_tentativas = [
        "arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/opentype/noto/NotoSans-Regular.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for caminho in fontes_tentativas:
        try:
            return ImageFont.truetype(caminho, tamanho)
        except:
            continue
    return ImageFont.load_default()

def escrever_texto_pillow(frame_bgr, texto, x, y, tamanho=26, cor=(255, 255, 255), stroke=2, stroke_cor=(0,0,0)):
    """
    Desenha texto com acentuação usando Pillow e retorna frame BGR novamente.
    """
    img_pil = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    fonte = _carregar_fonte(tamanho)

    # stroke melhora a legibilidade
    try:
        draw.text((x, y), texto, font=fonte, fill=cor, stroke_width=stroke, stroke_fill=stroke_cor)
    except TypeError:
        # versões antigas do Pillow podem não suportar stroke_*; desenha sem stroke
        draw.text((x, y), texto, font=fonte, fill=cor)

    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

# ==============================
# Geometria (classificação de forma)
# ==============================
def classificar_forma(contorno):
    """
    Classifica a forma a partir do contorno:
    - Primeiro conta vértices (approxPolyDP)
    - Depois valida círculo por circularidade >= CIRCULARITY_MIN
    """
    perimetro = cv2.arcLength(contorno, True)
    if perimetro == 0:
        return "indefinido"

    area = cv2.contourArea(contorno)
    if area < AREA_MIN:
        return None

    # Circularidade (próximo de 1 -> círculo)
    circularidade = (4 * math.pi * area) / (perimetro * perimetro)

    # Aproximação poligonal — ligeiramente mais sensível do que 0.02
    epsilon = 0.015 * perimetro
    approx = cv2.approxPolyDP(contorno, epsilon, True)
    vertices = len(approx)

    # Polígonos por vértices
    if vertices == 3:
        return "triângulo"
    if vertices == 4:
        x, y, w, h = cv2.boundingRect(approx)
        razao = (w / float(h)) if h != 0 else 0
        return "quadrado" if 0.93 <= razao <= 1.07 else "retângulo"
    if vertices == 5:
        return "pentágono"
    if vertices == 6:
        return "hexágono"

    # Verificação final de círculo (após poligonal)
    if circularidade >= CIRCULARITY_MIN:
        return "círculo"

    return f"polígono ({vertices} lados)"

# ==============================
# Cor (HSV)
# ==============================
def nome_cor_por_hsv(h, s, v):
    # Acromáticos
    if v < 50:
        return "preto"
    if s < 35 and v > 200:
        return "branco"
    if s < 35:
        return "cinza"

    # Matiz (Hue) em OpenCV é [0..179]
    if (0 <= h <= 10) or (160 <= h <= 179):
        return "vermelho"
    elif 11 <= h <= 25:
        return "laranja"
    elif 26 <= h <= 35:
        return "amarelo"
    elif 36 <= h <= 85:
        return "verde"
    elif 86 <= h <= 100:
        return "ciano"
    elif 101 <= h <= 130:
        return "azul"
    elif 131 <= h <= 159:
        return "púrpura"
    return "cor desconhecida"

def classificar_cor(frame_bgr, contorno):
    mask = np.zeros(frame_bgr.shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [contorno], -1, 255, thickness=cv2.FILLED)
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    mean_h, mean_s, mean_v, _ = cv2.mean(hsv, mask=mask)
    return nome_cor_por_hsv(int(mean_h), int(mean_s), int(mean_v))

# ==============================
# Distância (visão monocular)
# ==============================
def tamanho_px_para_distancia_cm(tamanho_real_cm, tamanho_px, focal):
    """
    distância = (tamanho_real * focal) / tamanho_px
    """
    if tamanho_px <= 0 or focal is None:
        return None
    return (tamanho_real_cm * focal) / float(tamanho_px)

def calcular_focal_length(tamanho_real_cm, distancia_real_cm, tamanho_px):
    """
    f = (tamanho_px * distancia_real) / tamanho_real
    """
    if tamanho_real_cm <= 0 or distancia_real_cm <= 0 or tamanho_px <= 0:
        return None
    return (tamanho_px * distancia_real_cm) / float(tamanho_real_cm)

def obter_tamanho_real_da_forma(forma: str):
    return MAPA_TAMANHO_REAL_CM.get(forma, TAMANHO_PADRAO_OBJETO_CM)

def estimar_tamanho_px(contorno, forma):
    """
    Tamanho característico em pixels:
    - círculo: diâmetro pelo menor círculo envolvente
    - demais: maior dimensão da bounding box (max(w, h))
    """
    if forma == "círculo":
        (x, y), r = cv2.minEnclosingCircle(contorno)
        return 2.0 * r
    x, y, w, h = cv2.boundingRect(contorno)
    return float(max(w, h))

# ==============================
# Pipeline de processamento
# ==============================
def processar_frame(frame, focal_length_state):
    """
    Retorna:
      - frame anotado (com texto por Pillow)
      - focal_length_state (pode ser atualizado por calibração automática)
    """
    borrada = cv2.GaussianBlur(frame, (5, 5), 0)
    cinza = cv2.cvtColor(borrada, cv2.COLOR_BGR2GRAY)
    bordas = cv2.Canny(cinza, 50, 150)

    kernel = np.ones((3, 3), np.uint8)
    bordas = cv2.morphologyEx(bordas, cv2.MORPH_CLOSE, kernel, iterations=2)

    contornos, _ = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    saida = frame.copy()

    # Para calibração automática com 1º objeto
    focal_atual = focal_length_state

    # Ordena por área (maior primeiro) — útil para calibração e estabilidade
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)

    for idx, cnt in enumerate(contornos):
        area = cv2.contourArea(cnt)
        if area < AREA_MIN:
            continue

        forma = classificar_forma(cnt)
        if forma is None:
            continue

        cor_nome = classificar_cor(frame, cnt)

        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(saida, (x, y), (x + w, y + h), COLOR_BOX, THICKNESS)
        cv2.drawContours(saida, [cnt], -1, COLOR_CONTOUR, 2)

        # ----- Distância -----
        tamanho_px = estimar_tamanho_px(cnt, forma)
        tamanho_real_cm = obter_tamanho_real_da_forma(forma)

        # Calibração automática (uma vez) na primeira detecção
        if focal_atual is None and CALIBRAR_AUTOMATICAMENTE:
            focal_calc = calcular_focal_length(
                tamanho_real_cm=CALIBRACAO_OBJETO_CM,
                distancia_real_cm=CALIBRACAO_DISTANCIA_CM,
                tamanho_px=tamanho_px
            )
            if focal_calc is not None and focal_calc > 0:
                focal_atual = float(focal_calc)
                # informa no frame
                saida = escrever_texto_pillow(
                    saida,
                    f"Focal calibrada: {focal_atual:.1f}",
                    10, 10, tamanho=24, cor=(255,255,0)
                )

        distancia_cm = tamanho_px_para_distancia_cm(tamanho_real_cm, tamanho_px, focal_atual)

        # Filtro por distância (se ativado e se temos focal)
        if ATIVAR_FILTRO_DISTANCIA and focal_atual is not None and distancia_cm is not None:
            if distancia_cm > DISTANCIA_MAX_CM:
                # Desenha um rótulo discreto e ignora o restante
                # saida = escrever_texto_pillow(
                #     saida, "fora do alcance", x, y - 28, tamanho=22, cor=(255, 200, 200)
                # )
                continue

        # ----- Rótulos -----
        base_label = f"{forma}, {cor_nome}"
        saida = escrever_texto_pillow(saida, base_label, x, y - 28, tamanho=26, cor=COLOR_TEXT)

        if distancia_cm is not None:
            saida = escrever_texto_pillow(
                saida, f"{distancia_cm:.1f} cm", x, y - 56, tamanho=22, cor=(200,255,200)
            )
        else:
            # dica de calibração quando não houver focal
            saida = escrever_texto_pillow(
                saida, "Pressione 'K' para calibrar", x, y - 56, tamanho=20, cor=(255,255,0)
            )

    return saida, focal_atual

# ==============================
# Laços principais (câmera ou imagem)
# ==============================
def loop_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Não foi possível acessar a câmera.")
        return

    print("Controles: 'q' para sair | 'k' para calibrar focal com objeto atual")
    focal_state = FOCAL_LENGTH

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        anotado, focal_state = processar_frame(frame, focal_state)
        # Overlay com status
        info = f"focal={focal_state:.1f}" if focal_state is not None else "focal=N/A"
        anotado = escrever_texto_pillow(anotado, info, 10, 40, tamanho=22, cor=(180, 255, 180))

        cv2.imshow("Detecção de Formas e Cores (Cam)", anotado)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('k'):
            # Calibração manual pelo maior contorno do frame atual
            # Reprocessa rapidamente para obter maior contorno e calcular focal
            borrada = cv2.GaussianBlur(frame, (5, 5), 0)
            cinza = cv2.cvtColor(borrada, cv2.COLOR_BGR2GRAY)
            bordas = cv2.Canny(cinza, 50, 150)
            kernel = np.ones((3, 3), np.uint8)
            bordas = cv2.morphologyEx(bordas, cv2.MORPH_CLOSE, kernel, iterations=2)
            conts, _ = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if conts:
                conts = sorted(conts, key=cv2.contourArea, reverse=True)
                cnt0 = conts[0]
                forma0 = classificar_forma(cnt0)
                if forma0 is not None:
                    tam_px0 = estimar_tamanho_px(cnt0, forma0)
                    # usa valores de calibração definidos no topo
                    foc = calcular_focal_length(CALIBRACAO_OBJETO_CM, CALIBRACAO_DISTANCIA_CM, tam_px0)
                    if foc is not None and foc > 0:
                        focal_state = float(foc)
                        print(f"[Calibração] Focal atualizada para: {focal_state:.2f}")

    cap.release()
    cv2.destroyAllWindows()

def processar_imagem():
    frame = cv2.imread(IMAGE_PATH)
    if frame is None:
        print(f"Falha ao carregar a imagem: {IMAGE_PATH}")
        return

    focal_state = FOCAL_LENGTH
    anotado, focal_state = processar_frame(frame, focal_state)

    # Exibe informações adicionais no topo
    info1 = f"focal={focal_state:.1f}" if focal_state is not None else "focal=N/A"
    info2 = f"Filtro distância: até {DISTANCIA_MAX_CM:.0f} cm" if ATIVAR_FILTRO_DISTANCIA else "Filtro distância: off"
    anotado = escrever_texto_pillow(anotado, info1, 10, 10, tamanho=22, cor=(180, 255, 180))
    anotado = escrever_texto_pillow(anotado, info2, 10, 40, tamanho=22, cor=(180, 255, 180))

    cv2.imshow("Detecção de Formas e Cores (Imagem)", anotado)
    print("Feche a janela para sair.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# ==============================
# Entrada do Programa
# ==============================
def main():
    if USE_CAMERA:
        loop_camera()
    else:
        processar_imagem()

if __name__ == "__main__":
    main()
