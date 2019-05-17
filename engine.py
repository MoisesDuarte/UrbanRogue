import tcod as libtcod

from death_functions import kill_monster, kill_player
from entity import get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import Message
from game_states import GameStates
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box
from render_functions import clear_all, render_all  

# INICIALIZAÇÃO DO JOGO
def main():
    constants = get_constants() # Variaveis fixas do jogo
    
    # Especificando arquivo de fonte a ser usada e o tipo de arquivo
    libtcod.console_set_custom_font('terminus10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    
    # Iniciando a tela com dimensões da tela, título e um valor boolean false para iniciar minimizado
    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)
    
    # Definindo instâncias de console
    con = libtcod.console_new(constants['screen_width'], constants['screen_height']) # Painel do jogo
    panel = libtcod.console_new(constants['screen_width'], constants['panel_height']) # Painel da interface
    
    # Declarando variaveis de jogo com valor vazio
    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None
    
    # Variaveis para controle de menu principal
    show_main_menu = True
    show_load_error_message = False
    
    # Fundo do menu
    main_menu_background_image = libtcod.image_load('menu_background.png')

    # Controle de inputs
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        
        if show_main_menu: # Mostra o menu principal
            main_menu(con, main_menu_background_image, 
                      constants['screen_width'], constants['screen_height'])
        
            # Não há arquivo de save
            if show_load_error_message:
                message_box(con, 'Não há nenhum save para carregar', 50,
                            constants['screen_width'], constants['screen_height'])
                
            libtcod.console_flush() # Atualiza o display
            
            # Navegação
            action = handle_main_menu(key)
            
            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')
            
            # Opções
            if show_load_error_message and (new_game or load_saved_game or exit_game): # Volta para o menu caso aparecer mensagem de erro
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state = get_game_variables(constants)     
                game_state = GameStates.PLAYERS_TURN
                show_main_menu = False   
            elif load_saved_game:
                try: # Checa se o save existe
                    player, entities, game_map, message_log, game_state = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break
        else: # Inicia o jogo
            libtcod.console_clear(con)
            play_game(player, entities, game_map, message_log, game_state, con, panel, constants)
            
            show_main_menu = True
        
    

# JOGAR O JOGO EM SI
def play_game(player, entities, game_map, message_log, game_state, con, panel, constants):
    fov_recompute = True # variavel para processamento de fov
    fov_map = initialize_fov(game_map)
    
    # Guardando inputs do jogador
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    
    previous_game_state = game_state # Para guardar o estado anterior ao turno atual
    
    targeting_item = None # Guarda o item que foi selecionado para o targeting atual
    
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse) # Captura eventos de input, atualizando os dados de key e mouse
        
        # Chamada do metodo recompute_fov se fov_recompute = True
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, 
                          constants['fov_radius'], constants['fov_light_walls'], constants['fov_algorithm'])
        
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants['screen_width'], constants['screen_height'], constants['bar_width'],
                   constants['panel_height'], constants['panel_y'], mouse, constants['colors'], game_state)
        
        fov_recompute = False
        
        libtcod.console_flush() # Apresenta os elementos da tela
        
        clear_all(con, entities) # Chamando função clear_all de render_functions para limpar rastro de personagem
        
        # Actions do teclado e mouse
        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)
        
        move = action.get('move') # Capturando retorno de action e guardando o valor de move 
        pickup = action.get('pickup')  
        show_inventory = action.get('show_inventory')
        inventory_index = action.get('inventory_index')
        drop_inventory = action.get('drop_inventory')
        exit = action.get('exit') 
        fullscreen = action.get('fullscreen')   
        
        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')
        
        player_turn_results = [] # lista para resultados de embates e ações em turno
        
        # Controle de turno (Jogador)
        # Processando o retorno de input
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            
            # Verifica se a tile adjancente é bloqueada
            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y) # Checa se destino está bloqueado
                
                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy) # Incremento para movimentação de jogador
                    
                    fov_recompute = True # Recalcula FOV a cada passo do jogador
                    
                game_state = GameStates.ENEMY_TURN # Inicia o turno do inimigo após movimento do jogador
        
        # Processando o pickup de items        
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y: # Checa se o jogador está em cima de um item
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)
                    
                    break # O break significa que o jogador apenas podera pegar um item por vez
                
            else:
                message_log.add_message(Message("Não há nada aqui para pegar.", libtcod.yellow))
        
        # Processando a chamada de menu inventário
        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY
            
        
        # Processando o descarte de item
        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY    
        
        # Processando a chamada de index de itens do menu
        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(player.inventory.items):
            item = player.inventory.items[inventory_index]
            # Checa se é uso ou descarte de item
            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map)) # 'Concatena' o resultado do uso do item ao result apresentado no log a cada turno
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))                                      
        
        # Processando a mira de um spell
        if game_state == GameStates.TARGETING:
            if left_click: # Confirma o alvo
                target_x, target_y = left_click

                item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map, target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click: # Cancela o alvo
                player_turn_results.append({'targeting_cancelled': True})
        
        if exit:
            # Verifica se inventário está aberto, para não fechar o jogo ao apertar esc no menu
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            # Verifica se o jogador está mirando, esc cancela o alvo
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                save_game(player, entities, game_map, message_log, game_state) # Salvar jogo ao sair
                
                return True
        
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())   
        
        # Controle do log do turno do jogador
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            
            if message:
                message_log.add_message(message)
                
            # Cancelamento de alvo
            if targeting_cancelled:
                game_state = previous_game_state
                message_log.add_message(Message('Alvo Cancelado'))
            
            # Morte de entidades
            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else: 
                    message = kill_monster(dead_entity)
                
                message_log.add_message(message)
                
            # Pickup de item
            if item_added:
                entities.remove(item_added)
                
                game_state = GameStates.ENEMY_TURN
                
            # Uso de item
            if item_consumed:
                game_state = GameStates.ENEMY_TURN
                
            # Mirando item
            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING
                
                targeting_item = targeting
                
                message_log.add_message(targeting_item.item.targeting_message)
                
            # Descarte de item
            if item_dropped:
                entities.append(item_dropped)
                
                game_state = GameStates.ENEMY_TURN
                
                        
        # Controle de turno (Inimigo)
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)
                    
                    # Controle de log do turno inimigo
                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')
                        
                        if message:
                            message_log.add_message(message)
                           
                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else: 
                                message = kill_monster(dead_entity)
                                
                            message_log.add_message(message)
                            
                            if game_state == GameStates.PLAYER_DEAD:
                                break
                            
                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:    
                game_state = GameStates.PLAYERS_TURN # Volta para o turno do jogador
       
    
    
# A função main apenas será executada quando o script for executado com o comando 'python engine.py'
if __name__ == '__main__':
    main()