import tcod as libtcod

from game_messages import Message

# Componente para controle de inventório
class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        
    # Função para adicionar item ao inventario
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
    
    # Função para usar item do inventario
    def use(self, item_entity, **kwargs):
        results = []
        
        item_component = item_entity.item
        
        # Checa se item é não é 'usavel' em inventário (ex: equipamento, itens de quest)
        if item_component.use_function is None:
            equippable_component = item_entity.equippable
            
            # Então, se esse item for equipavel, marca como equipado. Caso não, apenas mensagem
            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append({'message': Message('{0} não pode ser usado'.format(item_entity.name), libtcod.yellow)})
        else:
            # Checa se item necessita de um target, para não usa-lo antes e se já não ha um x e y recebido, para definir que alvo ainda não foi selecionado
            if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')): 
                results.append({'targeting': item_entity})
            else:
                kwargs = {**item_component.function_kwargs, **kwargs} # Concatena função com modificador para usar em function (ex: 'heal' == 4)
                item_use_results = item_component.use_function(self.owner, **kwargs) 
                
                # Checa se item está marcado como consumido e o remove do inventário
                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.remove_item(item_entity)
                        
                results.extend(item_use_results)
            
        return results
    
    # Função para remover item do inventario
    def remove_item(self, item):
        self.items.remove(item)
        
    # Função para descartar item do inventario e colocar ela aos pés do jogador (nas coordenadas)
    def drop_item(self, item):
        results = []
        
        # Se item jogado for equipavel, 'desequipa' antes de jogar
        if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item:
            self.owner.equipment.toggle_equip(item)
        
        # Define coordenadas do item como mesmas coordenadas do jogador
        item.x = self.owner.x
        item.y = self.owner.y
        
        self.remove_item(item) # Remove item do inventario
        results.append({'item_dropped': item, 'message': Message('Você descartou {0}'.format(item.name), libtcod.yellow)})
        
        return results       