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

    def get_data_as_str(self) -> str:
        stringified: str = "v1"
        stringified += f"\n{self.get_chunk_data_str()}"
        
        return stringified
    
    def get_chunk_data_str(self) -> str:
        stringified = "[CHUNK_DATA]"
        # Headers
        stringified += "\nChunkIdx,TimesHovered,IdleTime,MaxIdleTime,TimesPressed"

        for row in self.chunks:
            for chunk in row:
                if not chunk.has_data():
                    continue
                    
                chunk_idx = self.chunkPosToIdx(chunk.position)
                chunk_str = chunk.stringified()
                stringified += f"\n{chunk_idx},{chunk_str}"

        return stringified