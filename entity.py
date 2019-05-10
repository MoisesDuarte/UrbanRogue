class Entity:
    # Um objeto genérico para representar jogadores, inimigos, itens, etc
    def __init__(self, x, y, char, color):
        self.x = x # Coordenada X
        self.y = y # Coordenada Y
        self.char = char # Caracter que representa a entidade
        self.color = color # Cor do caracter
        
    def move(self, dx, dy):
        # Move a entidade em determinado incremento
        self.x += dx
        self.y += dy