from Listeners.data.MouseButtonStats import MouseButtonStats
from utils.Chunk.ScreenChunk import ScreenChunk


class MouseEventParser:
    last_hovered_chunk: ScreenChunk | None = None

    @staticmethod
    def parse_mouse_press(chunk: ScreenChunk, key_stats: MouseButtonStats):
        pass

    @staticmethod
    def parse_mouse_release(chunk: ScreenChunk, key_stats: MouseButtonStats):
        pass
    

    def parse_mouse_move(self, chunk: ScreenChunk):
        MouseEventParser._parse_mouse_move(chunk, self.last_hovered_chunk) # type: ignore
        self.last_hovered_chunk = chunk

    @staticmethod
    def _parse_mouse_move(chunk: ScreenChunk, last_chunk: ScreenChunk):
        if last_chunk != chunk:
            chunk.times_hovered += 1
        
        last_chunk = chunk