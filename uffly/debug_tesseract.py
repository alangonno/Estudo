# -*- coding: utf-8 -*-
"""
DEBUG ISOLADO: Tesseract OCR para Dígitos (3, 4, 5)
----------------------------------------------------
Este arquivo existe SOMENTE para depurar o pipeline de OCR.
Ele exibe janelas separadas para cada etapa do processamento,
permitindo ver exatamente onde o Tesseract falha.

Janelas exibidas:
- "1 - Frame Original": imagem crua da câmera
- "2 - Segmentada": resultado do adaptiveThreshold
- "3 - ROI Interna": recorte central do maior contorno encontrado
- "4 - Binarizada (Otsu)": o que o Tesseract realmente recebe
- Console: print do texto bruto retornado pelo Tesseract a cada frame
"""

import cv2
import numpy as np
import pytesseract

# ============================================================================
# CONFIGS DO TESSERACT (teste diferentes combinações aqui)
# ============================================================================

# psm 6 = bloco de texto | psm 10 = caractere unico | psm 13 = raw line
# Teste trocar entre eles para ver qual funciona melhor
TESSERACT_PSM = 6
TESSERACT_WHITELIST = '345'
_CONFIG = f'--oem 3 --psm {TESSERACT_PSM} -c tessedit_char_whitelist={TESSERACT_WHITELIST}'

# Filtros de contorno (mesmos do leitor_bases_isolado.py)
AREA_MIN = 2000
AREA_MAX = 200_000
SOLIDITY_MIN = 0.70


def segmentar(frame):
    """AdaptiveThreshold para isolar bordas localmente."""
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    borrada = cv2.GaussianBlur(cinza, (5, 5), 0)
    segmentada = cv2.adaptiveThreshold(
        borrada, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=31, C=4
    )
    kernel = np.ones((3, 3), np.uint8)
    return cv2.morphologyEx(segmentada, cv2.MORPH_CLOSE, kernel, iterations=2)


def encontrar_maior_contorno_valido(segmentada):
    """Retorna o maior contorno que passa nos filtros de área e solidez."""
    contornos, _ = cv2.findContours(segmentada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    melhor = None
    melhor_area = 0
    
    for cnt in contornos:
        area = cv2.contourArea(cnt)
        if not (AREA_MIN <= area <= AREA_MAX):
            continue
            
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        if hull_area <= 0:
            continue
        solidity = area / hull_area
        if solidity < SOLIDITY_MIN:
            continue
            
        if area > melhor_area:
            melhor_area = area
            melhor = cnt
    
    return melhor


def extrair_roi_interna(frame, contorno, margem=0.22):
    """Recorta o miolo da forma (encolhido pela margem)."""
    x, y, w, h = cv2.boundingRect(contorno)
    pad_x = int(w * margem)
    pad_y = int(h * margem)
    x1, y1 = x + pad_x, y + pad_y
    x2, y2 = x + w - pad_x, y + h - pad_y
    if x2 <= x1 or y2 <= y1:
        return None, (x, y, w, h)
    return frame[y1:y2, x1:x2], (x1, y1, x2, y2)


def binarizar_otsu(roi_bgr):
    """Binariza com Otsu + dilatação leve."""
    cinza = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)
    _, binarizada = cv2.threshold(cinza, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((2, 2), np.uint8)
    return cv2.dilate(binarizada, kernel, iterations=1)


def tentar_ocr(roi_bin):
    """Roda o Tesseract e retorna o texto bruto."""
    try:
        return pytesseract.image_to_string(roi_bin, config=_CONFIG).strip()
    except Exception as e:
        return f"[ERRO: {e}]"


def main():
    print("=" * 60)
    print(" DEBUG TESSERACT - Leitor de Dígitos (3, 4, 5)")
    print(f" Config: {_CONFIG}")
    print(" Pressione [Q] para sair")
    print("=" * 60)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERRO] Câmera não encontrada.")
        return

    frame_count = 0

    while True:
        status, frame = cap.read()
        if not status:
            break

        frame_count += 1
        frame_debug = frame.copy()

        # ------- ETAPA 1: Segmentação -------
        segmentada = segmentar(frame)

        # ------- ETAPA 2: Encontrar maior contorno válido -------
        contorno = encontrar_maior_contorno_valido(segmentada)

        if contorno is not None:
            x, y, w, h = cv2.boundingRect(contorno)

            # [DEBUG] Desenha bounding box verde no frame principal
            cv2.rectangle(frame_debug, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # [DEBUG] Desenha o contorno encontrado em azul
            cv2.drawContours(frame_debug, [contorno], -1, (255, 100, 0), 2)

            # [DEBUG] Desenha a área interna (ROI encolhida) em amarelo
            margem = 0.22
            px, py = int(w * margem), int(h * margem)
            cv2.rectangle(frame_debug, (x + px, y + py), (x + w - px, y + h - py), (0, 255, 255), 2)

            # [DEBUG] Texto de propriedades do contorno
            area = cv2.contourArea(contorno)
            hull = cv2.convexHull(contorno)
            sol = area / cv2.contourArea(hull) if cv2.contourArea(hull) > 0 else 0
            ar = w / float(h) if h > 0 else 0
            props_txt = f"A:{int(area)} S:{sol:.2f} AR:{ar:.2f}"
            cv2.putText(frame_debug, props_txt, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            # ------- ETAPA 3: Extrair ROI interna -------
            roi_interna, coords = extrair_roi_interna(frame, contorno, margem)

            if roi_interna is not None and roi_interna.size > 0:
                # ------- ETAPA 4: Binarizar para OCR -------
                roi_bin = binarizar_otsu(roi_interna)

                # ------- ETAPA 5: Rodar Tesseract -------
                texto_bruto = tentar_ocr(roi_bin)

                # [DEBUG] Print no console a cada 10 frames para não inundar
                if frame_count % 10 == 0:
                    print(f"[Frame {frame_count}] Tesseract retornou: '{texto_bruto}' | "
                          f"ROI: {roi_interna.shape[1]}x{roi_interna.shape[0]}px | "
                          f"Area={int(area)} Solidity={sol:.2f}")

                # [DEBUG] Resultado do OCR no frame principal
                cor_txt = (0, 255, 0) if texto_bruto in ('3', '4', '5') else (0, 0, 255)
                label = f"OCR: '{texto_bruto}'" if texto_bruto else "OCR: vazio"
                cv2.putText(frame_debug, label, (x, y + h + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor_txt, 2)

                # Exibe janelas separadas da ROI e binarização (redimensionadas para visualizar)
                roi_display = cv2.resize(roi_interna, (200, 200), interpolation=cv2.INTER_NEAREST)
                bin_display = cv2.resize(roi_bin, (200, 200), interpolation=cv2.INTER_NEAREST)

                cv2.imshow("3 - ROI Interna (miolo)", roi_display)
                cv2.imshow("4 - Binarizada (o que o Tesseract ve)", bin_display)
            else:
                cv2.putText(frame_debug, "ROI muito pequena", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        else:
            cv2.putText(frame_debug, "Nenhum contorno valido", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 2)

        # Exibe janelas principais
        cv2.imshow("1 - Frame Original (com debug)", frame_debug)

        seg_display = cv2.resize(segmentada, (frame.shape[1] // 2, frame.shape[0] // 2))
        cv2.imshow("2 - Segmentada (adaptiveThreshold)", seg_display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("\n[DEBUG TESSERACT] Finalizado.")


if __name__ == '__main__':
    main()
