import tcod as libtcod

from  game_messages import Message

# Classe que define se uma entidade é um objeto 'lutador' (Jogador ou inimigo)
class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        
    def take_damage(self, amount):
        results = [] # Lista para retornar 'resultados' do embate
        
        self.hp -= amount
        
        # Entidade é morta
        if self.hp <= 0:
            results.append({'dead': self.owner})
            
        return results
        
    # Função para ataque
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