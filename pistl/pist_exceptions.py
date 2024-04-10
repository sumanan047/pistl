# Exception classes for PISTL

class Visualization_Exceptions(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
