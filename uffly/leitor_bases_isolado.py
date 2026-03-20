# -*- coding: utf-8 -*-
"""
Módulo Isolado: Leitor de Números Dentro de Formas Geométricas (Passo B/C - Missão 1)
---------------------------------------------------------------------------------------
Abordagem: AdaptiveThreshold + Filtros em Cascata + Template Matching.

Pipeline:
1. AdaptiveThreshold: segmentação local robusta a iluminação variável.
2. Filtros em Cascata: Área → Solidity → Aspect Ratio (elimina falsos positivos).
3. classificar_geometria_gabarito (reaproveitado): identifica Triângulo/Hexágono/Estrela.
4. Template Matching (cv2.matchTemplate): compara ROI interna com templates
   dos dígitos 3, 4, 5 gerados em Arial Regular. Zero dependência externa.
5. EstabilizadorLeitura: confirma leitura após N frames consecutivos idênticos.

Reaproveitamentos:
- classificar_geometria_gabarito(): importado de leitor_aruco_isolado.
- escrever_texto_pillow(): importado de identificar_distancia.
"""

import cv2
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont

from identificar_distancia import escrever_texto_pillow
from leitor_aruco_isolado import classificar_geometria_gabarito

# ============================================================================
# SETUP DE CALIBRAÇÃO (alterar aqui no dia da competição)
# ============================================================================

# Limites de Área (px): abaixo = ruído; acima = borda da folha inteira.
# Reduzido o mínimo de 2000 para 800 para detectar formas mais distantes.
AREA_MIN = 800
AREA_MAX = 200_000

# Solidity (solidez = área / casco convexo): formas com muitos "buracos" têm solidity baixo.
# Reduzido de 0.70 para 0.40 porque estrelas de 5 pontas são côncavas (~0.45-0.55).
# A classificação posterior por approxPolyDP ainda protege contra falsos positivos.
SOLIDITY_MIN = 0.40

# Aspect Ratio (largura / altura): evita capturar linhas de horizonte e bordas longas.
ASPECT_RATIO_MIN = 0.35
ASPECT_RATIO_MAX = 2.80

# Template Matching: score mínimo para aceitar uma leitura.
SCORE_MINIMO_TEMPLATE = 0.45

# Escalas do template matching: mais escalas = detecta formas de tamanhos variados.
# Incluídos tamanhos menores (0.2, 0.35) para cobrir bases distantes da câmera.
ESCALAS_TEMPLATE = (0.2, 0.35, 0.5, 0.65, 0.8)

# Estabilizador: quantos frames consecutivos idênticos antes de confirmar leitura.
# ~15 frames a 30fps = 0.5 segundo. Evita oscilação entre dígitos parecidos (3↔4).
FRAMES_PARA_CONFIRMAR = 15

# AdaptiveThreshold: vizinhança local e tolerância.
# blockSize maior = menos sensível a ruídos locais; C maior = mais tolerante a fundos cinzas.
BLOCK_SIZE = 31
THRESHOLD_C = 4


# ============================================================================
# ESTABILIZADOR DE LEITURA (ANTI-OSCILAÇÃO)
# ============================================================================

class EstabilizadorLeitura:
    """
    Acumula leituras consecutivas idênticas (forma + dígito).
    Só confirma a leitura após N frames seguidos com o mesmo resultado.
    Reseta se a leitura mudar entre um frame e outro.

    Padrão idêntico ao RastreadorGabarito do leitor_aruco_isolado.py.
    """

    def __init__(self, frames_necessarios=FRAMES_PARA_CONFIRMAR):
        self.frames_necessarios = frames_necessarios
        self.forma_atual = None
        self.digito_atual = None
        self.frames_acumulados = 0
        self.confirmado = False      # True = leitura estável confirmada
        self.forma_confirmada = None
        self.digito_confirmado = None

    def atualizar(self, forma, digito):
        """
        Chamada a cada frame com a leitura bruta.
        Retorna True se a leitura foi confirmada (estável).
        """
        # Proteção: se o frame não detectou NADA de útil, zera o cronômetro na hora!
        # Não queremos "confirmar" que não há nenhuma base.
        if forma == "Nenhuma" or digito is None:
            self.forma_atual = None
            self.digito_atual = None
            self.frames_acumulados = 0
            self.confirmado = False
            return False

        # Se a leitura é idêntica ao frame anterior, acumula
        if forma == self.forma_atual and digito == self.digito_atual:
            self.frames_acumulados += 1

            # Atingiu o limiar de confirmação
            if self.frames_acumulados >= self.frames_necessarios:
                self.confirmado = True
                self.forma_confirmada = forma
                self.digito_confirmado = digito
        else:
            # Leitura mudou: reseta o contador
            self.forma_atual = forma
            self.digito_atual = digito
            self.frames_acumulados = 1
            self.confirmado = False

        return self.confirmado

    def obter_progresso(self):
        """Retorna fração 0.0 a 1.0 do progresso até confirmar."""
        return min(self.frames_acumulados / self.frames_necessarios, 1.0)

    def obter_leitura_confirmada(self):
        """Retorna (forma, digito) confirmados ou (None, None)."""
        if self.confirmado:
            return self.forma_confirmada, self.digito_confirmado
        return None, None


