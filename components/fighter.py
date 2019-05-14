# Classe que define se uma entidade é um objeto 'lutador' (Jogador ou inimigo)
class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power