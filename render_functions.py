import tcod as libtcod

from enum import Enum

# Define 'camadas' de renderização
class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3
    
# Renderiza a interface
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
def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, screen_width, screen_height, bar_width, panel_height, panel_y, colors):
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
        draw_entity(con, entity, fov_map) 
          
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0) # 'Desenha' o console definido em con
    
    # Reseta um console para suas cores padrões com um caractere ' ' (espaço)
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)
    
    # Renderiza uma barra de hp
    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)
    
    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y) # Desenha o console definido como panel na tela
    
# Limpar as entidades depois de coloca-las na tela (para que elas se movam sem deixar um rastro)
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)
  
# Desenha a entidade      
def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color) # Definindo a cor da entidade
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE) # Desenhando no console as coordenadas x e y, com background vazio
    
# Apaga o caracter que representa esse objeto (no caso, seu rastro)
def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
