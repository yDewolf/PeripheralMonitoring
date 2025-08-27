from utils.ChunkController import ChunkController
from pynput.mouse import Listener as MouseListener
# from pynput.keyboard import Listener as KeyboardListener
from utils.Chunk import Chunk

import screeninfo
import time
import os
from datetime import datetime

class MonitorChunkController(ChunkController):
    save_path: str
    chunk_size: int = 32
    start_listen_time: float

    properly_setup: bool = False

    previous_hovered_chunk: Chunk
    chunk_start_idle_time: float

    def __init__(self, chunk_size: int, save_path: str) -> None:
        super().__init__()
        self.chunk_size = chunk_size
        self.save_path = save_path

        total_width: int = 0
        max_height: int = 0
        for monitor in screeninfo.get_monitors():
            max_height = max(max_height, monitor.height)
            total_width += monitor.width

        super().setup(
            round(total_width / self.chunk_size), 
            round(max_height / chunk_size)
        )

    def save_to_file(self, data: str) -> None:
        with open(os.path.join(self.save_path, ((str) (datetime.strftime(datetime.now(),"%d-%m-%Y_%H-%M-%S")) + ".hmp")), "w+") as file:
            print("Saving...".center(30))
            file.write(data)

    def get_data_as_str(self) -> str:
        stringified: str = "v1"
        stringified += f"\nRuntimeInMs: {int(round((time.time() - self.start_listen_time) * 1000))}"
        
        stringified += f"\n{self.get_chunk_data_str()}"
        
        return stringified

    def start_listening(self):
        try:
            with MouseListener(
                on_move=self.on_mouse_move,
                on_click=self.on_mouse_click,
            ) as listener:
                self.start_listen_time = time.time()
                print("Listening...".center(30))
                print(f"To quit and save press the middle button on chunk (0, 0)".center(30))
                listener.join()
        
        except KeyboardInterrupt:
            pass
            
        finally:
            data = self.get_data_as_str()
            self.save_to_file(data)

            return data

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
        
        if chunk.position == (0, 0) and button.name == "middle":
            return False

    
    def get_chunk_at_mouse_pos(self, x: int, y: int) -> Chunk:
        chunk_pos: tuple = (
            min(max(x // self.chunk_size, 0), self.grid_size[0] - 1),
            min(max(y // self.chunk_size, 0), self.grid_size[1] - 1)
        )
        # print(chunk_pos)

        return self.chunks[chunk_pos[0]][chunk_pos[1]]