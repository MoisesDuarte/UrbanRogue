import tcod as libtcod

from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all

def main():
    # Dimensões da tela
    screen_width = 80
    screen_height = 50
    
    # Dimensões do mapa
    map_width = 80
    map_height = 45
    
    # Dimensões das salas
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    
    # Atributos para FOV (Field of View)
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10
    
    # Atributos para geração de inimigos
    max_monsters_per_room = 3
    
    # Cores dos tiles
    colors = {
        'dark_wall': libtcod.Color(49, 46, 47),
        'dark_ground': libtcod.Color(81, 94, 46),
        'light_wall': libtcod.Color(99, 92, 90),
        'light_ground': libtcod.Color(157, 159, 55)
    }
    
    # Posição dos elementos de jogo (função int usada para cast de resultado de divisão para um integer)
    player = Entity(0, 0, '@', libtcod.white)
    entities = [player]
    
    # Especificando arquivo de fonte a ser usada e o tipo de arquivo
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
    
    # Iniciando a tela com dimensões da tela, título e um valor boolean false para iniciar minimizado
    libtcod.console_init_root(screen_width, screen_height, 'Urban Rogue', False)
    
    # Definindo uma instância de console
    con = libtcod.console_new(screen_width, screen_height) 
    
    # Inicialização do mapa
    game_map = GameMap(map_width, map_height) # Definindo o tamanho do mapa
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room) # Gerando o mapa em si
    
    # Inicialização do FOV
    fov_recompute = True # variavel para processamento de fov
    fov_map = initialize_fov(game_map)
    
    # Inputs do jogador
    key = libtcod.Key() # Guarda input do teclado em key
    mouse = libtcod.Mouse() # Guarda input do mouse em mouse
    
    # Loop do jogo
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse) # Captura eventos de input, atualizando os dados de key e mouse
        
        # Chamada do metodo recompute_fov se fov_recompute = True
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
        
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors) # Chamando função render_all de render_functions para desenhar o mapa e todas entidades da lista entities na tela
        
        fov_recompute = False
        
        libtcod.console_flush() # Apresenta os elementos da tela
        
        clear_all(con, entities) # Chamando função clear_all de render_functions para limpar rastro de personagem
        
        # Input do teclado
        action = handle_keys(key)
        
        # Capturando retorno em action e seu conteúdo
        move = action.get('move') 
        exit = action.get('exit') 
        fullscreen = action.get('fullscreen')   
        
        # Processando o retorno de input
        if move:
            dx, dy = move
            # Verifica se a tile adjancente é bloqueada
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy) # Incremento para movimentação de jogador
                
                fov_recompute = True # Recalcula FOV a cada passo do jogador
        
        if exit:
            return True
        
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())   
        
    
# A função main apenas será executada quando o script for executado com o comando 'python engine.py'
if __name__ == '__main__':
    main()