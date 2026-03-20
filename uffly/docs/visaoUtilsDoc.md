# Documentação: Biblioteca de Visão Utilitária (visao_utils/)
**Caminho:** `visao_utils/`

Este pacote agrupa todas as rotinas brutas reutilizáveis de Matemática, Visão Computacional Genérica e Estados Temporais do nosso drone. Os arquivos de Passos operacionais importam os dados daqui para evitar Código "Miojo" (Espaguete).

---

## 1. Módulo de Geometria (`geometria.py`)
Módulo focado apenas nas propriedades matemáticas e linhas do OpenCV puro.
*Consome configurações de: `config.py` (Seção 4: Geometria).*

### `classificar_geometria_gabarito(roi_bgr)`
Avalia os traços de uma sub-imagem isolada (ROI) pelo OpenCV.
**Pipeline Executado:**
`BGR→Cinza` → `GaussianBlur` → `Canny` → `MORPH_CLOSE` → `findContours` → `ApproxPolyDP` → **conta vértices e vales (defeitos)**

**Resultados Retornados:** 
- `("Triângulo", contorno_visual)`
- `("Hexágono", contorno_visual)`
- `("Estrela", contorno_visual)` (Possui exigência complexa de *ConvexityDefects*, confirmando ao menos 4 reentrâncias afiadas proporcionais)
- `("Nenhuma", contorno_visual)`

---

## 2. Módulo Estabilizador (`estabilizador.py`)
Resolve o problema crônico de tremedeiras (perda de detecção de um frame pro outro) baseado no Clock nativo, independente de Framerate alto ou baixo da câmera nativa do Raspberry Pi.

### `EstabilizadorTemporal(tempo_necessario)`
Máquina de Estados de validação unificada. Interage por uma injeção de parâmetros (ex: Forma Geométrica + Dígito / ID de ArUco).
- **Coração Ininterrupto:** Se a Visão retornar dados inválidos por 1ms, o cronômetro despenca e aborta o "Lock-On" iminente via `resetar()`.
- **`atualizar_leitura(primario, secundario)`**: Injeta o dado frame-a-frame visando o travamento do target.
- **`obter_progresso()`**: Devolve a % do cronômetro para exibição estética nas barras de carregamento da interface.
- **`obter_leitura_confirmada()`**: Método terminal que só atesta que o drone reconheceu o objeto se e somente se tempo de checagem chegou no limite requisitado no `config.py`.

---

## 3. Módulo Interface/HUD (`hud.py`)
Abstrai os painéis e textos desenhados na cara da Câmera pelo OpenCV, que por padrão não lida com Acentuações e Fontes modernas.

### `escrever_texto_pillow`
Ao invés do falho `cv2.putText`, instanciamos o `ImageDraw` da biblioteca `PIL (Pillow)` no background do NumPy, redigindo com a fonte do projeto (Arial) e com strokes (bordas pretas para melhorar a legibilidade de textos brancos sob superfícies claras).
