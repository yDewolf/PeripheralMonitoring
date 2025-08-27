from utils.Chunk import Chunk
from utils.Chunk import Vector2i

class ChunkHolder:
    grid_size: Vector2i
    chunks: list[list[Chunk]]

    def __init__(self, grid_width: int, grid_height: int):
        self.grid_size = Vector2i(grid_width, grid_height)
        self.chunks = []

        for x in range(self.grid_size.x):
            row = []
            for y in range(self.grid_size.y):
                chunk = Chunk(Vector2i(x, y))
                row.append(chunk)
            
            self.chunks.append(row)
    
    def posToIdx(self, pos: Vector2i) -> int:
        return pos.x + (pos.y * self.grid_size.y)
    
    ## Override this on other classes
    def get_data_str(self) -> str:
        return ""