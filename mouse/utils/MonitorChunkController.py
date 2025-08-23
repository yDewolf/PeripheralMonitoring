from utils.ChunkController import ChunkController
from pynput.mouse import Controller, Listener
from utils.Chunk import Chunk

import screeninfo
import math
import time

class MonitorChunkController(ChunkController):
    chunk_size: int = 32

    properly_setup: bool = False

    previous_hovered_chunk: Chunk
    chunk_start_idle_time: float

    

    def __init__(self, chunk_size: int) -> None:
        super().__init__()
        self.chunk_size = chunk_size

        total_width: int = 0
        max_height: int = 0
        for monitor in screeninfo.get_monitors():
            max_height = max(max_height, monitor.height)
            total_width += monitor.width

        super().setup(
            round(total_width / self.chunk_size), 
            round(max_height / chunk_size)
        )

    
    def start_listening(self):
        with Listener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
        ) as listener:
            listener.join()

    def on_mouse_move(self, x, y):
        chunk: Chunk = self.get_chunk_at_mouse_pos(x, y)

        if self.properly_setup:
            # Moved to other chunk
            if self.previous_hovered_chunk != chunk:
                chunk.times_hovered += 1
                
                previous_chunk_idle_time = int(round((time.time() - self.chunk_start_idle_time) * 1000))
                self.previous_hovered_chunk.idle_time += previous_chunk_idle_time
                self.previous_hovered_chunk.max_idle_time = max(self.previous_hovered_chunk.max_idle_time, previous_chunk_idle_time)

        self.chunk_start_idle_time = time.time()
        self.previous_hovered_chunk = chunk

        self.properly_setup = True

    def on_mouse_click(self, x, y, button, pressed):
        chunk: Chunk = self.get_chunk_at_mouse_pos(x, y)
        
        if pressed:
            chunk.times_pressed[button.name] += 1

    
    def get_chunk_at_mouse_pos(self, x: int, y: int) -> Chunk:
        chunk_pos: tuple = (
            math.floor(x / self.chunk_size),
            math.floor(y / self.chunk_size)
        )

        return self.chunks[chunk_pos[0]][chunk_pos[1]]