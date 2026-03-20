
import cv2
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont

# ==============================
# Configurações
# ==============================
USE_CAMERA = True                    # True para webcam; False para imagem
IMAGE_PATH = "exemplo_formas_cores.jpg"

AREA_MIN = 300                        # área mínima do contorno
CIRCULARITY_MIN = 0.89                # limiar mais rigoroso p/ círculo

THICKNESS = 2
COLOR_BOX = (0, 255, 0)
COLOR_CONTOUR = (255, 0, 0)
COLOR_TEXT = (255, 255, 255)

# ==============================
# Função Pillow p/ texto com acentuação
# ==============================
def escrever_texto_pillow(frame, texto, x, y, tamanho=26, cor=(255,255,255)):
    # Converte BGR -> RGB
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    # Usa fonte TrueType (Arial ou similar)
    try:
        fonte = ImageFont.truetype("arial.ttf", tamanho)
    except:
        fonte = ImageFont.load_default()

    draw.text((x, y), texto, font=fonte, fill=cor)

    # Converte RGB -> BGR p/ OpenCV
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

# ==============================
# Classificação de forma
# ==============================
def classificar_forma(contorno):
    perimetro = cv2.arcLength(contorno, True)
    if perimetro == 0:
        return "indefinido"

    area = cv2.contourArea(contorno)
    if area < AREA_MIN:
        return None

    # Circularidade
    circularidade = (4 * math.pi * area) / (perimetro * perimetro)

    # Aproximação poligonal
    epsilon = 0.015 * perimetro
    approx = cv2.approxPolyDP(contorno, epsilon, True)
    vertices = len(approx)

    # Triângulo
    if vertices == 3:
        return "triângulo"

    # Quadrado ou retângulo
    if vertices == 4:
        x, y, w, h = cv2.boundingRect(approx)
        razao = w / float(h)
        if 0.93 <= razao <= 1.07:
            return "quadrado"
        else:
            return "retângulo"

    # Pentágono
    if vertices == 5:
        return "pentágono"

    # Hexágono
    if vertices == 6:
        return "hexágono"

    # Círculo REAL (última checagem!)
    if circularidade >= CIRCULARITY_MIN:
        return "círculo"

    # Outras formas
    return f"polígono ({vertices} lados)"

# ==============================
# Classificação de cor
# ==============================
def nome_cor_por_hsv(h, s, v):
    if v < 50:
        return "preto"
    if s < 35 and v > 200:
        return "branco"
    if s < 35:
        return "cinza"

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
# Processamento do frame
# ==============================
def processar_frame(frame):
    borrada = cv2.GaussianBlur(frame, (5, 5), 0)
    cinza = cv2.cvtColor(borrada, cv2.COLOR_BGR2GRAY)
    bordas = cv2.Canny(cinza, 50, 150)

    kernel = np.ones((3, 3), np.uint8)
    bordas = cv2.morphologyEx(bordas, cv2.MORPH_CLOSE, kernel, iterations=2)

    contornos, _ = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    saida = frame.copy()

    for cnt in contornos:
        area = cv2.contourArea(cnt)
        if area < AREA_MIN:
            continue

        forma = classificar_forma(cnt)
        if forma is None:
            continue

        cor_nome = classificar_cor(frame, cnt)

        x, y, w, h = cv2.boundingRect(cnt)

        cv2.rectangle(saida, (x, y), (x + w, y + h), COLOR_BOX, THICKNESS)

        texto = f"{forma}, {cor_nome}"

        # >>> Texto com acentuação OK via Pillow <<<
        saida = escrever_texto_pillow(saida, texto, x, y - 28, tamanho=26, cor=(255,255,255))

        cv2.drawContours(saida, [cnt], -1, COLOR_CONTOUR, 2)

    return saida

# ==============================
# Execução principal
# ==============================
def main():
    if USE_CAMERA:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Não foi possível acessar a câmera.")
            return

        print("Pressione 'q' para sair.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            anotado = processar_frame(frame)
            cv2.imshow("Detecção de Formas e Cores", anotado)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    else:
        frame = cv2.imread(IMAGE_PATH)
        if frame is None:
            print("Falha ao carregar imagem!")
            return

        anotado = processar_frame(frame)
        cv2.imshow("Detecção de Formas e Cores", anotado)
        print("Feche a janela para sair.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# ==============================
# Entrada do programa
# ==============================
if __name__ == "__main__":
    main()
