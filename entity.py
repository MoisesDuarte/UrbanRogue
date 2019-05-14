import math

class Entity:
    # Um objeto genérico para representar jogadores, inimigos, itens, etc
    def __init__(self, x, y, char, color, name, blocks=False, fighter=None, ai=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks # Define se a entidade bloqueia movimento
        self.fighter = fighter
        self.ai = ai
        
        if self.fighter:
            self.fighter.owner = self
            
        if self.ai:
            self.ai.owner = self
        
        
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