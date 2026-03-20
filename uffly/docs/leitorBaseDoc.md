# Documentação Técnica: `leitor_bases_isolado.py`

Script responsável pelo **Passo B/C** da Missão 1. Ele varre a câmera em tempo real buscando formas geométricas (Triângulo, Hexágono, Estrela) que contenham os dígitos `3`, `4` ou `5` no centro — as bases de pouso.

## 1. Glossário de Termos

| Termo | Significado |
|---|---|
| **AdaptiveThreshold** | Binarização que calcula o limiar localmente por região, em vez de valor fixo global. Ideal para iluminação desigual. |
| **Solidity (Solidez)** | Razão área real / área do casco convexo. Formas regulares ≈ 1.0, irregulares < 0.5. |
| **Casco Convexo (Convex Hull)** | Menor polígono convexo que envolve um contorno. Como um elástico esticado ao redor dos pontos. |
| **Aspect Ratio** | Largura ÷ altura da bounding box. Forma simétrica ≈ 1.0, linha horizontal > 5.0. |
| **Bounding Box** | Menor retângulo alinhado aos eixos que envolve um contorno. |
| **ROI (Region of Interest)** | Recorte retangular focado em uma área específica da imagem. |
| **Template Matching** | Técnica do OpenCV que desliza uma imagem pequena (template) sobre outra maior e calcula a similaridade pixel a pixel. Retorna a posição e o score de correlação. |
| **TM_CCOEFF_NORMED** | Método de correlação cruzada normalizada usado no template matching. Score varia de -1.0 a 1.0, onde 1.0 = match perfeito. |
| **Multi-escala** | Testar o template em múltiplos tamanhos para cobrir variação de distância câmera-base. |
| **MORPH_CLOSE** | Dilatação + erosão. Fecha lacunas entre bordas próximas sem alterar tamanho dos objetos. |
| **Contorno** | Curva fechada detectada por `cv2.findContours` sobre imagem binarizada. |
| **approxPolyDP** | Simplifica contorno curvo para polígono. 3 vértices = triângulo, 6 = hexágono, etc. |

---

## 2. Constantes Configuráveis

- **`AREA_MIN` / `AREA_MAX`**: Limites de área em pixels. Contornos menores que 2000px são ruído; maiores que 200.000px são a borda da folha inteira.
- **`SOLIDITY_MIN`**: Limiar de solidez. Formas regulares (triângulo, hexágono) ficam acima de 0.70. Sombras e texturas ficam abaixo.
- **`ASPECT_RATIO_MIN` / `ASPECT_RATIO_MAX`**: Razão largura/altura. Elimina linhas longas e bordas esticadas que passariam os filtros de área.
- **`SCORE_MINIMO_TEMPLATE`**: Score mínimo do template matching para aceitar leitura (0.45).

---

## 3. Funções e Responsabilidades

### Geração de Templates

#### `_gerar_template_digito(digito, tamanho_fonte, largura, altura)`
- **Chama:** `PIL.Image`, `PIL.ImageDraw`, `PIL.ImageFont`
- **O que faz:** Gera uma imagem binária (fundo branco, dígito preto) usando fonte **Arial Regular** via Pillow. Reproduz a aparência exata dos dígitos da competição.

#### `carregar_templates()`
- **Chama:** `_gerar_template_digito`
- **O que faz:** Gera os 3 templates (`3`, `4`, `5`) uma única vez na inicialização. Retorna dicionário `{'3': img, '4': img, '5': img}`.

### Pré-processamento

#### `segmentar_frame(frame)`
- **Chama:** `cv2.cvtColor`, `cv2.GaussianBlur`, `cv2.adaptiveThreshold`, `cv2.morphologyEx`
- **O que faz:** Recebe o frame colorido da câmera e devolve uma imagem binária (preto e branco) onde as bordas dos objetos são brancas. Usa AdaptiveThreshold em vez de Canny para adaptar-se a variações locais de iluminação.

### Filtros de Contorno

#### `calcular_solidity(contorno)`
- **Chama:** `cv2.contourArea`, `cv2.convexHull`
- **O que faz:** Calcula a razão entre a área real do contorno e a área do menor polígono convexo que o envolve (casco convexo). Um hexágono perfeito retorna ~1.0. Uma sombra irregular retorna ~0.3.

#### `calcular_aspect_ratio(contorno)`
- **Chama:** `cv2.boundingRect`
- **O que faz:** Divide a largura pela altura da caixa retangular que contém o contorno. Formas simétricas ficam próximas de 1.0. Linhas horizontais retornam valores maiores que 3.0.

#### `filtrar_contornos_por_propriedades(contornos)`
- **Chama:** `calcular_solidity`, `calcular_aspect_ratio`, `cv2.contourArea`
- **O que faz:** Aplica os 3 filtros em sequência (Área → Solidez → Aspect Ratio). Cada filtro elimina uma categoria diferente de falso positivo. Retorna os candidatos ordenados do maior para o menor.

### Leitura de Número (Template Matching)

#### `extrair_roi_interna(frame, contorno, margem=0.22)`
- **O que faz:** Recorta o miolo do contorno com margem negativa para excluir as linhas do polígono.

#### `identificar_digito_por_template(roi_gray, templates)`
- **Chama:** `cv2.resize`, `cv2.matchTemplate`, `cv2.minMaxLoc`
- **O que faz:** Desliza cada template (3, 4, 5) pela ROI em **3 escalas diferentes** (40%, 60%, 80%). Retorna o dígito com maior score de correlação (se acima do limiar).

#### `extrair_digito_base(roi_bgr, templates)`
- **Chama:** `cv2.cvtColor`, `identificar_digito_por_template`
- **O que faz:** Converte ROI para cinza e delega para o template matching. Retorna `'3'`, `'4'`, `'5'` ou `None`.

### Orquestração e Estabilidade

#### `EstabilizadorLeitura(frames_necessarios)`
- **O que faz:** Impede oscilações de detecção. Confirma a leitura do dígito e forma apenas após 15 frames consecutivos idênticos. **Trava de Segurança:** Se o classificador retornar que não viu "Nenhuma" base no frame, a contagem e a memória do estabilizador são zeradas imediatamente, garantindo que o drone entenda que perdeu o alvo.

#### `observar_frame_bases(frame, templates, estabilizador)`
- **O que faz:** Pipeline completo: Segmenta → Contornos → Filtra → Classifica forma → Template Matching → HUD visual. **Trava de Alvo:** O pipeline varre do maior para o menor contorno e envia apenas o **MAIOR alvo válido** da cena para o `EstabilizadorLeitura`, ignorando bases menores ao fundo para não reiniciar a contagem.

#### `iniciar_teste()`
- **O que faz:** Gera templates na inicialização, instancia o `EstabilizadorLeitura`, liga câmera, roda loop e escuta `Q`.

---

## 4. Código Reaproveitado (Imports)

| Função | Origem | Motivo |
|---|---|---|
| `escrever_texto_pillow()` | `identificar_distancia.py` | Texto com acentos na tela |
| `classificar_geometria_gabarito()` | `leitor_aruco_isolado.py` | Classificar forma sem duplicar lógica |
