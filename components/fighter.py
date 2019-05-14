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
            results.append({'message':'{0} ataca {1}, subtraindo {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage))})
            results.extend(target.fighter.take_damage(damage)) # Resultado da função takedamage
        else:
            results.append({'message':'{0} ataca {1}, mas não causa nenhum dano.'.format(self.owner.name.capitalize(), target.name)})

        return results