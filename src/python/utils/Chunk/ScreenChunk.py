from Listeners.data.KeyDataManager import KeyDataManager
from utils.Chunk.Chunk import Vector2i
from utils.Chunk.Chunk import Chunk

class ScreenChunk(Chunk):
    times_hovered: int = 0

    idle_time: int = 0
    max_idle_time: int = 0

    afk_time: int = 0

    key_manager: KeyDataManager

    def __init__(self, position: Vector2i):
        super().__init__(position)

        self.key_manager = KeyDataManager()
    
    def get_data_str(self) -> str:
        string_data: str = ""
        string_data += "[ChunkKeyData]\n" + self.key_manager.get_data_as_str()

        return string_data

    # CSV format
    def get_chunk_data(self) -> str:
        string_data: str = ""

        string_data += f"{self.times_hovered},"
        string_data += f"{self.idle_time},"
        string_data += f"{self.max_idle_time},"
        string_data += f"{self.afk_time}"

        return string_data


    def has_data(self) -> bool:
        return self.times_hovered != 0

    @staticmethod
    def get_header() -> str:
        return "TimesHovered,IdleTime,MaxIdleTime,AfkTime"