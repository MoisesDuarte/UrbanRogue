import tcod as libtcod

from game_states import GameStates

# Funções para processamento de morte de entidade

# Jogador morre
def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red
    
    return 'Você morreu!', GameStates.PLAYER_DEAD

# Monstro morre, limpa entidade
def kill_monster(monster):
    death_message = '{0} está morto!'.format(monster.name.capitalize())
    
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'Restos mortais de ' + monster.name
    
    return death_message