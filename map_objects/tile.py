class Tile:
    # Um tile em um mapa. Pode ou não estar bloqueado (não é possivel mover), pode ou não bloquer a visão
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        
        # Por padrão, se o tile está bloqueado, também bloqueara a linha de visão do jogador
        if block_sight is None: # Se valor for none, mudar para blocked
            block_sight = blocked
            
            self.explored = False # Memória de tiles já exploradas pelo jogador para fov
            
        self.block_sight = block_sight