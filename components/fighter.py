import tcod as libtcod

from  game_messages import Message

# Classe que define se uma entidade é um objeto 'lutador' (Jogador ou inimigo)
class Fighter:
    def __init__(self, hp, defense, power, xp=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp
        
    # Propriedades de bonus
    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus
    
    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus
        
    # Função para processamento de dano
    def take_damage(self, amount):
        results = [] # Lista para retornar 'resultados' do embate
        
        self.hp -= amount
        
        # Entidade é morta
        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})
            
        return results
    
    # Função para processamento de cura
    def heal(self, amount):
        self.hp += amount
        
        # Check para não ultrapassar o max de hp da entidade
        if self.hp > self.max_hp:
            self.hp = self.max_hp        
        
    # Função para processamento de ataque
    def attack(self, target):
        results = [] # Lista para retornar 'resultados' do embate
        
        damage = self.power - target.fighter.defense
        
        if damage > 0:
            results.append({'message': Message('{0} ataca {1} por {2} hp.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
            results.extend(target.fighter.take_damage(damage)) # Resultado da função takedamage
        else:
            results.append({'message':Message('{0} ataca {1} mas não causa dano.'.format(self.owner.name.capitalize(), target.name), libtcod.white)})

        return results