# ============================================================================
# GERAÇÃO E CARREGAMENTO DE TEMPLATES (ARIAL REGULAR)
# ============================================================================

def _gerar_template_digito(digito, tamanho_fonte=60, largura=50, altura=70):
    """
    Gera uma imagem binária de um dígito usando Arial Regular via Pillow.
    Fundo branco, dígito preto — imitando exatamente o visual das bases da competição.
    O template é retornado em escala de cinza como array NumPy.
    """
    img = Image.new('L', (largura, altura), 255)  # Fundo branco
    draw = ImageDraw.Draw(img)

    # Tenta usar Arial; se não encontrar, usa a fonte padrão do Pillow
    try:
        fonte = ImageFont.truetype("arial.ttf", tamanho_fonte)
    except (IOError, OSError):
        fonte = ImageFont.load_default()

    # Centraliza o dígito na imagem
    bbox = draw.textbbox((0, 0), str(digito), font=fonte)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pos_x = (largura - tw) // 2 - bbox[0]
    pos_y = (altura - th) // 2 - bbox[1]
    draw.text((pos_x, pos_y), str(digito), fill=0, font=fonte)  # Preto

    return np.array(img)


def carregar_templates():
    """
    Gera os 3 templates dos dígitos da competição (3, 4, 5).
    Retorna dicionário: {'3': img_gray, '4': img_gray, '5': img_gray}
    """
    templates = {}
    for d in ('3', '4', '5'):
        templates[d] = _gerar_template_digito(d)
    print(f"[TEMPLATES] Gerados {len(templates)} templates (Arial Regular): {list(templates.keys())}")
    return templates


# ============================================================================
# FUNÇÕES DE PRÉ-PROCESSAMENTO
# ============================================================================

def segmentar_frame(frame):
    """
    Converte o frame para tons de cinza e aplica AdaptiveThreshold.

    Por que AdaptiveThreshold em vez de Canny global?
    O Canny usa um limiar fixo em toda a imagem. Em ambientes com iluminação
    variável (reflexo de lâmpada, sombras parciais), isso gera bordas falsas
    em partes do fundo. O AdaptiveThreshold ajusta o limiar pixel a pixel,
    comparando cada região com a média dos vizinhos — muito mais estável.
    """
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    borrada = cv2.GaussianBlur(cinza, (5, 5), 0)

    # blockSize=31: vizinhança local de comparação
    # C=4: tolerância para papel com tom levemente acinzentado
    segmentada = cv2.adaptiveThreshold(
        borrada, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=BLOCK_SIZE, C=THRESHOLD_C
    )

    # Fecha lacunas entre bordas do polígono
    kernel = np.ones((3, 3), np.uint8)
    segmentada = cv2.morphologyEx(segmentada, cv2.MORPH_CLOSE, kernel, iterations=2)

    return segmentada


def calcular_solidity(contorno):
    """
    Solidez = área do contorno / área do casco convexo (hull).

    Um hexágono perfeito tem solidity próximo de 1.0.
    Uma sombra irregular ou textura de fundo tem solidity baixo.
    Usamos isso para descartar formas que 'parecem polígonos' mas não são.
    """
    area = cv2.contourArea(contorno)
    if area <= 0:
        return 0.0
    hull = cv2.convexHull(contorno)
    hull_area = cv2.contourArea(hull)
    if hull_area <= 0:
        return 0.0
    return area / hull_area


def calcular_aspect_ratio(contorno):
    """
    Aspect Ratio = largura / altura da bounding box do contorno.

    Bordas longas do papel, linhas horizontais e quadros de janela
    têm aspect ratio > 3.0 ou < 0.3. As formas que buscamos (triângulo,
    hexágono, estrela) tendem a ser aproximadamente 'simétricas'.
    """
    x, y, w, h = cv2.boundingRect(contorno)
    if h == 0:
        return 0.0
    return w / float(h)


