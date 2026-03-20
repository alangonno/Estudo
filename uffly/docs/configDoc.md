# Documentação: Configuração Global (config.py)
**Caminho:** `config.py`

O arquivo `config.py` concentra todas as variáveis "soltas" e mágicas que afetam o comportamento puramente matemático e visual do OpenCV. Ele serve como o **Painel de Controle** da Missão 1.

No dia da competição, toda e qualquer adaptação ao ambiente (Sol mais forte, câmera mais longe do solo, distorção de cores) deve começar avaliando os valores definidos aqui.

---

## 1. Parâmetros Gerais e HUD
Define as cores usadas pelo sistema para apresentar o texto na tela do computador.
- **`COR_TEXTO_SUCESSO`**: Cor do "ALVO TRAVADO COM SUCESSO" (Verde).
- **`COR_TEXTO_AVISO`**: Cor para rastreamento estabilizando (Amarelo).

## 2. Configurações dos Estabilizadores Temporais
Substitui a antiga contagem falha de "Frames" exigida para aprovar uma leitura, passando a usar Segundos reais do relógio do Raspberry Pi.
- **`TEMPO_CONFIRMACAO_GEOMETRIA (5.0)`**: Segundos ininterruptos lendo a mesma Forma + ArUco no Passo A para atestar "Lock-On".
- **`TEMPO_CONFIRMACAO_BASES (0.5)`**: Segundos ininterruptos no Passo B/C para confirmar um dígito lido (evita flutuar entre '3' e '4' num mesmo segundo).

## 3. Configurações de ArUco
- **`ARUCO_DICIONARIO`**: Define que os marcadores da competição usam dicionário `DICT_5X5_1000`.
- **`ARUCO_MARGEM_PERCENTUAL (1.35)`**: Multiplica a Bounding Box preta do ArUco para capturar a folha de 800mm ao seu redor inteira. Aumente este valor se a câmera perder as bordas da base por estar muito perto do chão.

## 4. Geometria (Triângulos, Hexágonos, Estrelas)
- **`GEOMETRIA_AREA_MIN_PX (500)`**: Descarta manchas minúsculas de sombra do chão.
- **`GEOMETRIA_CANNY_LOWER / UPPER`**: Limiares do detector de bordas Canny. Importante calibrar no dia se o contraste do chão/papel mudar.
- **`GEOMETRIA_EPSILON_MULT (0.015)`**: Suavizador de curvas do OpenCV. NUNCA suba acima de 0.02 ou as pontas da estrela serão interpretadas como linhas retas.
- **`GEOMETRIA_ESTRELA_VALEDEPTH_PERC (0.15)`**: Um "Vale" da estrela precisa ter 15% do tamanho total da forma para o código confirmar que não é apenas um papel amassado ou um celular.

## 5. Leitor de Bases Gerais
- **`BASES_AREA_MIN / MAX`**: Tamanho mínimo/máximo do polígono lido para o passo C.
- **`BASES_ASPECT_RATIO_MIN / MAX`**: Bloqueia fitas verticais ou linhas horizontais do piso de serem interpretadas como formas geométricas.
- **`BASES_SOLIDITY_MIN (0.40)`**: Proteção de densidade. Fixado em ~40% para acolher a variação do Hexágono Pálido e da Estrela Esquelética.
- **`BASES_THRESH_BLOCK_SIZE / THRESH_C`**: Afinam o quão severo e isolado é o *AdaptiveThreshold* com sombras. `BLOCK_SIZE` deve ser obrigatoriamente Ímpar.

## 6. Template Matching dos Dígitos
- **`BASES_SCORE_MINIMO_TEMPLATE (0.45)`**: O rigor matemático (0 a 1) para aprovar o match OCR de um dígito. Como a matemática se sobrepõe puramente nas linhas brancas sem penalidade do fundo de papel (devido ao invert da binarização), `0.45` filtra as oscilações.
- **`BASES_ESCALAS_TEMPLATE`**: Escalonadores simulando tamanho real; adiciona decibéis baixos (`0.2`) se a câmera do drone subir muito, lendo dígitos distantes.
