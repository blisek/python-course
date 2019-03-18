

class InputNotProvidedError(ValueError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
