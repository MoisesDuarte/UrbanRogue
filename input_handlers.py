import tcod as libtcod

from game_states import GameStates

# Checa em qual estado de jogo a tecla está sendo pressionada
def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    
    return {}

# Checagem para cliques do mouse, devolver coordenadas
def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}

# PLAYERS_TURN
def handle_player_turn_keys(key):
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
    elif key_char == 'i':
        return {'show_inventory': True}
    elif key_char == 'd':
        return {'drop_inventory': True}
    
    # Janela
    if key.vk == libtcod.KEY_ENTER and key.lalt: # Tecla fullscreen
        # Alt+Enter : Modo fullscreen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE: # Tecla sair
        # ESC = Sai do jogo
        return {'exit': True}
    
    # Nenhuma tecla pressionada
    return {} # Como a engine irá esperar um dicionário, é preciso sempre retornar algo, mesmo que nada aconteça

# TARGETING
def handle_targeting_keys(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}

# PLAYER_DEAD   
def handle_player_dead_keys(key):
    key_char = chr(key.c)
    
    # Inventário
    if key_char == 'i':
        return {'show_inventory': True}
    
    # Janela
    if key.vk == libtcod.KEY_ENTER and key.lalt: # Tecla fullscreen
        # Alt+Enter : Modo fullscreen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE: # Tecla sair
        # ESC = Sai do jogo
        return {'exit': True}
    
    return {}

# SHOW_INVENTORY
def handle_inventory_keys(key):
    index = key.c - ord('a')
    
    if index >= 0:
        return {'inventory_index': index}
    
    # Janela
    if key.vk == libtcod.KEY_ENTER and key.lalt: # Tecla fullscreen
        # Alt+Enter : Modo fullscreen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE: # Tecla sair
        # ESC = Sai do jogo
        return {'exit': True}
    
    # Nenhuma tecla pressionada
    return {} # Como a engine irá esperar um dicionário, é preciso sempre retornar algo, mesmo que nada aconteça