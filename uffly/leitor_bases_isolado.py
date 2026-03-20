# -*- coding: utf-8 -*-
"""
Módulo Isolado: Leitor de Números Dentro de Formas Geométricas (Passo B/C - Missão 1)
---------------------------------------------------------------------------------------
Objetivo:
Ignora o ArUco. Busca por formas grandes e analisa o Número/Dígito no interior.
"""

import cv2
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont

# Injeção via Painel de Controle
from config import *

# Injeção via Módulos Independentes
from visao_utils.hud import escrever_texto_pillow
from visao_utils.geometria import classificar_geometria_gabarito
from visao_utils.estabilizador import EstabilizadorTemporal

# ============================================================================
# LÓGICA DE DÍGITOS DA BASE (TEMPLATE MATCHING)
# ============================================================================

def _gerar_template_digito(digito, tamanho_fonte=60, largura=50, altura=70):
    """
    Gera a imagem base de memória para a IA comparar ('3', '4' ou '5').
    Fundo branco (255) / Texto Preto (0) -> Replica visual físico.
    """
    img = Image.new('L', (largura, altura), 255)  
    draw = ImageDraw.Draw(img)

    try:
        fonte = ImageFont.truetype("arial.ttf", tamanho_fonte)
    except (IOError, OSError):
        fonte = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), str(digito), font=fonte)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pos_x = (largura - tw) // 2 - bbox[0]
    pos_y = (altura - th) // 2 - bbox[1]
    draw.text((pos_x, pos_y), str(digito), fill=0, font=fonte)

    return np.array(img)

def carregar_templates():
    """Compila e guarda os 3 arquivos de memória de Template no Cash"""
    templates = {}
    for d in ('3', '4', '5'):
        templates[d] = _gerar_template_digito(d)
    print(f"[TEMPLATES] Gerados {len(templates)} templates (Arial Regular): {list(templates.keys())}")
    return templates

# ============================================================================
# PRÉ-PROCESSAMENTO
# ============================================================================

def segmentar_frame(frame):
    """
    Transforma o mundo colorido em Preto e Branco adaptativo.
    Usa Threshold Adaptativo ao invés do Canny Global para suportar sombras
    metade claras e metade escuras no campo simulado.
    """
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    borrada = cv2.GaussianBlur(cinza, (5, 5), 0)

    # BLOCK_SIZE ajusta a flexibilidade pra sombras locais pesadas.
    segmentada = cv2.adaptiveThreshold(
        borrada, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=BASES_THRESH_BLOCK_SIZE, C=BASES_THRESH_C
    )

    # Preenche frestas das linhas fragmentadas
    kernel = np.ones((3, 3), np.uint8)
    segmentada = cv2.morphologyEx(segmentada, cv2.MORPH_CLOSE, kernel, iterations=2)
    return segmentada

def calcular_solidity(contorno):
    """
    Atesta a firmeza. Formato irregular = menor que 1.
    Formato Perfeito (ex: Retângulo) = 1.0.
    A estrela pune muito essa métrica devido as pontas longas.
    """
    area = cv2.contourArea(contorno)
    if area <= 0: return 0.0
    hull = cv2.convexHull(contorno)
    hull_area = cv2.contourArea(hull)
    if hull_area <= 0: return 0.0
    return area / hull_area

def calcular_aspect_ratio(contorno):
    """Largura vs Altura. Destrói tentativas de ler paredes e fios finos."""
    x, y, w, h = cv2.boundingRect(contorno)
    if h == 0: return 0.0
    return w / float(h)

def filtrar_contornos_por_propriedades(contornos):
    """Cascata letal de filtros puristas importados do config.py"""
    candidatos = []
    for cnt in contornos:
        area = cv2.contourArea(cnt)
        if not (BASES_AREA_MIN <= area <= BASES_AREA_MAX): continue
        if calcular_solidity(cnt) < BASES_SOLIDITY_MIN: continue
        ar = calcular_aspect_ratio(cnt)
        if not (BASES_ASPECT_RATIO_MIN <= ar <= BASES_ASPECT_RATIO_MAX): continue
        candidatos.append(cnt)

    # Entrega sempre o GIGANTE mais próximo primeiro (trava de mira principal)
    return sorted(candidatos, key=cv2.contourArea, reverse=True)

# ============================================================================
# EXTRAÇÃO
# ============================================================================

def extrair_roi_interna(frame, contorno, margem=0.22):
    """Aperta e asfixia a Bounding Box recortando apenas a polpa/miolo geométrico."""
    x, y, w, h = cv2.boundingRect(contorno)
    pad_x, pad_y = int(w * margem), int(h * margem)
    x1, y1 = x + pad_x, y + pad_y
    x2, y2 = x + w - pad_x, y + h - pad_y

    if x2 <= x1 or y2 <= y1: return None
    return frame[y1:y2, x1:x2]

def identificar_digito_por_template(roi_gray, templates):
    """
    O Motor do Template Matching. Passa todos os tamanhos dos números 3, 4, e 5
    contra a mancha encontrada da câmera e procura > 0.45 de semelhança absoluta.
    """
    melhor_digito, melhor_score = None, 0.0
    h_roi, w_roi = roi_gray.shape[:2]
    
    if h_roi < 10 or w_roi < 10: return None

    for digito, tmpl in templates.items():
        # Busca recursiva em escalas menores que 100% da imagem
        for escala in BASES_ESCALAS_TEMPLATE:
            tw, th = max(5, int(w_roi * escala)), max(5, int(h_roi * escala))
            if tw >= w_roi or th >= h_roi: continue

            # Roda as matrizes umas sobre as outras e extrai a similaridade
            tmpl_resized = cv2.resize(tmpl, (tw, th), interpolation=cv2.INTER_AREA)
            resultado = cv2.matchTemplate(roi_gray, tmpl_resized, cv2.TM_CCOEFF_NORMED)
            _, score, _, _ = cv2.minMaxLoc(resultado)

            if score > melhor_score:
                melhor_score = score
                melhor_digito = digito

    # Barreiras fixadas em config.py
    if melhor_score < BASES_SCORE_MINIMO_TEMPLATE: return None
    return melhor_digito

