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

    def to_string(self) -> str:
        stringified = super().to_string() + ","
        stringified += f"{self.max_press_streak},"

        stringified += f"{self.total_hold_time},"
        stringified += f"{self.max_hold_time}"

        return stringified

    @staticmethod
    def get_key_name(key):
        return str(key).lower()

    @staticmethod
    def get_header() -> str:
        return BaseKeyStats.get_header() + "MaxStreak,TotalHoldTime,MaxHoldTime"