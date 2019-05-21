import tcod as libtcod

from enum import Enum

from game_states import GameStates

from menus import character_screen, inventory_menu, level_up_menu

# Define 'camadas' de renderização
class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4

# Escreve nome de entidades acima da barra de hp com mouseover 
def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()

# Renderiza barras (barra de vida, mana, etc)
def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width) 

    # Painel da interface
    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
    
    # Barra de hp, mana, etc
    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
    
    # Contador de hp, mana, etc
    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))

# Renderiza todo os elementos de tela
def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state):
    # Desenha todas as tiles do mapa
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight # Array com tiles guardados em gamemap
                
                # Renderização de paredes e chão com base em fov visivel (visible = True)
                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)
                        
                    game_map.tiles[x][y].explored = True # Marca tile como já explorada, a mantendo 'acesa' no mapa
                 
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET) # Definindo o background como tile parede
                    else:  
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET) # Definindo o background como tile chão
    
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value) # Retorna a lista de render
            
    # Desenha todas as entidades da lista entities com draw_entity   
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map) 
          
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0) # 'Desenha' o console definido em con
    
    # Checa o estado de jogo e desenha o inventário do jogador
    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        # Checa se é inventario de uso ou de descarte
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Aperta a tecla ao lado de um item para usar, ou Esc para cancelar.\n'
        else:
            inventory_title = 'Aperte a tecla ao lado de um item para descartar, ou Esc para cancelar.\n'
            
        inventory_menu(con, inventory_title, player, 50, screen_width, screen_height) # Chama o menu inventario
    
    # Checa se jogador sobe de nivel e chama tela de levelup
    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, 'Level up! Escolha um atributo para aumentar:', player, 40, screen_width, screen_height)
    # Checa chamada de tela de status
    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)
    
    # Reseta um console para suas cores padrões com um caractere ' ' (espaço)
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)
    
    # Escreve as mensagens do jogo, uma linha por vez
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1
    
    # Renderiza uma barra de hp e profundidae 
    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)
    libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Piso da masmorra: {0}'.format(game_map.dungeon_level))
    
    # Renderiza uma mensagem um nome acima da barra de hp no mouseover em uma entidade
    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse(mouse, entities, fov_map))
    
    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y) # Desenha o console definido como panel na tela
    
# Limpar as entidades depois de coloca-las na tela (para que elas se movam sem deixar um rastro)
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)
  
# Desenha a entidade      
def draw_entity(con, entity, fov_map, game_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.stairs and game_map.tiles[entity.x][entity.y].explored): # Checa se esta no fov ou se é uma escada
        libtcod.console_set_default_foreground(con, entity.color) # Definindo a cor da entidade
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE) # Desenhando no console as coordenadas x e y, com background vazio
    
# Apaga o caracter que representa esse objeto (no caso, seu rastro)
def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
