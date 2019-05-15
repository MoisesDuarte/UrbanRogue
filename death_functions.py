import tcod as libtcod

from game_messages import Message

from game_states import GameStates

from render_functions import RenderOrder

# Funções para processamento de morte de entidade
# Jogador morre
def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red
    return Message('Você morreu!', libtcod.red), GameStates.PLAYER_DEAD

# Monstro morre, limpa entidade
def kill_monster(monster):
    death_message = Message('{0} está morto!'.format(monster.name.capitalize()), libtcod.orange)
    
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'Restos mortais de ' + monster.name
    monster.render_order = RenderOrder.CORPSE
    
    return death_message