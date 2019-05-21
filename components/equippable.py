# Componente para controle de atributos de itens equipaveis
class Equippable:
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        self.slot = slot # Define o slot do equipamento (main hand ou offhand)
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
        
        