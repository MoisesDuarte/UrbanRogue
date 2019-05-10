import tcod as libtcod

def main():
    # Dimensões da tela
    screen_width = 80
    screen_height = 50
    
    # Posição do personagem
    # Desenha o personagem no meio da tela (função int usada para cast de resultado de divisão para um integer)
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)
    
    # Especificando arquivo de fonte a ser usada e o tipo de arquivo
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
    
    # Iniciando a tela com dimensões da tela, título e um valor boolean false para iniciar minimizado
    libtcod.console_init_root(screen_width, screen_height, 'Urban Rogue', False)
    
    # Inputs do jogador
    key = libtcod.Key() # Guarda input do teclado em key
    mouse = libtcod.Mouse() # Guarda input do mouse em mouse
    
    # Loop do jogo
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse) # Captura eventos de input, atualizando os dados de key e mouse
        
        libtcod.console_set_default_foreground(0, libtcod.white) # Definindo a cor do simbolo '@' como branco
        libtcod.console_put_char(0, player_x, player_y, '@', libtcod.BKGND_NONE) # Desenhando no console 0, que estamos usando, '@' nas coordenadas x e y, com background vazio
        libtcod.console_flush() # Apresenta os elementos da tela
        
        # Fechar jogo
        key = libtcod.console_check_for_keypress() # Guarda o input do teclado em key
        if key.vk == libtcod.KEY_ESCAPE: # Se key for igual a esc, retorna True, saindo do loop e fechando o jogo
            return True
    
# A função main apenas será executada quando o script for executado com o comando 'python engine.py'
if __name__ == '__main__':
    main()