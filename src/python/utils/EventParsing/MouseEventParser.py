import time
from Listeners.data.MouseButtonStats import MouseButtonStats
from utils.Chunk.ScreenChunk import ScreenChunk


class MouseEventParser:
    last_hovered_chunk: ScreenChunk | None = None

    @staticmethod
    def parse_mouse_press(chunk: ScreenChunk, key_stats: MouseButtonStats):
        if key_stats._is_pressed:
            return

        key_stats.times_pressed += 1
        key_stats._is_pressed = True

        key_stats.update_interval_variables()

    @staticmethod
    def parse_mouse_release(chunk: ScreenChunk, key_stats: MouseButtonStats):
        key_stats._is_pressed = False
    

    def parse_mouse_move(self, chunk: ScreenChunk):
        MouseEventParser._parse_mouse_move(chunk, self.last_hovered_chunk) # type: ignore
        self.last_hovered_chunk = chunk

    @staticmethod
    def _parse_mouse_move(chunk: ScreenChunk, last_chunk: ScreenChunk):
        if last_chunk == None:
            return

        if last_chunk != chunk:
            chunk.times_hovered += 1

            # Set the value to a reasonable value
            if last_chunk._start_idle_time == 0:
                last_chunk._start_idle_time = time.time()

            previous_chunk_idle_time = int(round((time.time() - last_chunk._start_idle_time) * 1000))
            if previous_chunk_idle_time > last_chunk._IDLE_TO_AFK_THRESHOLD:
                last_chunk.afk_time += previous_chunk_idle_time
                last_chunk.max_afk_time = max(last_chunk.max_afk_time, previous_chunk_idle_time)
            else:
                last_chunk.idle_time += previous_chunk_idle_time
                last_chunk.max_idle_time = max(last_chunk.max_idle_time, previous_chunk_idle_time)

        last_chunk._start_idle_time = time.time()