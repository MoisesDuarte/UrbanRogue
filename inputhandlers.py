import tcod as libtcod

def handle_keys(key):
    # Teclas de movimento
    if key.vk == libtcod.KEY_UP: # Seta para cima
        return {'move': (0, -1)} # Retornando valor com x/y axis dicionario 'move' para não confundir com outros possiveis uso da tecla
    elif key.vk == libtcod.KEY_DOWN: # Seta para baixo
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT: # Seta para esquerda
        return {'move': (1, 0)}
    elif key.vk == libtcod.KEY_RIGHT: # Seta para direita
        return {'move': (1, 0)}
    
    # Tecla fullscreen
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter : Modo fullscreen
        return {'fullscreen': True}
    
    # Tecla sair
    elif key.vk == libtcod.KEY_ESCAPE:
        # ESC = Sai do jogo
        return {'exit': True}
    
    # Nenhuma tecla pressionada
    return {} # Como a engine irá esperar um dicionário, é preciso sempre retornar algo, mesmo que nada aconteça