from map_objects.rectangle import Rect
from map_objects.tile import Tile

class GameMap:
    # Uma classe para inicialização de mapa
    
    def __init__(self, width, height):
        self.width = width # Largura do mapa
        self.height = height # Altura do mapa
        self.tiles = self.initialize_tiles() # Array de tiles do mapa
        
    # Inicialização de um array de mapas
    def initialize_tiles(self):
        # Array com primeira linha tiles em coordenada y (altura) e segunda linha tiles em coordenada x (largura)
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)] # Tiles em True = Bloqueadas por padrão
        
        return tiles
    
    # Gerador de mapa
    def make_map(self):
        # Duas salas para demonstrar
        room1 = Rect(20, 15, 10, 15)
        room2 = Rect(35, 15, 10, 15)
        
        self.create_room(room1)
        self.create_room(room2)
    
    # Gerador de salas retangulares
    def create_room(self, room):
        # Anda pelas tiles do retangulo e define elas como passaveis (não bloqueadas)
        for x in range(room.x1 + 1, room.x2): # Incremento de 1 para gerar uma parede sólida entre salas
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
    
    # Checa se o tile é bloqueado
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        
        return False
 