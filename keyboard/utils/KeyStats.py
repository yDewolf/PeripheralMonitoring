import time

class KeyStats:
    related_key_name: str

    times_pressed: int = 0
    max_press_streak: int = 0

    current_streak: int = 0

    is_pressed: bool = False

    # Epoch time
    last_moment_pressed: float

    # Intervals
    longest_interval: int = -1
    smallest_interval: int = -1

    # Hold time
    total_hold_time: int = 0
    max_hold_time: int = 0

    def __init__(self, key_name: str) -> None:
        self.related_key_name = key_name

        self.last_moment_pressed = time.time()

    def update_on_pressed(self, consecutive: bool):
        if self.is_pressed:
            return

        self.is_pressed = True

        self.times_pressed += 1

        if consecutive:
            self.max_press_streak = max(self.current_streak, self.max_press_streak)
            self.current_streak += 1
        
        if not consecutive:
            self.on_a_streak = False
            self.current_streak = 1

        # Setup the last moment pressed variable
        if self.times_pressed == 1:
            self.last_moment_pressed = time.time()
            return

        interval = int(round((time.time() - self.last_moment_pressed) * 1000))
        self.last_moment_pressed = time.time()
        
        if self.smallest_interval == -1 and self.times_pressed >= 2:
            self.smallest_interval = interval
        
        self.smallest_interval = min(interval, self.smallest_interval)
        self.longest_interval = max(interval, self.longest_interval)

    def update_on_released(self):
        self.is_pressed = False

        hold_time = int(round((time.time() - self.last_moment_pressed) * 1000))
        
        self.total_hold_time += hold_time
        self.max_hold_time = max(self.max_hold_time, hold_time)
    
    def to_string(self) -> str:
        stringified = ""
        stringified += f"{self.related_key_name},"
        stringified += f"{self.times_pressed},"
        stringified += f"{self.max_press_streak},"

        stringified += f"{self.longest_interval},"
        stringified += f"{self.smallest_interval},"

        stringified += f"{self.total_hold_time},"
        stringified += f"{self.max_hold_time}"

        return stringified