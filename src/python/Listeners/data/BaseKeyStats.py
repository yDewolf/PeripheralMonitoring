import time

class BaseKeyStats:
    related_key_name: str
    _is_pressed: bool = False

    times_pressed: int = 0
    _last_moment_pressed: float = 0

    # Intervals
    longest_interval: int = -1
    smallest_interval: int = -1

    def __init__(self, key_name: str) -> None:
        self.related_key_name = key_name

    def to_string(self) -> str:
        stringified = ""
        stringified += f"{self.related_key_name},"
        stringified += f"{self.times_pressed},"

        stringified += f"{self.longest_interval},"
        stringified += f"{self.smallest_interval}"

        return stringified

    def update_interval_variables(self):
        interval = -1
        if self.times_pressed >= 2:
            interval = int(round((time.time() - self._last_moment_pressed) * 1000))
        
        self._last_moment_pressed = time.time()
        
        if self.smallest_interval == -1 and self.times_pressed >= 2:
            self.smallest_interval = interval
        
        self.smallest_interval = min(interval, self.smallest_interval)
        self.longest_interval = max(interval, self.longest_interval)

    @staticmethod
    def get_header() -> str:
        return "KeyName,TimesPressed,LongestInterval,SmallestInterval"