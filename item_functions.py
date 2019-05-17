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

# Função para scroll de bola de fogo
def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    
    results = []
    
    # Checa se o tile está fora da fov
    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('Voce nao pode mirar em um tile fora de sua visão.', libtcod.yellow)})
        return results
    
    # Mensagem para notificar de radius do spell
    results.append({'consumed': True, 'message': Message('A bola de fogo explode, queimando tudo dentro de {0} tiles!'.format(radius), libtcod.orange)})
    
    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter: # Se a distancia das coordenadas da entidade forem menores que o radius do spell e se a entidade for uma 'fighter' (inimigo)
            results.append({'message': Message('{0} queima {1} hit points'.format(entity.name, damage), libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage))
            
    return results