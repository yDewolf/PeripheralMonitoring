from Listeners.data.BaseKeyStats import BaseKeyStats
import time

class KeyboardKeyStats(BaseKeyStats):
    max_press_streak: int = 0

    _current_streak: int = 0

    # Hold time
    total_hold_time: int = 0
    max_hold_time: int = 0

    def __init__(self, key_name: str) -> None:
        super().__init__(key_name)

        self._last_moment_pressed = time.time()

    @staticmethod
    def get_key_name(key):
        return str(key).lower()
