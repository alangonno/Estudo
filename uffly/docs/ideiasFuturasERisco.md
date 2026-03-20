# Ideias Futuras e Riscos Conhecidos

Documento de referência para melhorias, riscos e alternativas mapeadas durante o desenvolvimento da visão computacional da Missão 1.

---

## 1. Riscos de Iluminação no Dia da Competição

O `adaptiveThreshold` que usamos no `leitor_bases_isolado.py` já cobre boa parte dos cenários, mas existem situações extremas que precisam de atenção:

### Cenários e Riscos

| Cenário | Risco | Solução no dia |
|---|---|---|
| **Sol forte direto** | Reflexo estourado pontual no papel (zona branca sem contraste) | Inclinar a base ou mudar ângulo de abordagem |
| **Sombra do próprio drone** | Metade clara, metade escura sobre a base | Já coberto pelo adaptiveThreshold |
| **Ambiente escuro** (noturno/galpão fechado) | Câmera não capta contraste suficiente | Ajustar exposure/brightness da câmera |
| **Contraluz** (sol atrás da base) | Silhueta da base sem detalhes internos | Compensar com exposure negativo |

### Ideia Futura: Presets de Iluminação (`MODO_ILUMINACAO`)

Criar uma constante no topo do arquivo com presets prontos, onde no dia da competição basta trocar uma string:

```python
MODO_ILUMINACAO = "normal"  # Opções: "sol", "sombra", "noturno"

PRESETS = {
    "sol":     {"blockSize": 51, "C": 8, "exposure": -5},
    "normal":  {"blockSize": 31, "C": 4, "exposure": 0},
    "sombra":  {"blockSize": 31, "C": 3, "exposure": 0},
    "noturno": {"blockSize": 21, "C": 2, "exposure": 5},
}
```

Também é possível ajustar a câmera do Raspberry Pi diretamente no dia:
```python
cap.set(cv2.CAP_PROP_EXPOSURE, -5)    # negativo = sol forte
cap.set(cv2.CAP_PROP_BRIGHTNESS, 60)  # 0-100, aumentar se escuro
```

### Riscos Atuais do Sistema

- **Template Matching é sensível a rotação extrema**: Se a base estiver rotacionada mais de ~30°, o template retangular perde correlação. No voo real o drone olha de cima para baixo, então esse risco é baixo.
- Formas desenhadas à mão (não impressas) podem ter vértices irregulares que confundam o `approxPolyDP`.
- Estrelas com pontas muito finas podem ter solidity baixo e serem filtradas pelo limiar atual (`SOLIDITY_MIN = 0.70` ou `0.40`).
- **Erro na leitura correta de numeros:** Testado pela tela de celular porem nao obteve resultado satisfatorio. Muitas vezes trocando o numero 5 por 3 , mesmo usando a fonte corretamente, tentar usar em um fundo neutro com uma folha de papel simulando altura do drone para ver se funcionaria melhor. 

### Ideia Futura: Máscara Inversa (Fundo Preto) com Templates Exatos

Testar um algoritmo invertendo as imagens do leitor (`THRESH_BINARY_INV` + Otsu) de modo que o fundo da folha virasse 0 (Preto) e apenas o número fosse 255 (Branco). O objetivo sera forçar na matemática ($255 \times 255$) uma nota altíssima apenas para números de traços idênticos, anulando a penalidade ou bônus causado pelo fundo branco do papel.
- **Solução Futura:** Se extrairmos arquivos `.png` exatos direto do arquivo SVG da competição e usarmos como os nossos templates base (eliminando o Pillow), poderemos reativar a lógica do Fundo Negro. Testado com folhas brancas em um fundo neutro, isso trará talvez uma taxa melhor de acerto ao OCR numérico.

---

## 2. Alternativas de OCR Descartadas

### Tesseract OCR (DESCARTADO ❌)

**Motivo:** Consome ~98% da CPU do Raspberry Pi, 100-300ms por frame, e exige instalação do engine separado (`tesseract-ocr`). Para ler **apenas** 3 dígitos (`3`, `4`, `5`) impressos em Arial, o `cv2.matchTemplate` faz o mesmo em ~1-5ms sem dependência externa.

### EasyOCR (NÃO AVALIADO)

Requer PyTorch inteiro. Inviável no Raspberry Pi (~2GB de dependências).

### kNN / SVM do OpenCV (NÃO IMPLEMENTADO)

Exigiria criar dataset de treino. Como os dígitos da competição são em fonte fixa (Arial Regular), o Template Matching é mais direto e confiável.

---

## 3. Opções Alternativas de Filtro (Pesquisa Arquivada)
### Opção 1 — Filtros em Cascata por Propriedades do Contorno (IMPLEMENTADA ✅)

Métricas do OpenCV aplicadas **em sequência** para eliminar falsos positivos:

| Métrica | Cálculo | O que elimina |
|---|---|---|
| **Área** | `cv2.contourArea(cnt)` | Ruídos pequenos e bordas da folha inteira |
| **Solidity** | `area / cv2.contourArea(hull)` | Formas irregulares, sombras, texturas |
| **Aspect Ratio** | `w / h` via `boundingRect` | Linhas, bordas, objetos muito alongados |
| **Extent** | `area / (w * h)` | Formas muito esparsas e abertas | #Não Implementado

Filtros sugeridos para triângulo/hexágono/estrela:
- `solidity > 0.75`
- `0.5 <= aspect_ratio <= 2.0`
- `area entre 2000 e 200000 px`

### Opção 2 — Threshold Adaptativo (IMPLEMENTADA ✅)

O problema com Canny global é que iluminação variável (como numa sala) cria falsos positivos. A pesquisa recomenda usar cv2.adaptiveThreshold() antes de buscar contornos, pois ele ajusta o threshold localmente por região, ideal para papel iluminado de forma desigual.

```python
bin_img = cv2.adaptiveThreshold(
    gray, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    blockSize=31, C=5
)
```

### Opção 3 — Máscara HSV de Papel Branco/Claro

Criar uma máscara que isola apenas regiões de alta luminância (papel branco) antes de buscar contornos. O chão, mesas escuras e o ambiente são filtrados automaticamente.

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mascara_branco = cv2.inRange(hsv, (0, 0, 180), (180, 60, 255))
```

**Limitação:** Depende de iluminação consistente.

