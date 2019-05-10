import tcod as libtcod
from entity import Entity
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
    
    # Cores dos tiles
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150)
    }
    
    # Posição dos elementos de jogo (função int usada para cast de resultado de divisão para um integer)
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white) # Desenha o personagem
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow) # Desenha o npc
    entities = [npc, player] # Lista com todas as entidades do mapa
    
    # Especificando arquivo de fonte a ser usada e o tipo de arquivo
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
    
    # Iniciando a tela com dimensões da tela, título e um valor boolean false para iniciar minimizado
    libtcod.console_init_root(screen_width, screen_height, 'Urban Rogue', False)
    
    # Definindo uma instância de console
    con = libtcod.console_new(screen_width, screen_height) 
    
    # Inicialização do mapa
    game_map = GameMap(map_width, map_height) # Definindo o tamanho do mapa
    game_map.make_map() # Gerando o mapa em si
    
    # Inputs do jogador
    key = libtcod.Key() # Guarda input do teclado em key
    mouse = libtcod.Mouse() # Guarda input do mouse em mouse
    
    # Loop do jogo
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse) # Captura eventos de input, atualizando os dados de key e mouse
        render_all(con, entities, game_map, screen_width, screen_height, colors) # Chamando função render_all de render_functions para desenhar o mapa e todas entidades da lista entities na tela
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
        
        if exit:
            return True
        
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())   
        
    
# A função main apenas será executada quando o script for executado com o comando 'python engine.py'
if __name__ == '__main__':
    main()