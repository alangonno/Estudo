# Documentação Técnica: `leitor_aruco_isolado.py`

Este script é o **Passo A da Missão 1** do drone. Ele liga a câmera, procura um marcador ArUco impresso no chão, lê o número (ID) dele e identifica qual forma geométrica está desenhada ao redor — Triângulo, Hexágono ou Estrela.

---

## Glossário Rápido

Termos técnicos que aparecem ao longo do código e desta documentação:

| Termo | Em palavras simples |
|-------|---------------------|
| **ArUco** | Um QR Code quadrado preto-e-branco feito para ser lido por câmeras de drone. Cada um tem um número (ID) único embutido nos quadradinhos internos. O nome vem de *Augmented Reality University of Córdoba*, onde foi criado. |
| **Frame** | Uma foto tirada pela câmera naquele exato instante. O loop do código processa dezenas deles por segundo (FPS). |
| **ROI** *(Region of Interest)* | Um recorte de um frame — uma foto menor dentro da foto maior. Usamos para focar a análise só na área importante, sem varrer a imagem inteira. |
| **Bounding Box** | O menor retângulo imaginário que consegue cercar um objeto na tela. Usamos os seus 4 cantos para saber onde o ArUco está. |
| **BGR** | A ordem das cores no OpenCV: Azul → Verde → Vermelho. É o inverso do RGB que estamos acostumados. Isso não muda nada visualmente, mas é importante saber quando converter cores no código. |
| **Canny** | Um algoritmo de 1986 que encontra as bordas/contornos de objetos numa imagem, detectando onde os pixels mudam bruscamente de claro para escuro. |
| **ApproxPolyDP** | Algoritmo que "limpa" um contorno tremido e irregular, transformando-o num polígono com vértices nítidos. Com ele, basta contar os vértices para saber a forma. |
| **MORPH_CLOSE** | Uma operação que "costura" brechas em bordas quebradas — como se você pegasse um pincel e fechasse as lacunas de uma linha tracejada. |
| **RETR_EXTERNAL** | Modo que diz ao OpenCV: "encontre apenas os contornos de fora, ignore o que está dentro deles". |
| **CHAIN_APPROX_SIMPLE** | Modo de compressão: em vez de guardar todos os pontos de uma linha reta, guarda só os dois extremos. Economiza memória. |
| **State Machine** *(Máquina de Estados)* | Uma lógica de controle com estados bem definidos: `Buscando` → `Estabilizando` → `Travado`. O sistema só avança de estado quando as condições forem atendidas, sem pular etapas. |
| **Lock-On** | O estado final: o gabarito foi confirmado com segurança suficiente. O cronômetro de 5s chegou ao fim sem interrupções. |
| **HUD** *(Heads-Up Display)* | Os textos e informações que aparecem sobrepostos na janela da câmera — como o placar num videogame, mas para diagnóstico em tempo real. |
| **FPS** *(Frames Per Second)* | Quantas fotos por segundo a câmera está processando. Quanto mais alto, mais fluído e responsivo o sistema. |

---

## 1. Variáveis Importantes

- **`DICIONARIO_COMPETICAO`** — Diz ao detector qual "família" de ArUco procurar. O valor `DICT_5X5_1000` significa: malha de 5×5 bits por marcador, com até 1000 IDs diferentes. Se usar o dicionário errado, o marcador simplesmente não é detectado.

- **`DETECTOR_ARUCO`** — O objeto do OpenCV que analisa cada frame e devolve os ArUcos encontrados, com seus cantos e IDs.

- **`margem_percentual` (padrão: `1.35`)** — Como o ArUco fica no centro da forma geométrica, expandimos a Bounding Box em 135% para que a ROI cubra também as bordas do Triângulo, Hexágono ou Estrela ao redor. Sem isso, tentaríamos identificar a forma dentro de uma caixa pequena demais.

---

## 2. Funções do OpenCV Usadas

