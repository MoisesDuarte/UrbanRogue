import tcod as libtcod
from random import randint

from render_functions import RenderOrder

from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs

from entity import Entity

from game_messages import Message

from item_functions import cast_confuse, cast_fireball, cast_lightning, heal

from map_objects.rectangle import Rect
from map_objects.tile import Tile

from random_utils import from_dungeon_level, random_choice_from_dict

class GameMap:
    # Uma classe para inicialização de mapa
    
    def __init__(self, width, height, dungeon_level=1):
        self.width = width # Largura do mapa
        self.height = height # Altura do mapa
        self.tiles = self.initialize_tiles() # Array de tiles do map
        
        self.dungeon_level = dungeon_level # 'Profundidade' do jogador na dungeon
        
    # Inicialização de um array de mapas
    def initialize_tiles(self):
        # Array com primeira linha tiles em coordenada y (altura) e segunda linha tiles em coordenada x (largura)
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)] # Tiles em True = Bloqueadas por padrão
        
        return tiles
    
    # Gerador de mapa (cavocando salas em um mapa totalmente sólido)
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        rooms = [] # Lista das salas geradas
        num_rooms = 0 # Guarda número de salas no mapa
        
        # Ponto central da última sala para colocar escada
        center_of_last_room_x = None
        center_of_last_room_y = None
        
        # Randomizando o tamanho das salas
        for r in range(max_rooms):
            # Altura e largura aleatoria
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # Posição aleatoria sem sair dos limites do mapa
            x = randint(0, map_width - w - 1)      
            y = randint(0, map_height - h - 1)
            
            new_room = Rect(x, y, w, h) # Objeto que irá representar a nova sala
            
            # Checagem de interseção
            for other_room in rooms: # Se o loop for não der 'break', então a sala será criada
                if new_room.intersect(other_room):
                    break
            else:
                # Não há interseções, então a sala é valida
                
                # 'Pintar' a sala nos tiles do mapa (nesse caso, cavocar)
                self.create_room(new_room)
                
                # Centraliza as coordenadas x e y da sala
                (new_x, new_y) = new_room.center()
                
                center_of_last_room_x = new_x
                center_of_last_room_y = new_y
                
                # Checagem de sala inicial
                if num_rooms == 0:
                    # Centraliza o jogador na sala inicial
                    player.x = new_x
                    player.y = new_y
                else:
                    # Todas as salas além da inicial
                    # Conectar a sala anterior com um tunel
                    
                    # Centralizar as coordenadas da sala anterior
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    
                    # Cara ou coroa (1 ou 0)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                        
                self.place_entities(new_room, entities) # Chama a função para gerar inimigos
                        
                rooms.append(new_room)
                num_rooms += 1
                
        # Processamento da entidade escada
        stairs_component = Stairs(self.dungeon_level + 1) # Sobe o jogador um nivel
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs', render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)     
                
    
    # Gerador de salas
    def create_room(self, room):
        # Anda pelas tiles do retangulo e define elas como passaveis (não bloqueadas)
        for x in range(room.x1 + 1, room.x2): # Incremento de 1 para gerar uma parede sólida entre salas
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
                
    # Gerador de tuneis
    # Gera tuneis horizontais
    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
    
    # Gera tuneis verticais
    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
            
    # Gera e coloca entidades de jogo
    def place_entities(self, room, entities):   
        # Definindo maximo de monstros e itens com base em nivel da dungeon
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)
    
        number_of_monsters = randint(0, max_monsters_per_room)  # Gera um número aleatório de inimigos para sala
        number_of_items = randint(0, max_items_per_room) # Gera um número aleatorio de itens para sala
        
        # Guardando as diferentes 'chances' de monstros e itens para algoritmo de randomização
        monster_chances = {
                'orc': 80, 
                'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)
            }
            
        item_chances = {
                'frasco_cura': 35, 
                'scroll_relampago': from_dungeon_level([[25, 4]], self.dungeon_level), 
                'scroll_boladefogo': from_dungeon_level([[25, 6]], self.dungeon_level), 
                'scroll_confusao': from_dungeon_level([[10, 2]], self.dungeon_level)
            }
        
        # Colocando os inimigos em espaços aleatorios do mapa
        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            
            if not any([entity for entity in entities if entity.x == x and entity.y == y]): # Checa se já não há um inimigo nas mesmas coordenadas
                monster_choice = random_choice_from_dict(monster_chances) # Chamando a função de randomizacao para escolhar um monstro randomico em array
                
                if monster_choice == 'orc':
                    fighter_component = Fighter(hp=20, defense=0, power=4, xp=35)
                    ai_component = BasicMonster()               
                    monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                else:
                    fighter_component = Fighter(hp=30, defense=2, power=8, xp=100)
                    ai_component = BasicMonster()           
                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                    
                entities.append(monster) # Adiciona o monstro gerado a lista de entidade para renderizar em RenderFunctions.render_all
                
        # Colocando itens em espaços aleatorios do mapa
        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances) # O mesmo que a chamada da função para monstros acima
                
                if item_choice == 'frasco_cura':     
                    item_component = Item(use_function=heal, amount=40) # Define o item como um item de cura +4 hp
                    item = Entity(x, y, '!', libtcod.violet, 'Frasco de Cura', render_order=RenderOrder.ITEM, item=item_component)
                elif item_choice == 'scroll_boladefogo':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message('Click em um tile para bola de fogo, ou click-direito para cancelar.', libtcod.light_cyan), damage=25, radius=3)
                    item = Entity(x, y, '#', libtcod.red, 'Scroll de Bola de Fogo', render_order=RenderOrder.ITEM, item=item_component)
                elif item_choice == 'scroll_confusao':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message("Click em um inimigo para confundir, ou click-direito para cancelar.", libtcod.light_cyan))
                    item = Entity(x, y, '#', libtcod.light_pink, 'Scroll de Confusão', render_order=RenderOrder.ITEM, item=item_component)
                else:
                    item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5) # Define o item como uma scroll de relampago, dano 20, range 5
                    item = Entity(x, y, '#', libtcod.yellow, 'Scroll de Relampago', render_order=RenderOrder.ITEM, item=item_component)
                    
                entities.append(item)
        
            
    # Checa se o tile é bloqueado
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
 
 
    # Gera o proximo mapa
    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player] # Cria uma nova lista de entidades
        
        # Gera as tiles do novo piso
        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                    constants['map_width'], constants['map_height'], player, entities)
        
        # Metade do hp de volta
        player.fighter.heal(player.fighter.max_hp // 2)
        
        message_log.add_message(Message('Você descansa um pouco, recuperando suas forças.', libtcod.light_violet))
        
        return entities