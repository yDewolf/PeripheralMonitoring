import time
from Listeners.data.KeyboardKeyStats import KeyboardKeyStats


class KeyboardEventParser:
    consecutive: bool = False
    previous_key_name: str = ""

    def parse_key_press(self, key_stats: KeyboardKeyStats):
        is_consecutive: bool = self.previous_key_name == key_stats.related_key_name
        self._parse_key_press(key_stats, is_consecutive)

    @staticmethod
    def _parse_key_press(key_stats: KeyboardKeyStats, consecutive: bool):
        KeyboardEventParser.update_on_pressed(key_stats, consecutive)

    @staticmethod
    def update_on_pressed(key_stats: KeyboardKeyStats, consecutive: bool):
        if key_stats.is_pressed:
            return

        key_stats.is_pressed = True

        key_stats.times_pressed += 1

        if consecutive:
            key_stats.max_press_streak = max(key_stats.current_streak, key_stats.max_press_streak)
            key_stats.current_streak += 1
        
        if not consecutive:
            key_stats.current_streak = 1

        # Setup the last moment pressed variable
        if key_stats.times_pressed == 1:
            key_stats.last_moment_pressed = time.time()
            return

        interval = int(round((time.time() - key_stats.last_moment_pressed) * 1000))
        key_stats.last_moment_pressed = time.time()
        
        if key_stats.smallest_interval == -1 and key_stats.times_pressed >= 2:
            key_stats.smallest_interval = interval
        
        key_stats.smallest_interval = min(interval, key_stats.smallest_interval)
        key_stats.longest_interval = max(interval, key_stats.longest_interval)


    @staticmethod
    def parse_key_release(key_stats: KeyboardKeyStats):
        KeyboardEventParser.update_on_released(key_stats)

    @staticmethod
    def update_on_released(key_stats: KeyboardKeyStats):
        key_stats.is_pressed = False

        hold_time = int(round((time.time() - key_stats.last_moment_pressed) * 1000))
        
        key_stats.total_hold_time += hold_time
        key_stats.max_hold_time = max(key_stats.max_hold_time, hold_time)