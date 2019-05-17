import tcod as libtcod

from components.fighter import Fighter
from components.inventory import Inventory

from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import Message, MessageLog
from game_states import GameStates
from input_handlers import handle_keys, handle_mouse
from loader_functions.initialize_new_game import get_gamevariables
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all, RenderOrder

def main():
    gamevariables = get_gamevariables() # Carrega todas as variaveis fixas do jogo
    
    # Atributos do jogador
    fighter_component = Fighter(hp=30, defense=2, power=5) 
    inventory_component = Inventory(26)
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component)
    entities = [player]
    
    # Especificando arquivo de fonte a ser usada e o tipo de arquivo
    libtcod.console_set_custom_font('terminus10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    
    # Iniciando a tela com dimensões da tela, título e um valor boolean false para iniciar minimizado
    libtcod.console_init_root(gamevariables['screen_width'], gamevariables['screen_height'], gamevariables['window_title'], False)
    
    # Definindo instâncias de console
    con = libtcod.console_new(gamevariables['screen_width'], gamevariables['screen_height']) # Painel do jogo
    panel = libtcod.console_new(gamevariables['screen_width'], gamevariables['panel_height']) # Painel da interface
    
    # Inicialização do mapa
    game_map = GameMap(gamevariables['map_width'], gamevariables['map_height'])
    game_map.make_map(gamevariables['max_rooms'], gamevariables['room_min_size'], gamevariables['room_max_size'],
                      gamevariables['map_width'], gamevariables['map_height'], player, entities,
                      gamevariables['max_monsters_per_room'], gamevariables['max_items_per_room'])
    
    # Inicialização do FOV
    fov_recompute = True # variavel para processamento de fov
    fov_map = initialize_fov(game_map)
    
    # Inicialização do log
    message_log = MessageLog(gamevariables['message_x'], gamevariables['message_width'], gamevariables['message_height'])
    
    # Guardando inputs do jogador
    key = libtcod.Key() # Guarda input do teclado em key
    mouse = libtcod.Mouse() # Guarda input do mouse em mouse
    
    # Estados de jogo
    game_state = GameStates.PLAYERS_TURN # Inicia estado de jogo como turno do jogador
    previous_game_state = game_state # Guarda o estado anterior ao turno atual
    
    targeting_item = None # Guarda o item que foi selecionado para o targeting atual
    
    # Loop do jogo
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse) # Captura eventos de input, atualizando os dados de key e mouse
        
        # Chamada do metodo recompute_fov se fov_recompute = True
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, 
                          gamevariables['fov_radius'], gamevariables['fov_light_walls'], gamevariables['fov_algorithm'])
        
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                   gamevariables['screen_width'], gamevariables['screen_height'], gamevariables['bar_width'],
                   gamevariables['panel_height'], gamevariables['panel_y'], mouse, gamevariables['colors'], game_state)
        
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