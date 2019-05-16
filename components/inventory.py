import tcod as libtcod

from game_messages import Message

# Componente para controle de inventório
class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        
    def add_item(self, item):
        results = []
        
        # Checa se inventário está cheio
        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('Não pode carregar mais nada, inventário cheio.', libtcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('Você pegou {0}!'.format(item.name), libtcod.blue)
            })
            
            self.items.append(item)
            
        return results