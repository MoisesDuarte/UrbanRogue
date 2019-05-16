# Classe genérica para itens
class Item:
    def __init__(self, use_function, **kwargs):
        self.use_function = use_function
        self.function_kwargs = kwargs