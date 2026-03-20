# -*- coding: utf-8 -*-
"""
Módulo Isolado: Leitor de ArUco + Forma Externa (Passo A - Missão 1)
---------------------------------------------------------------------
Responsabilidade Exclusiva:
1. Capturar imagem da câmera.
2. Identificar Marcador ArUco (Dicionário 5x5).
3. Determinar o ID do ArUco validado.
4. Buscar geometria/contornos em uma margem ao redor (Bounding Box expandida).
5. Estabilização Lógica no Estado de Busca Temporal.
"""

import cv2
import numpy as np

# Injeção de dependências do Painel de Controle
from config import ARUCO_DICIONARIO, ARUCO_MARGEM_PERCENTUAL, TEMPO_CONFIRMACAO_GEOMETRIA

# Injeção de dependências Táticas e Estéticas 
from visao_utils.hud import interagir_hub_principal, escrever_texto_pillow
from visao_utils.estabilizador import EstabilizadorTemporal
from visao_utils.geometria import classificar_geometria_gabarito

# Inicializa o motor interno do OpenCV para leitura de ArUcos
_aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICIONARIO)
_aruco_params = cv2.aruco.DetectorParameters()
DETECTOR_ARUCO = cv2.aruco.ArucoDetector(_aruco_dict, _aruco_params)

# ============================================================================
# LÓGICAS MESTRE (COMPUTER VISION PURA)
# ============================================================================

def extrair_roi_expandida(frame, cantos_aruco, margem_percentual=ARUCO_MARGEM_PERCENTUAL):
    """
    Pega os cantos apertados do ArUco lido e cria uma janela (ROI) folgada
    ao redor dele. Assim a visão "ignora" o galpão inteiro e só procura a forma
    geométrica pertinho magnético do ArUco.
    """
    pts = cantos_aruco[0].astype(int)
    # Extrai o ponto mais à esquerda/cima e o mais à direita/baixo
    x_min, y_min = np.min(pts, axis=0)
    x_max, y_max = np.max(pts, axis=0)
    
    largura = x_max - x_min
    altura = y_max - y_min
    
    # Adiciona a gordura de margem (padding)
    pad_x = int(largura * margem_percentual)
    pad_y = int(altura * margem_percentual)
    
    # Trava as margens para não estourar para fora da tela da câmera (IndexError)
    altura_frame, largura_frame = frame.shape[:2]
    x_ini = max(0, x_min - pad_x)
    y_ini = max(0, y_min - pad_y)
    x_fim = min(largura_frame, x_max + pad_x)
    y_fim = min(altura_frame, y_max + pad_y)
    
    # Recorta a imagem
    roi = frame[y_ini:y_fim, x_ini:x_fim]
    return roi, x_ini, y_ini


