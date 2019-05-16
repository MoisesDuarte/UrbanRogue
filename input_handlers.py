import tcod as libtcod

def handle_keys(key):
    key_char = chr(key.c) # Retorna o caracter da tecla pressionada
    
    # Movimento Cardinal
    if key.vk == libtcod.KEY_UP or key_char == 'k':
        return {'move': (0, -1)} # Retornando valor com x/y axis dicionario 'move' para não confundir com outros possiveis uso da tecla
    elif key.vk == libtcod.KEY_DOWN or key_char == 'j':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'h':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
        return {'move': (1, 0)}
    # Movimento Diagonal
    elif key_char == 'y':
        return {'move': (-1, -1)}
    elif key_char == 'u':
        return {'move': (1, -1)}
    elif key_char == 'b':
        return {'move': (-1, 1)}
    elif key_char == 'n':
        return {'move': (1, s1)}
    
    # Inventário
    if key_char == 'g':
        return {'pickup': True}
   
    
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
