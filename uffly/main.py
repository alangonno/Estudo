
import cv2
import numpy as np
import math
import pytesseract
import os

# ==============================
# Configurações do usuário
# ==============================
USE_CAMERA = True            # True para webcam/stream, False para imagem
IMAGE_PATH = "bouncing.png"   # <- caminho do seu anexo
VIDEO_SOURCE = 0              # índice de câmera ou URL (RTSP/UDP/MJPEG)
TEMPLATE_GABARITO_PATH = ""   # opcional: caminho para recorte do ícone "gabarito" (PNG/JPG)

# Parâmetros de detecção
AREA_MIN_TOKEN = 1500          # área mínima para tokens
CIRC_TOKEN_MIN = 0.80          # circularidade mínima para considerar um token circular branco
CIRC_BASE_MIN  = 0.80          # circularidade mínima para a base
BLUE_HSV_RANGE = ((100, 90, 40), (140, 255, 255))  # faixa de azul (ajuste conforme a sua câmera)

# OCR (Tesseract) - reconhecer apenas dígitos, um único caractere
TESS_CONFIG = r'--oem 3 --psm 10 -c tessedit_char_whitelist=0123456789'

# Fonte para overlays
FONT = cv2.FONT_HERSHEY_SIMPLEX

# ==============================
# Utilidades
# ==============================
def circularidade(cnt):
    per = cv2.arcLength(cnt, True)
    if per == 0:
        return 0
    area = cv2.contourArea(cnt)
    return (4 * math.pi * area) / (per * per)

def binarizar_roi(roi_gray):
    # equaliza e aplica binarização adaptativa para contornos nítidos
    eq = cv2.equalizeHist(roi_gray)
    bin_img = cv2.adaptiveThreshold(eq, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY_INV, 31, 5)
    return bin_img

def classificar_forma_interna(roi_bin):
    """
    Retorna (nome_forma, contorno_escolhido)
    Heurísticas:
      - Triângulo: 3 vértices
      - Quadrilátero: 4 vértices
      - Pentágono/Hexágono: 5/6 vértices
      - Estrela: polígono não convexo com muitos picos (vértices >= 8) e área << area do hull
    """
    contours, _ = cv2.findContours(roi_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None

    # Pega o maior contorno (forma interna desenhada)
    cnt = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(cnt)
    if area < 100:  # ruído
        return None, None

    per = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * per, True)
    vertices = len(approx)

    # Estrela: não convexa + muitos vértices + área bem menor que o casco convexo
    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull) if hull is not None else 0
    non_convex = not cv2.isContourConvex(approx)
    star_like = (vertices >= 8) and non_convex
    area_ratio = (area / hull_area) if hull_area > 0 else 1.0

    if star_like and area_ratio < 0.8:
        return "estrela", cnt

    if vertices == 3:
        return "triângulo", cnt
    elif vertices == 4:
        # quadrado/retângulo (mas no seu layout não é o foco)
        x, y, w, h = cv2.boundingRect(approx)
        ratio = w / float(h) if h > 0 else 0
        if 0.93 <= ratio <= 1.07:
            return "quadrado", cnt
        else:
            return "retângulo", cnt
    elif vertices == 5:
        return "pentágono", cnt
    elif vertices == 6:
        return "hexágono", cnt
    elif vertices >= 7:
        return f"polígono ({vertices} lados)", cnt
    else:
        # forma muito irregular
        return "forma", cnt