def observar_frame_single_step(frame, rastreador):
    """
    Coração do Leitor: Aplica o pipeline do ArUco e varre a Máfica de Visão.
    """
    frame_processado = frame.copy()
    
    # Etapa 1: Pede pro OpenCV caçar os códigos de barras quadrados
    corners, ids, rejected = DETECTOR_ARUCO.detectMarkers(frame_processado)
    
    # Mostra os falsos-positivos de ArUco (ajuda no debug)
    qtd_rejeitados = len(rejected) if rejected is not None else 0
    if qtd_rejeitados > 0:
        cv2.aruco.drawDetectedMarkers(frame_processado, rejected, borderColor=(0, 0, 255))
        
    candidato_id = None
    candidato_forma = "Nenhuma"
    candidato_area = 0
    
    # Se encontrou ao menos um ArUco nítido
    if ids is not None and len(ids) > 0:
        cv2.aruco.drawDetectedMarkers(frame_processado, corners, ids)
        
        # Etapa 2: Analisa todos os ArUcos detectados no frame
        for index in range(len(ids)):
            aruco_id = ids[index][0]
            corn = corners[index]
            
            # Etapa 3: Isola a região de busca (apenas o que está grudado no ArUco)
            roi_expandida, roi_x, roi_y = extrair_roi_expandida(frame, corn, margem_percentual=ARUCO_MARGEM_PERCENTUAL)
            
            # Etapa 4: Analisa puramente as linhas da ROI pra dizer qual a Forma Geométrica
            forma, cnt_forma = classificar_geometria_gabarito(roi_expandida)
            
            # Caixa Amarela = Até onde a visão do drone se extendeu para procurar a forma
            roi_h, roi_w = roi_expandida.shape[:2]
            cv2.rectangle(frame_processado, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 255, 255), 2)
            
            # Desenha no Polígono o contorno que o Módulo de Geometria encontrou
            if cnt_forma is not None:
                cnt_forma_global = cnt_forma + [roi_x, roi_y] # Compensa o X/Y local pelo global
                cor_forma = (0, 255, 0) if forma != "Nenhuma" else (100, 100, 100)
                espessura = 3 if forma != "Nenhuma" else 1
                cv2.drawContours(frame_processado, [cnt_forma_global], -1, cor_forma, espessura)
            
            # Etapa 5: Prioriza o maior gabarito da cena (Trava de Foco)
            area = cv2.contourArea(corn)
            if area > candidato_area:
                candidato_area = area
                candidato_id = aruco_id
                candidato_forma = forma

    # =========================================================================
    # REPASSE PARA A MÁQUINA DE ESTADOS
    # =========================================================================
    # Etapa 6: Gerencia a Confirmação Temporal (ex: 5 Segundos sem piscar)
    if not rastreador.travado:
        # Se algum dos dois se perdeu nesse Exato MS, quebra o relógio inteiro
        if ids is None or candidato_id is None:
            rastreador.resetar()
        else:
            # Enviamos a forma primeiro porque ela rejeita 'Nenhuma' internamente na classe.
            rastreador.atualizar_leitura(candidato_forma, candidato_id)

    # -------------------------------------------------------------
    # FEEDBACK VISUAL FINAL NA TELA DO USUÁRIO
    # -------------------------------------------------------------
    # Se alcançou a quantidade de segundos reais de confirmação
    if rastreador.travado:
        forma_conf, id_conf = rastreador.obter_leitura_confirmada()
        msg_trava = f"ALVO TRAVADO COM SUCESSO! ID: {id_conf} | Gabarito: {forma_conf}"
        frame_processado = interagir_hub_principal(frame_processado, msg_trava, 20, 40, cor_fonte=(0, 255, 0))
    else:
        # Mostra os Segundos correndo
        val_sec = rastreador.obter_progresso() * rastreador.tempo_necessario
        if val_sec > 0.0:
            msg = f"Estabilizando ({val_sec:.1f}s / {rastreador.tempo_necessario}s): {candidato_forma} c/ ID {candidato_id}"
            frame_processado = interagir_hub_principal(frame_processado, msg, 20, 40, cor_fonte=(0, 255, 255))
        else:
            msg = f"Buscando Gabarito Estável... (Rejeitados: {qtd_rejeitados})"
            frame_processado = interagir_hub_principal(frame_processado, msg, 20, 40, cor_fonte=(200, 200, 200))
            
    # HUD FPS e Resolução
    info_cam = f"Res: {frame.shape[1]}x{frame.shape[0]}"
    frame_processado = escrever_texto_pillow(frame_processado, info_cam, 10, frame.shape[0] - 30, 16, (0, 255, 255))

    return frame_processado

# ============================================================================
# ESTADO DE EXECUÇÃO PRINCIPAL
# ============================================================================

def iniciar_teste():
    print("[MÓDULO - PASSO A | COM TEMPORIZADOR MODULAR] Iniciando Interface OpenCV...")
    print(" >>> Pressione [Q] para encerrar e fechar a visualização.\n")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERRO CRÍTICO] Falhou em abrir hardware da Câmera (Index=0).")
        return
        
    # Nasce o vigilante que exige 'TEMPO_CONFIRMACAO_GEOMETRIA' (Ex: 5.0) segundos ininterruptos
    tracker = EstabilizadorTemporal(tempo_necessario=TEMPO_CONFIRMACAO_GEOMETRIA)
        
    while True:
        status, frame = cap.read()
        if not status:
            break
            
        frame_anotado = observar_frame_single_step(frame, tracker)
        
        cv2.imshow("VISUALIZADOR ARUCO + LOCK ON 5S", frame_anotado)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    print("[MÓDULO - PASSO A] Finalizado com sucesso.")

if __name__ == '__main__':
    iniciar_teste()
