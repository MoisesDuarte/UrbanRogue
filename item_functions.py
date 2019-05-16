import tcod as libtcod

from game_messages import Message

# Funções para diferentes tipos de itens
# Função para item de cura
def heal(*args, **kwargs):
    # *args = convenção de nome utilizado para variavel que recebera um numero variavel de argumentos 'brutos'
    # **kwargs = convenção de nome utilizada para variavel que recebera um numero variavel de argumentos nomeados
    entity = args[0] # Entidade que está usando item
    amount = kwargs.get('amount') # Modificador da função do item
    
    results = []
    
    # Checando a vida 'atual' do personagem
    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('Você já esta com a vida cheia', libtcod.yellow)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('A dor de suas feridas começam a ceder!', libtcod.green)})
        
    return results