def extrair_digito_base(roi_bgr, templates):
    # Passo obrigatório: Retira Cor Colorida pra operar só com intensidade térmica
    cinza = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)
    return identificar_digito_por_template(cinza, templates)

# ============================================================================
# ORQUESTRADOR DE EVENTOS DA TELA
# ============================================================================

def observar_frame_bases(frame, templates, estabilizador):
    """Orquestra as cascatas de segmentação para este milissegundo."""
    frame_saida = frame.copy()

    # Etapa 1: Preparação de Terreno Isolado
    segmentada = segmentar_frame(frame)
    contornos_brutos, _ = cv2.findContours(segmentada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Etapa 2: Barreiras Físicas (Área, Solidez, Alongamento)
    candidatos = filtrar_contornos_por_propriedades(contornos_brutos)

    melhor_forma_frame = "Nenhuma"
    melhor_digito_frame = None

    for contorno in candidatos:
        x, y, w, h = cv2.boundingRect(contorno)
        
        # Etapa 3: Invoca o Módulo de Geometria Genérica (Acha as Formas)
        roi_forma = frame[max(0, y-5):min(frame.shape[0], y+h+5), max(0, x-5):min(frame.shape[1], x+w+5)]
        forma, cnt_visual = classificar_geometria_gabarito(roi_forma)

        digito = None
        
        # Etapa 4: Extrai as entranhas do Polígono válido
        if forma != "Nenhuma":
            roi_interna = extrair_roi_interna(frame, contorno)
            if roi_interna is not None and roi_interna.size > 0:
                # Etapa 5: Invoca o Motor de Semelhança de Números (Lê os Dígitos)
                digito = extrair_digito_base(roi_interna, templates)

        # Retenção exclusiva do Maior e Melhor Alvo
        if melhor_forma_frame == "Nenhuma" and forma != "Nenhuma" and digito is not None:
            melhor_forma_frame = forma
            melhor_digito_frame = digito

        # Feedbacks Visuais e UX do OpenCV
        label = f"{forma} | {digito if digito else '?'}"
        if digito and forma != "Nenhuma": cor_box = (0, 255, 0)
        elif forma != "Nenhuma": cor_box = (0, 255, 255)
        else: cor_box = (80, 80, 80)

        cv2.rectangle(frame_saida, (x, y), (x + w, y + h), cor_box, 2)

        if cnt_visual is not None:
            cnt_global = cnt_visual + [max(0, x-5), max(0, y-5)]
            cv2.drawContours(frame_saida, [cnt_global], -1, (255, 180, 0), 2)

        frame_saida = escrever_texto_pillow(frame_saida, label, x, max(10, y - 35), 22, (255, 255, 255), 2, (0, 0, 0))

    # =========================================================================
    # REPASSE PARA A MÁQUINA DE ESTADOS
    # =========================================================================
    # Etapa 6: Repasse ao Estado Temporal (Segundos ininterruptos reais, salvando Raspberry de Low FPS)
    estabilizador.atualizar_leitura(val_primario=melhor_forma_frame, val_secundario=melhor_digito_frame)
    progresso = estabilizador.obter_progresso()
    forma_conf, digito_conf = estabilizador.obter_leitura_confirmada()

    # Barra HUB HUD Carregamento
    barra_w, barra_h = 200, 20
    barra_x, barra_y = frame.shape[1] - barra_w - 20, 15
    cv2.rectangle(frame_saida, (barra_x, barra_y), (barra_x + barra_w, barra_y + barra_h), (60, 60, 60), -1)
    
    fill_w = int(barra_w * progresso)
    cor_barra = (0, 255, 0) if forma_conf else (0, 200, 255)
    cv2.rectangle(frame_saida, (barra_x, barra_y), (barra_x + fill_w, barra_y + barra_h), cor_barra, -1)
    cv2.rectangle(frame_saida, (barra_x, barra_y), (barra_x + barra_w, barra_y + barra_h), (255, 255, 255), 1)

    if forma_conf:
        status_txt = f"CONFIRMADO: {forma_conf} | {digito_conf}"
        cor_status = (0, 255, 0)
    elif progresso > 0:
        status_txt = f"Estabilizando... {int(progresso * 100)}%"
        cor_status = (0, 200, 255)
    else:
        status_txt = "Buscando bases..."
        cor_status = (200, 200, 200)

    frame_saida = escrever_texto_pillow(frame_saida, status_txt, barra_x, barra_y + barra_h + 5, 16, cor_status)
    info = f"Res: {frame.shape[1]}x{frame.shape[0]} | Candidatos: {len(candidatos)}"
    frame_saida = escrever_texto_pillow(frame_saida, info, 10, frame.shape[0] - 30, 16, (0, 255, 255))

    return frame_saida

def iniciar_teste():
    print("[MÓDULO - PASSO B/C | COM CRONÔMETRO] Leitor de Bases")
    print(" >>> Pressione [Q] para encerrar.\n")
    
    templates = carregar_templates()
    estabilizador = EstabilizadorTemporal(tempo_necessario=TEMPO_CONFIRMACAO_BASES)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened(): return

    while True:
        status, frame = cap.read()
        if not status: break

        frame_anotado = observar_frame_bases(frame, templates, estabilizador)
        cv2.imshow("LEITOR DE BASES - TEMPLATE MATCHING", frame_anotado)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    iniciar_teste()
