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
   Somente após 5 segundos ininterruptos de leitura com sucesso o drone atesta o Gabarito.

Glossário de Termos Técnicos:
  - ArUco    : Augmented Reality University of Córdoba. Marcador fiducial quadrado
               preto-e-branco com padrão interno de bits que encoda um ID numérico.
  - ROI      : Region of Interest (Região de Interesse). Um recorte retangular de
               um frame — submatriz NumPy menor extraída da imagem original.
  - BGR      : Blue-Green-Red. Ordem padrão dos canais de cor no OpenCV
               (diferente do RGB convencional — OpenCV inverte os canais R e B).
  - Bounding Box: Caixa delimitadora. Retângulo mínimo que envolve completamente
               um objeto detectado, definido por (x_min, y_min, x_max, y_max).
  - State Machine: Máquina de Estados. Lógica que controla em qual estado o
               sistema está (ex: Buscando → Estabilizando → Travado), impedindo
               transições inválidas e garantindo consistência temporal.
  - Lock-On  : Travamento. Estado final da State Machine quando o alvo é confirmado
               com estabilidade suficiente (5s contínuos) para ser considerado válido.
"""

import cv2
import numpy as np
import time

# Reutilizando injeção funcional do seu projeto existente para overlay estético com acentuação
from identificar_distancia import escrever_texto_pillow

# ============================================================================
# CONSTANTES DE CONFIGURAÇÃO BASE
# ============================================================================
# DICT_5X5_1000: Dicionário ArUco com marcadores de malha 5x5 bits, suportando até 1000 IDs únicos.
DICIONARIO_COMPETICAO = cv2.aruco.DICT_5X5_1000

_aruco_dict = cv2.aruco.getPredefinedDictionary(DICIONARIO_COMPETICAO)
_aruco_params = cv2.aruco.DetectorParameters()  # Parâmetros padrão de detecção (limiar, adaptativo, etc.)
DETECTOR_ARUCO = cv2.aruco.ArucoDetector(_aruco_dict, _aruco_params)

# ============================================================================
# CLASSES DE DOMÍNIO (STATE MACHINE / TEMPORIZADOR)
# ============================================================================

class RastreadorGabarito:
    """
    Classe focada exclusivamente em lidar com Temporizadores (Cronômetro de Estabilidade).
    Isola a lógica do cronômetro de 5s evitando variáveis globais e spaghettis no OpenCV.
    """
    def __init__(self, tempo_necessario=5.0):
        self.alvo_id = None
        self.alvo_forma = "Nenhuma"
        self.inicio_captura = 0.0
        self.tempo_necessario = tempo_necessario
        self.travado = False

    def atualizar_leitura(self, aruco_id, forma_lida):
        # Se o sistema já atestou e travou o alvo final durante 5 segundos, não avalia mais.
        if self.travado:
            return

        # Para iniciar o cronômetro, exigimos o ArUco lido e uma Forma real ("Nenhuma" aborta).
        if forma_lida == "Nenhuma" or aruco_id is None:
            self.resetar()
            return

        # Constância Constatada: Se o ID e a Forma lida agora forem idênticas ao frame passado
        if aruco_id == self.alvo_id and forma_lida == self.alvo_forma:
            tempo_decorrido = time.time() - self.inicio_captura
            if tempo_decorrido >= self.tempo_necessario:
                self.travado = True
                print(f"[STATE MACHINE COMPLETED] GABARITO LOCK: ID={self.alvo_id} | Forma={self.alvo_forma}")
        else:
            # Quebra de Consistência Temporal: Novo ID, formato que distorceu, ou leitura zero
            self.alvo_id = aruco_id
            self.alvo_forma = forma_lida
            self.inicio_captura = time.time()

    def obter_progresso(self):
        """Retorna os segundos contínuos acumulados"""
        if self.alvo_id is None or self.alvo_forma == "Nenhuma":
            return 0.0
        return min(time.time() - self.inicio_captura, self.tempo_necessario)

    def resetar(self):
        """Quebra instantânea da integridade (perda de rastreio em tela)"""
        if self.alvo_id is not None:
            self.alvo_id = None
            self.alvo_forma = "Nenhuma"
            self.inicio_captura = 0.0


# ============================================================================
# LÓGICAS MESTRE (COMPUTER VISION PURA)
# ============================================================================

def extrair_roi_expandida(frame, cantos_aruco, margem_percentual=1.35):
    """
    Recebe os limites exatos do ArUco em pixels e devolve a ROI expandida.

    ROI (Region of Interest): recorte retangular do frame — submatriz NumPy
    menor que representa apenas a área relevante da imagem, evitando processar
    o frame inteiro e reduzindo falsos positivos de outras regiões da cena.

    Bounding Box: o retângulo mínimo que contém o ArUco, calculado a partir
    dos 4 cantos detectados (x_min, y_min) → (x_max, y_max).
    """
    pts = cantos_aruco[0].astype(int)
    # Bounding Box mínima: extremos dos 4 cantos do ArUco em pixels
    x_min, y_min = np.min(pts, axis=0)
    x_max, y_max = np.max(pts, axis=0)
    
    largura = x_max - x_min
    altura = y_max - y_min
    
    # Padding: expansão em pixels ao redor da Bounding Box para cobrir a forma geométrica
    pad_x = int(largura * margem_percentual)
    pad_y = int(altura * margem_percentual)
    
    # Clamp: garante que as coordenadas não ultrapassem os limites do frame (evita IndexError)
    altura_frame, largura_frame = frame.shape[:2]
    x_ini = max(0, x_min - pad_x)
    y_ini = max(0, y_min - pad_y)
    x_fim = min(largura_frame, x_max + pad_x)
    y_fim = min(altura_frame, y_max + pad_y)
    
    # Fatiagem NumPy: extrai a ROI como submatriz [linhas, colunas] do frame original
    roi = frame[y_ini:y_fim, x_ini:x_fim]
    return roi, x_ini, y_ini

def classificar_geometria_gabarito(roi_bgr):
    """
    Pipeline de visão computacional aplicado sobre a ROI (Region of Interest).
    Etapas: BGR→Cinza → GaussianBlur → Canny → MORPH_CLOSE → findContours → ApproxPolyDP

    Parâmetro:
      roi_bgr : imagem recortada no espaço de cor BGR
                (BGR = Blue-Green-Red, padrão OpenCV — ordem invertida do RGB clássico)

    Classificações Suportadas: Triângulo(3 vértices), Hexágono(6), Estrela(>=8 côncava).
    """
    if roi_bgr.size == 0:
        return "Nenhuma", None

    # BGR2GRAY: converte os 3 canais de cor (B, G, R) para 1 canal de luminância.
    # Bordas são definidas por contraste de brilho, não de cor.
    cinza = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)

    # GaussianBlur: suaviza ruído de alta frequência antes do Canny.
    # Kernel (5,5) = área de influência; sigma=0 = calculado automaticamente.
    borrada = cv2.GaussianBlur(cinza, (5, 5), 0)

    # Canny (Eduard Canny, 1986): detecta bordas por gradiente de intensidade.
    # 50 = limiar inferior (pixel candidato a borda); 150 = limiar superior (borda forte).
    # Pixels entre os limiares só viram borda se conectados a uma borda forte.
    bordas = cv2.Canny(borrada, 50, 150)

    # MORPH_CLOSE (Fechamento Morfológico): dilata depois erode.
    # Fecha gaps e une bordas quebradas causadas por reflexo ou impressão irregular.
    # kernel (3,3) = elemento estruturante; iterations=2 = aplica a operação 2 vezes.
    kernel = np.ones((3, 3), np.uint8)
    bordas = cv2.morphologyEx(bordas, cv2.MORPH_CLOSE, kernel, iterations=2)

    # RETR_EXTERNAL: recupera apenas os contornos mais externos (ignora "buracos" internos).
    # CHAIN_APPROX_SIMPLE: comprime segmentos horizontais/verticais/diagonais
    #   guardando apenas os pontos extremos — economiza memória sem perder forma.
    contornos, _ = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        return "Nenhuma", None
        
    maior_contorno = max(contornos, key=cv2.contourArea)
    area = cv2.contourArea(maior_contorno)
    
    # Filtro de área mínima: ignora detecções imperceptíveis (ruído, poeira, compressão JPEG)
    if area < 500: 
        return "Nenhuma", None

    perimetro = cv2.arcLength(maior_contorno, True)

    # ApproxPolyDP (Douglas-Peucker): simplifica o contorno trêmulo do papel impresso
    # em um polígono de vértices nítidos. epsilon = tolerância de desvio em pixels
    # (2% do perímetro = equilibrio entre suavização e fidelidade à forma real).
    epsilon = 0.02 * perimetro
    approx = cv2.approxPolyDP(maior_contorno, epsilon, True)
    vertices = len(approx)
    
    # Lógicas Condicionais Diretas (Conforme especificações da competição)
    if vertices == 3:
        return "Triângulo", maior_contorno
    elif vertices == 6:
        return "Hexágono", maior_contorno
    else:
        # A forma de "Estrela" comumente possui mais de 5 pontos no "approxPolyDP"
        # Além disso, estrelas garantidamente possuem cascos "não-convexos"
        e_convexa = cv2.isContourConvex(approx)
        if vertices >= 8 and not e_convexa:
            return "Estrela", maior_contorno
            
    return "Nenhuma", maior_contorno


def interagir_hub_principal(frame, texto, ancora_x, ancora_y, cor_fonte=(255, 255, 0)):
    """Auxiliar limpo para envelopar desenho via Pillow"""
    return escrever_texto_pillow(
        frame_bgr=frame, 
        texto=texto, 
        x=ancora_x, 
        y=ancora_y, 
        tamanho=24, 
        cor=cor_fonte, 
        stroke=2, stroke_cor=(0, 0, 0)
    )

def observar_frame_single_step(frame, rastreador):
    """
    Orquestra a visão de um único quadro e manipula as regras de travamento de estado.
    """
    frame_processado = frame.copy()
    
    # Core: Busca Direta dos ArUcos
    corners, ids, rejected = DETECTOR_ARUCO.detectMarkers(frame_processado)
    
    # -------------------------------------------------------------
    # DEBUG BÁSICO - Rejeições (Falsos ArUcos vistos porém borrados)
    # -------------------------------------------------------------
    qtd_rejeitados = len(rejected) if rejected is not None else 0
    if qtd_rejeitados > 0:
        cv2.aruco.drawDetectedMarkers(frame_processado, rejected, borderColor=(0, 0, 255))
        
    # Armazena qual ArUco dessa iteração é mais provável ser o nosso gabarito
    candidato_id = None
    candidato_forma = "Nenhuma"
    candidato_area = 0
    
    if ids is not None and len(ids) > 0:
        cv2.aruco.drawDetectedMarkers(frame_processado, corners, ids)
        
        # Iterar sobre ArUcos encontrados para varrer o chão do gabinete
        for index in range(len(ids)):
            aruco_id = ids[index][0]
            corn = corners[index]
            
            roi_expandida, roi_x, roi_y = extrair_roi_expandida(frame, corn, margem_percentual=1.35)
            forma, cnt_forma = classificar_geometria_gabarito(roi_expandida)
            
            # [ESTÉTICA/DEBUG] Desenha Caixas de Busca (Amarelo) e Formas de Leitura (Verde)
            roi_h, roi_w = roi_expandida.shape[:2]
            cv2.rectangle(frame_processado, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 255, 255), 2)
            
            if cnt_forma is not None:
                # Transladando o contorno de coordenadas locais(ROI) para coordenadas globais(Frame)
                cnt_forma_global = cnt_forma + [roi_x, roi_y]
                
                # Verde forte se for válido (Triângulo, Hexágono, etc), Cinza se "Nenhuma" for compreendida
                cor_forma = (0, 255, 0) if forma != "Nenhuma" else (100, 100, 100)
                espessura = 3 if forma != "Nenhuma" else 1
                cv2.drawContours(frame_processado, [cnt_forma_global], -1, cor_forma, espessura)
            
            # Consideramos como Alvo Preferencial o Gabarito maior desenhado em tela
            area = cv2.contourArea(corn)
            if area > candidato_area:
                candidato_area = area
                candidato_id = aruco_id
                candidato_forma = forma

    # =========================================================================
    # REPASSE PARA A MÁQUINA DE ESTADOS E TRATATIVAS DO TEMPORIZADOR
    # =========================================================================
    
    # Apenas enviamos a atualização do frame se ainda não tivermos travado sucesso de 5s
    if not rastreador.travado:
        if ids is None or candidato_id is None:
            # Reseta na hora, sumiu por 1 ms. Trepidou = perdeu estabilidade e timer atrito
            rastreador.resetar()
        else:
            rastreador.atualizar_leitura(candidato_id, candidato_forma)

    # -------------------------------------------------------------
    # FEEDBACK VISUAL FINAL NA TELA DO USUÁRIO
    # -------------------------------------------------------------
    if rastreador.travado:
        # TELA DE LOCK-ON E FIM DE GABARITO (Passo B autorizado na arquitetura final)
        msg_trava = f"ALVO TRAVADO COM SUCESSO! ID: {rastreador.alvo_id} | Gabarito: {rastreador.alvo_forma}"
        frame_processado = interagir_hub_principal(frame_processado, msg_trava, 20, 40, cor_fonte=(0, 255, 0))
    else:
        # TELA DE CARREGAMENTO / BUSCA DE ESTABILIZADADE
        val = rastreador.obter_progresso()
        if val > 0.0:
            msg = f"Estabilizando ({val:.1f}s / {rastreador.tempo_necessario}s): {candidato_forma} c/ ID {candidato_id}"
            frame_processado = interagir_hub_principal(frame_processado, msg, 20, 40, cor_fonte=(0, 255, 255))
        else:
            msg = f"Buscando Gabarito Estável... (Rejeitados: {qtd_rejeitados})"
            frame_processado = interagir_hub_principal(frame_processado, msg, 20, 40, cor_fonte=(200, 200, 200))
            
    # FPS e Resolution Debug
    info_cam = f"Res: {frame.shape[1]}x{frame.shape[0]}"
    frame_processado = escrever_texto_pillow(frame_processado, info_cam, 10, frame.shape[0] - 30, 16, (0, 255, 255))

    return frame_processado

# ============================================================================
# ESTADO DE EXECUÇÃO PRINCIPAL
# ============================================================================

def iniciar_teste():
    print("[MÓDULO - PASSO A | COM TEMPORIZADOR] Iniciando Interface OpenCV...")
    print(" >>> Pressione [Q] para encerrar e fechar a visualização.\n")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERRO CRÍTICO] Falhou em abrir hardware da Câmera (Index=0).")
        return
        
    # Inicializa nosso Gestor Isolado de Estados Puros (Passa param customizado se precisar ex: 5.0)
    tracker = RastreadorGabarito(tempo_necessario=5.0)
        
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
