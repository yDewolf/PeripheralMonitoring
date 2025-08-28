from utils.Chunk.Chunk import Vector2i
from utils.Chunk.ScreenChunk import ScreenChunk
from utils.Chunk.ChunkHolder import ChunkHolder
import screeninfo
import utils.FileUtils as FileUtils
import time

class ScreenChunkController(ChunkHolder):
    chunk_size: int = 32
    default_save_path: str = "saves"
    CHUNK_HEADER: str = "ChunkIdx,TimesHovered,IdleTime,MaxIdleTime,TimesPressed"

    start_listen_time: float

    def __init__(self, chunk_size: int, save_path: str = ""):
        self.chunk_size = chunk_size
        self.default_save_path = save_path
        width: int = 0
        height: int = 0

        max_height: int = 0
        for monitor in screeninfo.get_monitors():
            max_height = max(max_height, monitor.height)
            width += monitor.width
        
        self.grid_size = Vector2i(
            round(width / self.chunk_size),
            round(height / self.chunk_size)
        )

        self.setup()
    
    def save(self):
        FileUtils.save_to_file(self.get_data_str(), self.default_save_path)
    
    def setup(self):
        self.chunks = []

        for x in range(self.grid_size.x):
            row = []
            for y in range(self.grid_size.y):
                chunk = ScreenChunk(Vector2i(x, y))
                row.append(chunk)
            
            self.chunks.append(row)


    def getChunkAt(self, x: int, y: int) -> ScreenChunk | None:
        return super().getChunkAt(x, y) # type: ignore


    def get_data_str(self) -> str:
        stringified: str = "v1.2"
        stringified += f"\nRuntimeInMs: {int(round((time.time() - self.start_listen_time) * 1000))}"
        
        stringified += f"\n{self.get_chunk_data_str()}"
        
        return stringified
    
    def get_chunk_data_str(self) -> str:
        stringified = "[CHUNK_DATA]"
        # Headers
        stringified += f"\n{self.CHUNK_HEADER}"

        for row in self.chunks:
            for chunk in row:
                if not chunk.has_data():
                    continue
                    
                chunk_idx = self.posToIdx(chunk.position)
                chunk_str = chunk.get_data_str()
                stringified += f"\n{chunk_idx},{chunk_str}"

        return stringified