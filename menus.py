import tcod as libtcod

# Funções para menu genérico (Opções, inventário, etc)
# Função para gerar janela de menu
def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Não pode haver um menu com mais de 26 opções.')

    # Calcula altura total para o header (depois do auto-wrap) e uma linha por opção para definir dimensões do menu
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height
    
    # Cria um console offscreen para representar a janela de menu
    window = libtcod.console_new(width, height)
    
    # Desenha o header, com auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)
    
    # Desenha todas as opções
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1
        
    # 'Blita' o conteúdo centralizado para a 'janela' do console root 
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)
    
# Função para gerar menu de inventário
def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    # Mostra um menu com cada item do inventário como uma opção
    if len(player.inventory.items) == 0:
        options = ['Inventário está vazio.']
    else:
        options = []
        
        # Checagem para distinção entre equipamento e item comum
        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{0} (Arma)'.format(item.name))
            elif player.equipment.off_hand == item:
                options.append('{0} (Defesa)'.format(item.name))
            else:
                options.append(item.name)
        
    menu(con, header, options, inventory_width, screen_width, screen_height)
    
# Função para gerar menu inicial
def main_menu(con, background_image, screen_width, screen_height):
    # Imagem de fundo
    libtcod.image_blit_2x(background_image, 0, 0, 0)
    
    # Titulo
    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             'URBAN ROGUE')
    
    # Subtitulo
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER, 
                             'Por MDuarte')
    
    # Opções
    menu(con, '', ['Novo jogo', 'Carregar jogo', 'Sair'], 24, screen_width, screen_height)
    
# Menu de level-up com habilidades
def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['Musculatura (+20 HP, de {0})'.format(player.fighter.max_hp),
               'Força (+1 ataque, de {0})'.format(player.fighter.power),
               'Agilidade (+1 defesa, de {0})'.format(player.fighter.defense)]
    
    menu(con, header, options, menu_width, screen_width, screen_height)
    
# Tela de status do jogador
def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcod.console_new(character_screen_width, character_screen_height)
    
    libtcod.console_set_default_foreground(window, libtcod.white)
    
    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                          libtcod.LEFT, 'Status do Personagem')
    libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                          libtcod.LEFT, 'Nível: {0}'.format(player.level.current_level))
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                          libtcod.LEFT, 'Experiência: {0} / {1}'.format(player.level.current_xp, player.level.experience_to_next_level))
    
    libtcod.console_print_rect_ex(window, 0, 5, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                          libtcod.LEFT, 'HP Máximo: {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                          libtcod.LEFT, 'Ataque: {0}'.format(player.fighter.power))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                          libtcod.LEFT, 'Defesa: {0}'.format(player.fighter.defense))
    
    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)

# Menu vazio para mostrar mensagens
def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)