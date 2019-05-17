# Classe genérica para itens
class Item:
    def __init__(self, use_function, targeting=False, targeting_message=None, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs