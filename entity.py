import tcod as libtcod
import math

from render_functions import RenderOrder

class Entity:
    # Um objeto genérico para representar jogadores, inimigos, itens, etc
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None, item=None, inventory=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks # Define se a entidade bloqueia movimento
        self.render_order = render_order # Define a 'camada' de renderização
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        
        # Para acessar a classe por meio da entidade referente (ex: monster.name)
        if self.fighter:
            self.fighter.owner = self
            
        if self.ai:
            self.ai.owner = self
        
        if self.item:
            self.item.owner = self
            
        if self.inventory:
            self.inventory.owner = self
        
    def move(self, dx, dy):
        # Move a entidade em determinado incremento
        self.x += dx
        self.y += dy
    
    # Movimenta o inimigo em direção ao jogador    
    def move_towards(self, target_x, target_y, game_map, entities):
        # Calcula a distancia entre dois pontos utilizando formula de pitagoras
        dx = target_x - self.x # x2 - x1
        dy = target_y - self.y # y2 - y1
        distance = math.sqrt(dx ** 2 + dy ** 2) # Ambas coordenadas elevadas ao quadrado, então é retirada a raiz quadrada, que define a distancia entre os pontos
        
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        
        if not (game_map.is_blocked(self.x + dx, self.y + dy) or get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)
    
    # Algoritmo A* para movimento diagonal
    def move_astar(self, target, entities, game_map):
        # Criar um mapa fov com as dimensões do mapa
        fov = libtcod.map_new(game_map.width, game_map.height)

        # Checa o mapa atual a cada turno e define todas paredes como impassaveis
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].blocked)

        # Checa todas as entidades para ver se não sera preciso circular por ela
        # Checa também se a entidade não é self ou target
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Alocação de um path *A
        # 1.41 é o valor padrão de movimento diagonal
        my_path = libtcod.path_new_using_map(fov, 1.41)

        # Processa o caminho entre as coordenadas proprias da entidade (self) e as do seu alvo (target)
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Checa se o caminho existe e se ele é menor que 25 tiles
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            # Procura as proximas coordenadas do path computado
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # Define as coordenadas proprias para a proxima tile do caminho
                self.x = x
                self.y = y
        else:
            # A velha função como backup, caso for necessario (inimigo bloqueia um corredor, etc)
            self.move_towards(target.x, target.y, game_map, entities)

        # Deleta o caminho para liberar memória
        libtcod.path_delete(my_path)
    
    # Devolve a distancia entre duas coordenadas
    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
        
# Checa se há uma entidade com blocks=True nas coordenadas x e y
def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
        
    return None