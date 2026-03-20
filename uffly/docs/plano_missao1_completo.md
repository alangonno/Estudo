# Planejamento da Missão 1: ArUco + State Machine

O objetivo da Missão 1 é aplicar uma lógica combinada de Visão Computacional de múltiplas etapas, estruturada como uma **Máquina de Estados (State Machine)**.

## 1. Parâmetros e Constantes (Regras da Competição)
- **ArUco Dictionary:** `cv2.aruco.DICT_5X5_1000` (IDs 0 a 999).
- **Tamanho Físico do ArUco:** `25.0 cm x 25.0 cm`.
- **Formas Geométricas Válidas:** Hexágono regular, Estrela de cinco pontas, Triângulo equilátero.
- **Divisores de Pouso (Bases):** 3, 4 ou 5.

## 2. Arquitetura Proposta: pipeline_missao1.py

O script será desenhado utilizando a estrutura de classes (ex: `Mission1Controller`), ou funções puras rodando num loop infinito `while True`, gerenciadas por uma variável de Estado.

### 2.1 Visão Computacional (Componentes)
- **`detectar_gabarito()`**: Utiliza `cv2.aruco.ArucoDetector` com `DICT_5X5_1000`. Ao achar o ArUco, expande a ROI para fora em busca do contorno envolvente. Classifica se é Hexágono (6 lados), Estrela (>8 lados/pontas) ou Triângulo (3 lados). Retorna `aruco_id` e `forma_gabarito`.
- **`detectar_bases_e_ler_ocr()`**: Varre a imagem buscando contornos fechados e números (3, 4 ou 5). Aplica Tesseract OCR. Retorna a forma base e o número.

### 2.2 Máquina de Estados (Lógica Central)
* **ESTADO 0: `BUSCANDO_GABARITO` (Passo A)**
  - Câmera busca um ArUco 5x5 e sua forma externa.
  - Salvou `TARGET_ID` e `TARGET_FORMA`? Transita para `BUSCANDO_BASES`.
* **ESTADO 1: `BUSCANDO_BASES` (Passo B e C)**
  - Foco exclusivo em contornos da base e OCR. Ignora ArUcos.
  - Verifica: `Forma_Base == TARGET_FORMA` E `TARGET_ID % Numero_Base == 0`.
  - Achou validado? Transita para `ALINHANDO_POUSO`.
* **ESTADO 2: `ALINHANDO_POUSO`**
  - Foca a bounding box na base vitoriosa. Estima altitude via trigonometria.
