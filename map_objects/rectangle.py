class Rect:
    # Um retângulo simples para criação de salas no mapa
    def __init__(self, x, y, w, h):
        self.x1 = x # x do canto superior esquerdo
        self.y1 = y # y do canto superior esquerdo
        self.x2 = x + w # x do canto superior direito (+ screenwidth para posicionar na outra extremidade)
        self.y2 = y + h # y do canto superior direito (+ screenheight para posicionar na outra extremidade)
      
    # Retornar o ponto central da sala  
    def center(self):
        center_x = int((self.x1 + self.x2) / 2) # Ponto esquerdo + ponto direito divido por dois equivale a metade horizontal da sala
        center_y = int((self.y1 + self.y2) / 2) # O mesmo acima, equivalente a metade horizontal vertical
        return (center_x, center_y)
    
    # Retornar true se um retângulo sobrepoor outro
    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)