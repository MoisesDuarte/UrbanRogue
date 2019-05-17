from enum import Enum

# Controle de turnos e estados de jogo
class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURN = 2  
    PLAYER_DEAD = 3
    SHOW_INVENTORY = 4
    DROP_INVENTORY = 5
    TARGETING = 6