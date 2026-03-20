# -*- coding: utf-8 -*-
"""
Script de Debug Visual + Matemático: Template Matching (Missão 1)
-----------------------------------------------------------------
Objetivo: Diagnosticar o viés no dígito '3' e investigar por que '4' e '5' 
estão recebendo scores mais baixos do OpenCV.

Como funciona:
- Lê a câmera continuamente.
- Segmenta a maior base encontrada, igual ao `leitor_bases_isolado.py`.
- Mostra em janelas separadas: A Segmentação Binarizada, a ROI pura em cinza,
  e os Templates gerados da Arial.
- Pressione [ESPAÇO] a qualquer momento para FORÇAR um "dump" detalhado no 
  console, exibindo qual foi a nota de similaridade do 3, 4 e 5 pixel por pixel.
- Pressione [S] para Salvar a ROI atual no disco (para podermos analisar se for fonte).
"""

import cv2
import numpy as np
import time
import os

from identificar_distancia import escrever_texto_pillow

# Importa as configurações exatas que estão rodando no script principal
from leitor_bases_isolado import (
    segmentar_frame, 
    filtrar_contornos_por_propriedades, 
    extrair_roi_interna, 
    carregar_templates, 
    ESCALAS_TEMPLATE,
    SCORE_MINIMO_TEMPLATE
)

def gerar_imagem_templates(templates):
    """Junta as 3 imagens dos templates lado a lado para exibição"""
    imgs = [templates['3'], templates['4'], templates['5']]
    return np.hstack(imgs)

def registrar_dump_matematico(roi_gray, templates):
    """
    Simula o exato cruzamento que o OpenCV faz, mas guarda 
    e imprime TODOS os recortes em TODAS as escalas.
    """
    h_roi, w_roi = roi_gray.shape[:2]
    if h_roi < 10 or w_roi < 10:
        print("[ERRO] ROI muito pequena para análise.")
        return

    print("\n" + "="*50)
    print("DUMP MATEMÁTICO: TEMPLATE MATCHING (TM_CCOEFF_NORMED)")
    print(f"Resolução da ROI (miolo da base): {w_roi}x{h_roi} px")
    print("="*50)

    melhor_global = {"digito": None, "score": 0.0, "escala": 0.0}

    for escala in ESCALAS_TEMPLATE:
        print(f"\n[Escala {escala:.2f}] Tamanho testado:")
        
        for digito, tmpl in templates.items():
            tw = max(5, int(w_roi * escala))
            th = max(5, int(h_roi * escala))
            
            if tw >= w_roi or th >= h_roi:
                print(f"  - Digito '{digito}': {tw}x{th} -> EXCEDEU TAMANHO DA ROI (Ignorado)")
                continue
                
            tmpl_resized = cv2.resize(tmpl, (tw, th), interpolation=cv2.INTER_AREA)
            
            # O cv2.matchTemplate "escorrega" o tmpl_resized por cima da roi_gray
            # comparando o preenchimento dos pixels. 1.0 é um match idêntico.
            resultado = cv2.matchTemplate(roi_gray, tmpl_resized, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(resultado)
            
            print(f"  - Digito '{digito}': Score {max_val:.4f} (Mínimo: {SCORE_MINIMO_TEMPLATE:.2f})")
            
            if max_val > melhor_global["score"]:
                melhor_global = {"digito": digito, "score": max_val, "escala": escala}

    print("-" * 50)
    if melhor_global["score"] >= SCORE_MINIMO_TEMPLATE:
        print(f"VENCEDOR: '{melhor_global['digito']}' | Score: {melhor_global['score']:.4f} (Escala: {melhor_global['escala']:.2f})")
    else:
        print(f"NENHUM VENCEU. O melhor foi '{melhor_global['digito']}' com {melhor_global['score']:.4f}, mas não atingiu os {SCORE_MINIMO_TEMPLATE:.2f} exigidos.")
    print("="*50 + "\n")

def loop_debug():
    templates = carregar_templates()
    img_templates_combinada = gerar_imagem_templates(templates)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Câmera não encontrada.")
        return

    print("="*50)
    print("MODO DE DEBUG VISUAL ATIVADO")
    print("Aponte a câmera para uma base contendo os números 3, 4 ou 5.")
    print(" - Janela 'Câmera': Visão total com Bounding Box.")
    print(" - Janela 'Segmentada': Como o robô enxerga o claro/escuro.")
    print(" - Janela 'ROI Bruta': O miolo da base (é ISSO que é comparado ao template).")
    print(" ")
    print("CONTROLES:")
    print(" [ESPAÇO] -> Tira um 'raio-x' dos cálculos no exato frame atual no console.")
    print(" [S] -> Salva a foto da ROI atual (imagem preta e branca do número) na pasta.")
    print(" [Q] -> Sair do debug.")
    print("="*50)

    ultimo_dump = 0

    while True:
        status, frame = cap.read()
        if not status: break

        frame_saida = frame.copy()
        
        # Segmentação e Filtros importados do projeto original para não haver diferenças nenhura
        segmentada = segmentar_frame(frame)
        contornos_brutos, _ = cv2.findContours(segmentada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        candidatos = filtrar_contornos_por_propriedades(contornos_brutos)

        roi_cinza_pura = None
        achou_alvo = False

        for contorno in candidatos:
            x, y, w, h = cv2.boundingRect(contorno)
            cv2.rectangle(frame_saida, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            roi_interna = extrair_roi_interna(frame, contorno)
            if roi_interna is not None and roi_interna.size > 0:
                roi_cinza_pura = cv2.cvtColor(roi_interna, cv2.COLOR_BGR2GRAY)
                cv2.imshow("2. ROI Bruta (O que é analisado)", roi_cinza_pura)
                achou_alvo = True
                
                frame_saida = escrever_texto_pillow(frame_saida, "ALVO DETECTADO - APERTE [ESPAÇO]", x, y - 30, 16, (0, 255, 0))
            break # Trava só no primeiro (Maior Alvo) igual fizemos no sistema original

        if not achou_alvo:
            frame_saida = escrever_texto_pillow(frame_saida, "Buscando Base...", 20, 30, 20, (200, 200, 200))
            # Cria tela preta se não achou para a janela não travar no último bom frame
            tela_preta = np.zeros((100, 100), dtype=np.uint8)
            cv2.imshow("2. ROI Bruta (O que é analisado)", tela_preta)

        cv2.imshow("1. Camera (Visao Total)", frame_saida)
        cv2.imshow("3. Binarizacao AdaptiveThreshold", segmentada)
        cv2.imshow("4. Templates Font Arial", img_templates_combinada)

        key = cv2.waitKey(30) & 0xFF
        
        if key == ord('q') or key == 27: # Q ou ESC
            break
            
        elif key == 32: # ESPAÇO
            if roi_cinza_pura is not None:
                registrar_dump_matematico(roi_cinza_pura, templates)
            else:
                print("Nenhuma ROI isolada no momento. Aponte para uma base.")
                
        elif key == ord('s'): # S (Salvar print)
            if roi_cinza_pura is not None:
                nome_arq = f"roi_debug_{int(time.time())}.png"
                cv2.imwrite(nome_arq, roi_cinza_pura)
                print(f"[IMAGEM SALVA] A imagem da ROI foi salva como '{nome_arq}' na pasta do projeto.")
            else:
                print("Não há ROI para salvar no momento.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    loop_debug()
