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
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]
        
        tiles[30][22].blocked = True
        tiles[30][22].block_sight = True
        tiles[31][22].blocked = True
        tiles[31][22].block_sight = True
        tiles[32][22].blocked = True
        tiles[32][22].block_sight = True
        
        return tiles
    
    # Checa se o tile é bloqueado
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        
        return False
 