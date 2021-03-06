from random import randint

# Devolve um 'peso' apropriado para geração de entidades em nível atual da dungeon
def from_dungeon_level(table, dungeon_level):
    # Checa os valores da tabela de dungeon em reverso, começando pelo maior piso
    for (value, level) in reversed(table):
        # Se o nivel for maior ou igual, retornar o valor do peso
        if dungeon_level >= level:
            return value
        
    return 0

# Função para randomização de chance
def random_choice_index(chances):
    random_chance = randint(1, sum(chances)) # Numero randomico entre 1 e o total de chances
    
    running_sum = 0 
    choice = 0
    for w in chances:
        running_sum += w
        
        # Quando a soma corrente for alcança o valor de chance, retornar o valor para processamento
        if random_chance <= running_sum:
            return choice
        choice += 1 

# Escolha entre um valor randomico definido em um dicionario de valores predefinidas (array)
def random_choice_from_dict(choice_dict):
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())
    
    return choices[random_choice_index(chances)]
    