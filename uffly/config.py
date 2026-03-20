# -*- coding: utf-8 -*-
"""
Configurações Globais de Constantes de Visão Computacional
----------------------------------------------------------
Este arquivo centraliza e unifica todos os limiares que afetam
a detecção da câmera (Filtros, Cores, Tempos, Thresholds matemáticos). 
Edite este arquivo caso sinta necessidade(muito sol, sombra extrema, distância).
"""

import cv2

# ==============================================================================
# 1. PARÂMETROS GERAIS E INTERFACE (HUD)
# ==============================================================================
COR_TEXTO_PADRAO = (255, 255, 255)  # Branco
COR_TEXTO_SUCESSO = (0, 255, 0)     # Verde
COR_TEXTO_AVISO = (0, 255, 255)     # Amarelo
COR_TEXTO_FALHA = (200, 200, 200)   # Cinza claro


# ==============================================================================
# 2. CONFIGURAÇÕES DOS ESTABILIZADORES TEMPORAIS (visao_utils/estabilizador.py)
# ==============================================================================
# Tempo CONTÍNUO (em segundos reais de relógio) exigido para atestar uma identificação.
# Substitui o uso de "Frames". Protege contra a variação de FPS no Raspberry Pi.
TEMPO_CONFIRMACAO_GEOMETRIA = 5.0  # Usado pelo Passo A (ArUco + Forma Externa)
TEMPO_CONFIRMACAO_BASES = 0.5      # Usado pelo Passo B (Substitui os antigos '15 frames')


# ==============================================================================
# 3. CONFIGURAÇÕES DE DETECÇÃO ARUCO (leitor_aruco_isolado.py)
# ==============================================================================
# Base oficial exigida nas regras
ARUCO_DICIONARIO = cv2.aruco.DICT_5X5_1000

# Fator multiplicador de Bounding Box após encontrar o ArUco.
# Usado para recortar o contorno quadrado na folha A4 e focar a leitura ali.
# Ex: 1.35 significa que a imagem recortada será 35% mais larga que a área preta do ArUco.
ARUCO_MARGEM_PERCENTUAL = 1.35


# ==============================================================================
# 4. CONFIGURAÇÕES MATEMÁTICAS DE GEOMETRIA E CONTORNOS (visao_utils/geometria.py)
# ==============================================================================
# Área mínima para o polígono não ser descartado como um simples ruído de piso
GEOMETRIA_AREA_MIN_PX = 500

# Limiares do Filtro Canny (Detecção de borda). Lower detecta os fracos conectados aos fortes. Upper detecta os fortes.
GEOMETRIA_CANNY_LOWER = 50
GEOMETRIA_CANNY_UPPER = 150

# Fator Epsilon de suavização do ApproxPolyDP. Diz o quão rígido ou curvo será o polígono final.
# NUNCA usar maior que 0.02, ou as pontas longas da Estrela de 5 pontas serão "cortadas"/fundidas.
GEOMETRIA_EPSILON_MULT = 0.015

# Usado pela função de Convexity Defects. Profundidade mínima de um vale para ser atestado.
# É definido como % da menor largura/altura da janela. 0.15 = Vale precisa entrar 15% pra dentro da forma.
GEOMETRIA_ESTRELA_VALEDEPTH_PERC = 0.15


# ==============================================================================
# 5. CONFIGURAÇÕES DO LEITOR DE BASES GERAIS (leitor_bases_isolado.py)
# ==============================================================================
# Área do polígono total da Base para não captar um papel torto longe
BASES_AREA_MIN = 800
BASES_AREA_MAX = 200000

# Aspect Ratio (Largura / Altura do Polígono). Elimina detecções em cordas, vigas e paredes longas.
BASES_ASPECT_RATIO_MIN = 0.35
BASES_ASPECT_RATIO_MAX = 2.80

# Solidity (Razão de Preenchimento: Volume Real / Matéria Virtual Envolvente).
# Ex: Hexágono puro = 1.0. Estrela pura = 0.40 ~ 0.50 (ela é cheia de vales que subtraem do invólucro).
BASES_SOLIDITY_MIN = 0.40

# AdaptiveThreshold: Segmentação de Luminosidade Variável (luz local melhor que Canny Global).
BASES_THRESH_BLOCK_SIZE = 31 # Tamanho da sonda em pixels. DEVE ser número Ímpar
BASES_THRESH_C = 4           # Valor de correção. Tolerância pra sombra.

# ==============================================================================
# 6. CONFIGURAÇÕES DO TEMPLATE MATCHING DOS DÍGITOS DA BASE (leitor_bases_isolado.py)
# ==============================================================================
# Nota decimal bruta necessária para bater o martelo sobre um número (0 = nada, 1 = igual a cópia).
BASES_SCORE_MINIMO_TEMPLATE = 0.45

# Multi-Escalas a serem varridas matematicamente (Custa FPS para cada escala extraida).
# Mais opções de decibéis baixos significa ler de mais longe.
BASES_ESCALAS_TEMPLATE = (0.2, 0.35, 0.5, 0.65, 0.8)
