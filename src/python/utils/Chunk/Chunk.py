class Vector2i:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def set(self, pos: tuple) -> None:
        self.x = pos[0]
        self.y = pos[1]

    def get(self) -> tuple:
        return (self.x, self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

class Chunk:
    position: Vector2i

    def __init__(self, position: Vector2i):
        self.position = position

    ## Override this on other classes
    def has_data(self) -> bool:
        return False