class Rect:
    # Um retângulo simples para criação de salas no mapa
    def __init__(self, x, y, w, h):
        self.x1 = x # x do canto superior esquerdo
        self.y1 = y # y do canto superior esquerdo
        self.x2 = x + w # x do canto superior direito (+ screenwidth para posicionar na outra extremidade)
        self.y2 = y + h # y do canto superior direito (+ screenheight para posicionar na outra extremidade)