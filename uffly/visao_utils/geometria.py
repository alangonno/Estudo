import cv2
import numpy as np
from config import *

def classificar_geometria_gabarito(roi_bgr):
    """
    Pipeline de visão computacional independente aplicado sobre a ROI (Region of Interest).
    Analisa bordas e morfologia para atestar puramente "Qual forma é?".
    
    Etapas: BGR→Cinza → GaussianBlur → Canny → MORPH_CLOSE → findContours → ApproxPolyDP
    Resultados Retornados: 
        ("Triângulo" | "Hexágono" | "Estrela" | "Nenhuma", [contorno numpy visual])
    """
    if roi_bgr.size == 0:
        return "Nenhuma", None

    # Processamento padrão BGR->Cinza e Canny (Limiares Dinâmicos puxados da Config)
    cinza = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)
    borrada = cv2.GaussianBlur(cinza, (5, 5), 0)
    bordas = cv2.Canny(borrada, GEOMETRIA_CANNY_LOWER, GEOMETRIA_CANNY_UPPER)

    # Fechando pequenos gaps das linhas desenhadas
    kernel = np.ones((3, 3), np.uint8)
    bordas = cv2.morphologyEx(bordas, cv2.MORPH_CLOSE, kernel, iterations=2)

    contornos, _ = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        return "Nenhuma", None
        
    maior_contorno = max(contornos, key=cv2.contourArea)
    area = cv2.contourArea(maior_contorno)
    
    # Filtro Primário
    if area < GEOMETRIA_AREA_MIN_PX: 
        return "Nenhuma", None

    perimetro = cv2.arcLength(maior_contorno, True)

    # ApproxPolyDP amacia os traços do polígono do Papel 
    epsilon = GEOMETRIA_EPSILON_MULT * perimetro
    approx = cv2.approxPolyDP(maior_contorno, epsilon, True)
    vertices = len(approx)
    
    if vertices == 3:
        return "Triângulo", maior_contorno
    elif vertices == 6:
        return "Hexágono", maior_contorno
    else:
        # Complexidade para classificar Estrela Exata
        e_convexa = cv2.isContourConvex(approx)
        if not e_convexa and 8 <= vertices <= 14:
            hull_indices = cv2.convexHull(approx, returnPoints=False)
            try:
                defects = cv2.convexityDefects(approx, hull_indices)
            except:
                defects = None
                
            if defects is not None:
                _, _, w, h = cv2.boundingRect(approx)
                limiar_profundidade = (min(w, h) * GEOMETRIA_ESTRELA_VALEDEPTH_PERC) * 256.0 
                
                vales_profundos = 0
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    if d > limiar_profundidade:
                        vales_profundos += 1
                
                # Aceitamos de 4 a 5 vales precisos (Uma estrela real de 5 pontas gerará sempre 5 vales, mas 4 cobre inclinação/culling)
                if vales_profundos >= 4:
                    return "Estrela", maior_contorno
            
    return "Nenhuma", maior_contorno
