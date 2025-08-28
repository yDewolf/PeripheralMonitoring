from utils.Chunk.Chunk import Vector2i
from utils.Chunk.ScreenChunk import ScreenChunk
from utils.Chunk.ChunkHolder import ChunkHolder
import screeninfo

class ScreenChunkController(ChunkHolder):
    chunk_size: int = 32

    start_listen_time: float

    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size
        width: int = 0

        max_height: int = 0
        for monitor in screeninfo.get_monitors():
            max_height = max(max_height, monitor.height)
            width += monitor.width
        
        self.grid_size = Vector2i(
            round(width / self.chunk_size),
            round(max_height / self.chunk_size)
        )

        self.setup()
    
    def setup(self):
        self.chunks = []

        for x in range(self.grid_size.x):
            row = []
            for y in range(self.grid_size.y):
                pos = Vector2i(x, y)
                chunk = ScreenChunk(pos)
                row.append(chunk)
            
            self.chunks.append(row)


    def getChunkAt(self, x: int, y: int) -> ScreenChunk | None:
        return super().getChunkAt(x, y) # type: ignore


    def get_data_str(self) -> str:
        stringified: str = ""
        
        stringified += self.get_chunk_data_str()
        
        return stringified
    
    def get_chunk_data_str(self) -> str:
        stringified = ""

        chunk_strings: list = []
        for row in self.chunks:
            for chunk in row:
                if not chunk.has_data():
                    continue
                
                header = f"\n{self.get_header()},{ScreenChunk.get_header()}"
                
                chunk_idx = self.posToIdx(chunk.position)
                chunk_data_str = f"\n{header}\n{chunk_idx},{chunk.get_chunk_data()}"
                
                other_data = chunk.get_data_str()
                chunk_strings.append(
                    [chunk_idx, f"\n[CHUNK_DATA_{chunk_idx}]\n{chunk_data_str}\n{other_data}"]
                )
        chunk_strings.sort(key=ScreenChunkController.sort_chunk_strings)
        for str_list in chunk_strings:
            stringified += str_list[1]

        return stringified

    @staticmethod
    def get_header() -> str:
        return "ChunkIdx"

    @staticmethod
    def sort_chunk_strings(string_list: list) -> int:
        return string_list[0]