def filtrar_contornos_por_propriedades(contornos):
    """Aplica os 3 filtros em cascata: Área → Solidity → Aspect Ratio."""
    candidatos = []
    for cnt in contornos:
        # Filtro 1: Área — elimina ruídos pequenos e bordas do frame inteiro
        area = cv2.contourArea(cnt)
        if not (AREA_MIN <= area <= AREA_MAX):
            continue

        # Filtro 2: Solidity — elimina sombras irregulares e texturas
        if calcular_solidity(cnt) < SOLIDITY_MIN:
            continue

        # Filtro 3: Aspect Ratio — elimina linhas longas e bordas de folha
        ar = calcular_aspect_ratio(cnt)
        if not (ASPECT_RATIO_MIN <= ar <= ASPECT_RATIO_MAX):
            continue

        candidatos.append(cnt)

    # Retorna do maior para o menor (prioriza o destaque principal na cena)
    return sorted(candidatos, key=cv2.contourArea, reverse=True)


# ============================================================================
# TEMPLATE MATCHING
# ============================================================================

def extrair_roi_interna(frame, contorno, margem=0.22):
    """
    Recorta o interior do contorno com margem negativa (encolhe a bbox).
    Evita capturar as linhas do polígono, entregando só o miolo.
    """
    x, y, w, h = cv2.boundingRect(contorno)

    # Margem negativa: shrink interno para pegar só o centro limpo
    pad_x = int(w * margem)
    pad_y = int(h * margem)

    x1, y1 = x + pad_x, y + pad_y
    x2, y2 = x + w - pad_x, y + h - pad_y

    # Garante que o crop não ficou invertido (casos extremos com formas muito pequenas)
    if x2 <= x1 or y2 <= y1:
        return None

    return frame[y1:y2, x1:x2]


def identificar_digito_por_template(roi_gray, templates):
    """
    Desliza cada template (3, 4, 5) pela ROI e retorna o dígito com maior
    correlação (TM_CCOEFF_NORMED). Rejeita se o score ficar abaixo do limiar.

    Multi-escala: testa o template em múltiplos tamanhos para cobrir
    variação de distância da câmera.
    """
    melhor_digito = None
    melhor_score = 0.0

    h_roi, w_roi = roi_gray.shape[:2]
    if h_roi < 10 or w_roi < 10:
        return None

    for digito, tmpl in templates.items():
        # Multi-escala: testa cada escala configurada no SETUP
        for escala in ESCALAS_TEMPLATE:
            tw = max(5, int(w_roi * escala))
            th = max(5, int(h_roi * escala))

            # O template não pode ser maior que a ROI
            if tw >= w_roi or th >= h_roi:
                continue

            tmpl_resized = cv2.resize(tmpl, (tw, th), interpolation=cv2.INTER_AREA)
            resultado = cv2.matchTemplate(roi_gray, tmpl_resized, cv2.TM_CCOEFF_NORMED)
            _, score, _, _ = cv2.minMaxLoc(resultado)

            if score > melhor_score:
                melhor_score = score
                melhor_digito = digito

    # Rejeita leituras com confiança baixa
    if melhor_score < SCORE_MINIMO_TEMPLATE:
        return None

    return melhor_digito


def extrair_digito_base(roi_bgr, templates):
    """
    Converte a ROI interna para cinza e aplica template matching.
    Retorna '3', '4', '5' ou None.
    """
    cinza = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)
    return identificar_digito_por_template(cinza, templates)


# ============================================================================
# ORQUESTRADOR DO FRAME
# ============================================================================