- **`detectMarkers(frame)`** — Analisa o frame inteiro e retorna três coisas:
  - `corners` — as coordenadas dos 4 cantos de cada ArUco encontrado
  - `ids` — o número (ID) de cada ArUco decodificado com sucesso
  - `rejected` — regiões que pareciam ArUco mas estavam borradas demais para decifrar

- **`cvtColor(BGR→GRAY)`** — Converte a imagem colorida (BGR) para tons de cinza. Bordas são encontradas por contraste de brilho, e cor não importa nessa etapa.

- **`GaussianBlur()`** — Borra levemente a imagem antes do Canny para eliminar ruídos microscópicos que gerariam bordas falsas.

- **`Canny(50, 150)`** — Encontra as bordas. O `50` e `150` são limiares de sensibilidade: bordas fracas só valem se estiverem conectadas a bordas fortes.

- **`morphologyEx(MORPH_CLOSE)`** — Fecha as brechas nas bordas que o Canny deixou abertas por causa de reflexo de luz ou papel mal impresso.

- **`findContours(RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)`** — Transforma as bordas em contornos fechados, pegando só os externos e comprimindo os pontos redundantes.

- **`approxPolyDP(epsilon=1.5%)`** — Suaviza o contorno trêmulo do papel para um polígono limpo. O `epsilon` de 1.5% do perímetro retém detalhes finos das formas (como as pontas da estrela).

---

## 3. Funções do Script

### `extrair_roi_expandida(frame, cantos_aruco, margem_percentual)`()
- **O que faz:** Usando a exata posição X,Y onde achou o ArUco, ela recorta um pedaço retangular da tela da câmera. A área é aumentada iterativamente via multiplicador `margem_percentual`. Impedindo que o drone tente analisar formas geométricas irrelevantes de toda a sala (portas, janelas, chão). Ele vai procurar as formas **estritamente em volta daquele ArUco** 

> Talvez no futuro seja melhor analisar a imagem primeiro e depois o ArUco caso existam ArUcos falsos na competição para enganar. --Alan

### Dependências Modulares da Visão (`visao_utils`)
Este script atua principalmente como um **Orquestrador**, terceirizando as responsabilidades complexas de identificação estática para os módulos abaixo:

- **`classificar_geometria_gabarito`**: Função purista de reconhecimento visual de formas matemáticas importada de `visao_utils/geometria.py`. (Veja [Visão Utils Doc](visaoUtilsDoc.md) para detalhes da arquitetura algorítmica).
- **`EstabilizadorTemporal`**: Cronômetro autônomo baseado no System Clock acionado via injeção importado de `visao_utils/estabilizador.py`. O bloqueio "Trava-lock" no arquivo foi setado para durar de acordo com a meta da constante `TEMPO_CONFIRMACAO_GEOMETRIA` que reside no painel controlador `config.py`.

### `observar_frame_single_step(frame, rastreador)`
A função que "mastiga" um frame por vez e orquestra tudo:

1. Detecta ArUcos no frame completo
2. Marca em vermelho os `rejected` (diagnóstico visual)
3. Para cada ArUco válido: extrai a ROI e classifica a forma
4. Desenha a Bounding Box da ROI em amarelo na janela
5. Seleciona o candidato principal (ArUco de maior área na tela)
6. Atualiza a State Machine
7. Atualiza o HUD com o estado atual (`Buscando`, `Estabilizando X.Xs`, ou `LOCK-ON`)

### `iniciar_teste()`
Liga a câmera, roda o loop `while True` chamando `observar_frame_single_step()` a cada frame, e fecha tudo ao apertar `Q`.

---

## 4. Diagrama: Frame vs ROI

```
┌──────────────────────────────┐
│       FRAME COMPLETO         │  ← foto tirada pela câmera
│                              │
│   ┌──────────────┐           │
│   │     ROI      │ ← recorte focado ao redor do ArUco
│   │  ┌───────┐   │   (expandida 135% via margem_percentual)
│   │  │ ArUco │   │
│   │  └───────┘   │
│   │  △  forma    │
│   └──────────────┘
└──────────────────────────────┘
```
