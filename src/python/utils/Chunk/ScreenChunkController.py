from Listeners.data.KeyDataManager import KeyDataManager
from utils.Chunk.Chunk import Vector2i
from utils.Chunk.ScreenChunk import ScreenChunk
from utils.Chunk.ChunkHolder import ChunkHolder
import screeninfo

class ScreenChunkController(ChunkHolder):
    chunk_size: int = 32

    x_bounds: tuple[int, int] = (0, 0)
    y_bounds: tuple[int, int] = (0, 0)

    start_listen_time: float

    def __init__(self, chunk_size: int, chunk_index: dict[str, ScreenChunk] = {}, target_monitors: list[int] = []):
        self.chunk_size = chunk_size

        x_bound: tuple[int | None, int] = (None, 0)
        y_bound: tuple[int | None, int] = (None, 0)
        for idx, monitor in enumerate(screeninfo.get_monitors()):
            if target_monitors != []:
                if not target_monitors.__contains__(idx):
                    continue

            x_bound = (
                min(x_bound[0] if x_bound[0] != None else monitor.x, monitor.x), 
                x_bound[1] + monitor.width
            )
            y_bound = (
                min(y_bound[0] if y_bound[0] != None else monitor.y, monitor.y), 
                max(y_bound[1], monitor.height)
            )
        
        if target_monitors == []:
            self.x_bounds = (0, x_bound[1])
            self.y_bounds = (0, y_bound[1])
        else:
            self.x_bounds = (x_bound[0] if x_bound[0] != None else 0, x_bound[1])
            self.y_bounds = (y_bound[0] if y_bound[0] != None else 0, y_bound[1])

        self.grid_size = Vector2i(
            round(self.x_bounds[1] / self.chunk_size),
            round(self.y_bounds[1] / self.chunk_size)
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