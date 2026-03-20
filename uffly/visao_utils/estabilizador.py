import time

class EstabilizadorTemporal:
    """
    Máquina de Estados de validação cronometrada unificada.
    Substitui as antigas abordagens baseadas em frames (muito vulneráveis a FPS baixo).
    
    Ela avalia duas informações primárias continuamente (ex: Forma e Dígito). Se a visão tremer ou
    for identificada como "Nenhuma"/None, o relógio é quebrado. Se sobreviver e bater a meta sem quebras,
    aplica o Lock-On.
    """
    def __init__(self, tempo_necessario=5.0):
        # Configuração Cota
        self.tempo_necessario = tempo_necessario
        
        # Estado atual oscilante
        self.valor_primario_atual = None
        self.valor_secundario_atual = None
        
        # Cronômetro Interno
        self.inicio_captura = 0.0
        self.travado = False
        
        # Banco de memória do sucesso
        self.primario_confirmado = None
        self.secundario_confirmado = None

    def atualizar_leitura(self, val_primario, val_secundario=None):
        """
        Injeta os dados validados pelo OpenCV deste exato momento matemático no estabilizador.
        Se os dados persistirem iguas por toda a cota requerida (time.time()), trava como sucesso.
        """
        # Se já confirmamos estabilidade por todo o período, não avalia mais.
        if self.travado:
            return True

        # Proteção: Se a IA reporta não ver formato válido ("Nenhuma", "None"), o cronômetro é quebrado na hora
        if val_primario == "Nenhuma" or val_primario is None:
            self.resetar()
            return False

        # Quebra Lógica: O OpenCV apontou uma transição visual. Ex: Era um Triângulo, virou um Hexágono na folha lida.
        if val_primario != self.valor_primario_atual or val_secundario != self.valor_secundario_atual:
            self.valor_primario_atual = val_primario
            self.valor_secundario_atual = val_secundario
            self.inicio_captura = time.time()
            self.travado = False
            return False

        # Avaliação Contínua e Ininterrupta: Verificando a duração estática na tela
        tempo_decorrido = time.time() - self.inicio_captura
        if tempo_decorrido >= self.tempo_necessario:
            self.travado = True
            self.primario_confirmado = val_primario
            self.secundario_confirmado = val_secundario
            return True
            
        return False
        
    def obter_progresso(self):
        """Retorna uma razão linear (0.0 até 1.0 MAX) de preenchimento do cronômetro da trava atual."""
        if self.valor_primario_atual is None or self.valor_primario_atual == "Nenhuma":
            return 0.0
        if self.travado: 
            return 1.0
        return min((time.time() - self.inicio_captura) / self.tempo_necessario, 1.0)

    def obter_leitura_confirmada(self):
        """Devolve os valores apenas e estritamente atestados para frente. Se não bateu a cota, devolve (None,None)"""
        if self.travado:
            return self.primario_confirmado, self.secundario_confirmado
        return None, None

    def resetar(self):
        """Morte Súbita induzível. Limpa a memória instantaneamente de qualquer lock on parcial ou finalizado."""
        if self.valor_primario_atual is not None:
            self.valor_primario_atual = None
            self.valor_secundario_atual = None
            self.inicio_captura = 0.0
            self.travado = False
            self.primario_confirmado = None
            self.secundario_confirmado = None