def observar_frame_bases(frame, templates, estabilizador):
    """Orquestra o pipeline completo para um único frame."""
    frame_saida = frame.copy()

    # 1. Segmentação com AdaptiveThreshold
    segmentada = segmentar_frame(frame)

    # 2. Extração de contornos externos
    contornos_brutos, _ = cv2.findContours(segmentada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 3. Filtro em cascata
    candidatos = filtrar_contornos_por_propriedades(contornos_brutos)

    # Variáveis da melhor leitura do frame (para passar ao estabilizador)
    melhor_forma_frame = "Nenhuma"
    melhor_digito_frame = None

    for contorno in candidatos:
        x, y, w, h = cv2.boundingRect(contorno)

        # 4. Classifica a forma geométrica (reaproveitando módulo ArUco)
        roi_forma = frame[max(0, y-5):min(frame.shape[0], y+h+5),
                          max(0, x-5):min(frame.shape[1], x+w+5)]
        forma, cnt_visual = classificar_geometria_gabarito(roi_forma)

        # 5. Extrai miolo e aplica Template Matching SÓ se achou uma forma válida
        digito = None
        if forma != "Nenhuma":
            roi_interna = extrair_roi_interna(frame, contorno)
            if roi_interna is not None and roi_interna.size > 0:
                digito = extrair_digito_base(roi_interna, templates)

        # Guarda o candidato mais completo (forma + dígito) para o estabilizador
        # Como iteramos os candidatos do MAIOR pro MENOR, travamos apenas no PRIMEIRO que estiver válido!
        if melhor_forma_frame == "Nenhuma" and forma != "Nenhuma" and digito is not None:
            melhor_forma_frame = forma
            melhor_digito_frame = digito

        # --------- Feedback Visual ---------
        label = f"{forma} | {digito if digito else '?'}"

        if digito and forma != "Nenhuma":
            cor_box = (0, 255, 0)       # Verde: forma + número identificados
        elif forma != "Nenhuma":
            cor_box = (0, 255, 255)     # Amarelo: forma sim, número não
        else:
            cor_box = (80, 80, 80)      # Cinza: indefinido

        cv2.rectangle(frame_saida, (x, y), (x + w, y + h), cor_box, 2)

        # Desenha contorno do forma em azul claro (debug visual)
        if cnt_visual is not None:
            cnt_global = cnt_visual + [max(0, x-5), max(0, y-5)]
            cv2.drawContours(frame_saida, [cnt_global], -1, (255, 180, 0), 2)

        # Texto HUD acima da box
        frame_saida = escrever_texto_pillow(
            frame_bgr=frame_saida,
            texto=label,
            x=x, y=max(10, y - 35),
            tamanho=22, cor=(255, 255, 255),
            stroke=2, stroke_cor=(0, 0, 0)
        )

    # 6. Estabilizador: acumula leituras e confirma apenas após N frames idênticos
    estabilizador.atualizar(melhor_forma_frame, melhor_digito_frame)
    progresso = estabilizador.obter_progresso()
    forma_conf, digito_conf = estabilizador.obter_leitura_confirmada()

    # Barra de progresso visual do estabilizador (canto superior direito)
    barra_w = 200
    barra_h = 20
    barra_x = frame.shape[1] - barra_w - 20
    barra_y = 15
    cv2.rectangle(frame_saida, (barra_x, barra_y), (barra_x + barra_w, barra_y + barra_h), (60, 60, 60), -1)
    fill_w = int(barra_w * progresso)
    cor_barra = (0, 255, 0) if forma_conf else (0, 200, 255)
    cv2.rectangle(frame_saida, (barra_x, barra_y), (barra_x + fill_w, barra_y + barra_h), cor_barra, -1)
    cv2.rectangle(frame_saida, (barra_x, barra_y), (barra_x + barra_w, barra_y + barra_h), (255, 255, 255), 1)

    # Texto de status do estabilizador
    if forma_conf:
        status_txt = f"CONFIRMADO: {forma_conf} | {digito_conf}"
        cor_status = (0, 255, 0)
    elif progresso > 0:
        status_txt = f"Estabilizando... {int(progresso * 100)}%"
        cor_status = (0, 200, 255)
    else:
        status_txt = "Buscando bases..."
        cor_status = (200, 200, 200)

    frame_saida = escrever_texto_pillow(
        frame_saida, status_txt,
        barra_x, barra_y + barra_h + 5,
        16, cor_status
    )

    # Rodapé de debug
    info = f"Res: {frame.shape[1]}x{frame.shape[0]} | Candidatos: {len(candidatos)}"
    frame_saida = escrever_texto_pillow(frame_saida, info, 10, frame.shape[0] - 30, 16, (0, 255, 255))

    return frame_saida


# ============================================================================
# LOOP PRINCIPAL
# ============================================================================

def iniciar_teste():
    print("[MÓDULO - PASSO B/C] Leitor de Bases (Template Matching + Estabilizador)")
    print(f" >>> Setup: AREA={AREA_MIN}-{AREA_MAX} | SOLIDITY>={SOLIDITY_MIN} | SCORE>={SCORE_MINIMO_TEMPLATE}")
    print(f" >>> Escalas: {ESCALAS_TEMPLATE} | Confirmar após: {FRAMES_PARA_CONFIRMAR} frames")
    print(" >>> Pressione [Q] para encerrar.\n")

    # Gera templates dos dígitos na inicialização (uma única vez)
    templates = carregar_templates()

    # Instancia o estabilizador de leitura
    estabilizador = EstabilizadorLeitura()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERRO CRÍTICO] Câmera não encontrada (Index=0).")
        return

    while True:
        status, frame = cap.read()
        if not status:
            break

        frame_anotado = observar_frame_bases(frame, templates, estabilizador)
        cv2.imshow("LEITOR DE BASES - TEMPLATE MATCHING", frame_anotado)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[MÓDULO - PASSO B/C] Finalizado com sucesso.")


if __name__ == '__main__':
    iniciar_teste()
