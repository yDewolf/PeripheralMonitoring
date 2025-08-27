from utils.ChunkHolder import ChunkHolder
import screeninfo
import utils.FileUtils as FileUtils
import time

class ChunkController(ChunkHolder):
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
        
        super().__init__(
            round(width / self.chunk_size),
            round(height / self.chunk_size)
        )
    
    def save(self):
        FileUtils.save_to_file(self.get_data_str(), self.default_save_path)
    

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