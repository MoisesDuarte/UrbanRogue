import tcod as libtcod

import textwrap

# Mensagem dentro do log
class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color

# Log das mensagens
class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height
        
    # Escreva uma mensagem no log
    def add_message(self, message):
        # Quebra a mensagens em várias linhas se for necessário
        new_msg_lines = textwrap.wrap(message.text, self.width)
        
        for line in new_msg_lines:
            # Se o buffer estiver cheio, remover primeira linha para dar espaço para a nova
            if len(self.messages) == self.height: # Se array messages for igual a altura do painel
                del self.messages[0] # Deletar a primeira mensagem do array
                
            # Adiciona a nova linha como um objeto Mensagem, com texto e cor
            self.messages.append(Message(line, message.color))