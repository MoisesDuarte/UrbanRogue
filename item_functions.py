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

# Função para scroll de magia de relampago
def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')
    
    results = []
    
    target = None
    closest_distance = maximum_range + 1
    
    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y): # Checa se entidade é diferente do jogador e se está na fov
           distance = caster.distance_to(entity) 
           
           if distance < closest_distance: # Checa se a distancia em distance_to é menor que o range do spell
               target = entity
               closest_distance = distance 
               
    if target:
        results.append({'consumed': True, 'target': target, 'message': Message('Um relampago atinge {0} com um estrondo! O dano é {1} hp'.format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
        
    return results