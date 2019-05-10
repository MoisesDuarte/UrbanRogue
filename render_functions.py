import tcod as libtcod

# Desenha todas as entidades da lista entities com função draw_entity
def render_all(con, entities, screen_width, screen_height):
    for entity in entities:
        draw_entity(con, entity) 
          
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0) # 'Leva' as mudanças para tela
    
# Limpar as entidades depois de coloca-las na tela (para que elas se movam sem deixar um rastro)
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)
  
# Desenha a entidade      
def draw_entity(con, entity):
    libtcod.console_set_default_foreground(con, entity.color) # Definindo a cor da entidade
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE) # Desenhando no console as coordenadas x e y, com background vazio
    
# Apaga o caracter que representa esse objeto (no caso, seu rastro)
def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