def ocr_digito(roi_gray):
    """
    Extrai um único dígito usando Tesseract configurado para 0–9.
    Pré-processa com limiar adaptativo e pequenas morfologias.
    Retorna string com 1 caractere ou ''.
    """
    # Inverte para o Tesseract (preto no branco)
    _, bin_inv = cv2.threshold(roi_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Como o desenho é preto no branco, queremos números pretos → invertido = bom
    # Mas o Tesseract costuma preferir texto escuro em fundo claro: 
    # Se precisar, remova a inversão (teste nos seus dados).
    try:
        txt = pytesseract.image_to_string(bin_inv, config=TESS_CONFIG).strip()
    except Exception as e:
        return ""
    # Mantém somente um dígito, se houver
    for ch in txt:
        if ch.isdigit():
            return ch
    return ""

def template_match_gabarito(roi_gray, template_path, thr=0.6):
    """
    Faz template matching do ícone 'gabarito' dentro do ROI (grayscale).
    Retorna score máximo (0..1) e posição; se template não existir, retorna (0, None).
    """
    if not template_path or not os.path.exists(template_path):
        return 0.0, None
    tpl = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if tpl is None:
        return 0.0, None
    # Normaliza tamanhos aproximando o template ao ROI
    # (opcionalmente, teste multi-escala se necessário)
    method = cv2.TM_CCOEFF_NORMED
    res = cv2.matchTemplate(roi_gray, tpl, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val >= thr:
        return float(max_val), max_loc
    return float(max_val), None

def detectar_base_azul(frame_bgr):
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    (h1, s1, v1), (h2, s2, v2) = BLUE_HSV_RANGE
    mask = cv2.inRange(hsv, (h1, s1, v1), (h2, s2, v2))
    # Limpeza
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, mask

    # maior área
    cnt = max(contours, key=cv2.contourArea)
    if cv2.contourArea(cnt) < 1000:
        return None, mask

    circ = circularidade(cnt)
    if circ < CIRC_BASE_MIN:
        return None, mask

    M = cv2.moments(cnt)
    cx = int(M["m10"] / M["m00"]) if M["m00"] != 0 else 0
    cy = int(M["m01"] / M["m00"]) if M["m00"] != 0 else 0
    x, y, w, h = cv2.boundingRect(cnt)

    return {
        "tipo": "base_azul",
        "centro": (cx, cy),
        "bbox": (x, y, w, h),
        "contorno": cnt
    }, mask

def processar_frame(frame):
    """
    1) Detecta tokens circulares (brancos)
    2) Para cada token, classifica forma interna e lê dígito
    3) Detecta base azul
    Retorna frame anotado e uma lista de detecções
    """
    saida = frame.copy()
    detecoes = []

    # --------------------------
    # 0) Base azul
    # --------------------------
    base_info, _mask_blue = detectar_base_azul(frame)
    if base_info:
        x, y, w, h = base_info["bbox"]
        cv2.rectangle(saida, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(saida, "base de decolagem", (x, y - 8), FONT, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.drawContours(saida, [base_info["contorno"]], -1, (255, 0, 0), 2)
        detecoes.append({"tipo": "base_azul", "centro": base_info["centro"]})

    # --------------------------
    # 1) Tokens circulares
    # --------------------------
    # Aproxima por "círculo branco" usando limiar por brilho + contorno + circularidade
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # fundo é cinza; discos são brancos: usa limiar alto
    _, th = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    kernel = np.ones((3, 3), np.uint8)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=1)
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < AREA_MIN_TOKEN:
            continue

        circ = circularidade(cnt)
        if circ < CIRC_TOKEN_MIN:
            continue  # não é circular o suficiente

        x, y, w, h = cv2.boundingRect(cnt)
        # expande um pouco para garantir a borda interna
        pad = int(0.04 * max(w, h))
        x0 = max(x - pad, 0)
        y0 = max(y - pad, 0)
        x1 = min(x + w + pad, frame.shape[1])
        y1 = min(y + h + pad, frame.shape[0])

        roi = frame[y0:y1, x0:x1]
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi_bin = binarizar_roi(roi_gray)

        # 1.1) Classificar forma interna
        forma, cnt_int = classificar_forma_interna(roi_bin)

        # 1.2) Ler dígito (OCR)
        dig = ocr_digito(roi_gray)

        # 1.3) (Opcional) gabarito via template
        gab_score, gab_loc = template_match_gabarito(roi_gray, TEMPLATE_GABARITO_PATH, thr=0.6)
        is_gabarito = gab_score >= 0.6

        label_partes = []
        if forma:
            label_partes.append(forma)
        if dig:
            label_partes.append(f"n={dig}")
        if is_gabarito:
            label_partes.append("gabarito")

        label = ", ".join(label_partes) if label_partes else "token"

        # Desenhos
        cv2.rectangle(saida, (x0, y0), (x1, y1), (0, 255, 0), 2)
        cv2.putText(saida, label, (x0, y0 - 8), FONT, 0.6, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(saida, label, (x0, y0 - 8), FONT, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

        if cnt_int is not None:
            cnt_shifted = cnt_int + np.array([[x0, y0]])
            cv2.drawContours(saida, [cnt_shifted], -1, (0, 255, 255), 2)

        det_info = {
            "tipo": "token",
            "bbox": (x0, y0, x1 - x0, y1 - y0),
            "forma": forma if forma else "",
            "digito": dig,
            "gabarito": bool(is_gabarito),
        }
        detecoes.append(det_info)

    return saida, detecoes

# ==============================
# Execução
# ==============================
def loop_de_video(capture):
    if not capture.isOpened():
        print("Não foi possível abrir a fonte de vídeo.")
        return

    print("Pressione 'q' para sair.")
    while True:
        ret, frame = capture.read()
        if not ret:
            print("Falha ao ler frame.")
            break

        anotado, dets = processar_frame(frame)
        cv2.imshow("Reconhecimento (formas e dígitos)", anotado)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

def main():
    if USE_CAMERA:
        cap = cv2.VideoCapture(VIDEO_SOURCE, cv2.CAP_ANY)
        # Você pode tentar reduzir latência:
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        cap.set(cv2.CAP_PROP_FPS, 30)
        loop_de_video(cap)
    else:
        frame = cv2.imread(IMAGE_PATH)
        if frame is None:
            print(f"Falha ao carregar imagem: {IMAGE_PATH}")
            return
        anotado, dets = processar_frame(frame)
        print("Detecções:", dets)
        cv2.imshow("Resultado", anotado)
        print("Feche a janela para terminar.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
