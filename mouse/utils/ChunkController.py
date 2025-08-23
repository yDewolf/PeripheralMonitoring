from utils.Chunk import Chunk

class ChunkController:
    grid_size: tuple
    chunks: list[list]

    def setup(self, grid_width: int, grid_height: int):
        self.grid_size = (grid_width, grid_height)
        self.chunks = []
        for x in range(grid_width):
            row: list[Chunk] = []
            for y in range(grid_height):
                row.append(Chunk((x, y)))
            
            self.chunks.append(row)
            
    
    def chunkPosToIdx(self, pos: tuple) -> int:
        return pos[0] + (pos[1] * self.grid_size[0])