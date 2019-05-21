from equipment_slots import EquipmentSlots

class Equipment:
    def __init__(self, main_hand=None, off_hand=None):
        self.main_hand = main_hand
        self.off_hand = off_hand
        
    # Funções para processamentos de bonus
    @property
    def max_hp_bonus(self):
        bonus = 0
        
        # Se slot estiver ocupado, adicionar o bonus de hp
        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus
            
        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bon
            
        return bonus
    
    @property
    def defense_bonus(self):
        bonus = 0
        
        # Se slot estiver ocupado, adicionar o bonus de defesa
        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus
            
        if self.off_hand and self.off_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus
            
        return bonus
    
    # Para trocar estado de equipamento no jogador (equipado, desequipado)
    def toggle_equip(self, equippable_entity):
        results = []
        
        slot = equippable_entity.equippable.slot
        
        # Se item já estiver equipado, deduzimos que o jogador quer desequipa-lo
        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})
                    
                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})
                    
                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})
                
        return results