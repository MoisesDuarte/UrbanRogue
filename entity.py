class Entity:
    # Um objeto genérico para representar jogadores, inimigos, itens, etc
    def __init__(self, x, y, char, color, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks # Define se a entidade bloqueia movimento
        
        
    def move(self, dx, dy):
        # Move a entidade em determinado incremento
        self.x += dx
        self.y += dy
        
# Checa se há uma entidade com blocks=True nas coordenadas x e y
def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
        
    return None