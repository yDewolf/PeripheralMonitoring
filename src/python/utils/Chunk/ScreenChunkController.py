from Listeners.data.KeyDataManager import KeyDataManager
from utils.Chunk.Chunk import Vector2i
from utils.Chunk.ScreenChunk import ScreenChunk
from utils.Chunk.ChunkHolder import ChunkHolder
import screeninfo

class ScreenChunkController(ChunkHolder):
    chunk_size: int = 32

    x_bounds: tuple[int, int] = (0, 0)

    start_listen_time: float

    def __init__(self, chunk_size: int, chunk_index: dict[str, ScreenChunk] = {}, target_monitor: int = -1):
        self.chunk_size = chunk_size
        width: int = 0

        max_height: int = 0
        for idx, monitor in enumerate(screeninfo.get_monitors()):
            if target_monitor != idx and target_monitor != -1:
                continue
            else:
                self.x_bounds = (monitor.x, monitor.width)
            
            max_height = max(max_height, monitor.height)
            width += monitor.width
        
        if target_monitor == -1:
            self.x_bounds = (0, width)
        
        self.grid_size = Vector2i(
            round(width / self.chunk_size),
            round(max_height / self.chunk_size)
        )

        self.setup(chunk_index)
    
    def setup(self, chunk_index: dict[str, ScreenChunk] = {}):
        self.chunks = []

        for x in range(self.grid_size.x):
            row = []
            for y in range(self.grid_size.y):
                pos = Vector2i(x, y)
                chunk: ScreenChunk | None = chunk_index.get(str(pos), None)
                if chunk == None: chunk = ScreenChunk(pos)

                row.append(chunk)
            
            self.chunks.append(row)


    def getChunkAt(self, x: int, y: int) -> ScreenChunk | None:
        return super().getChunkAt(x, y) # type: ignore

    @staticmethod
    def sort_chunk_strings(string_list: list) -> int:
        return string_list[0]