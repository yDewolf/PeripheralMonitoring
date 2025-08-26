class TimesPressed:
    left_mouse: int = 0
    right_mouse: int = 0
    middle_mouse: int = 0


class Chunk:
    position: tuple

    times_hovered: int = 0

    idle_time: int = 0
    max_idle_time: int = 0

    times_pressed: dict

    def __init__(self, pos: tuple) -> None:
        self.position = pos
        self.times_pressed = {
            "left": 0,
            "right": 0,
            "middle": 0
        }
    
    def stringified(self) -> str:
        times_pressed_str: str = str(self.times_pressed)
        times_pressed_str.replace(",", ";")
        return f"{self.times_hovered},{self.idle_time},{self.max_idle_time},{times_pressed_str}"

    def has_data(self) -> bool:
        return self.times_hovered != 0