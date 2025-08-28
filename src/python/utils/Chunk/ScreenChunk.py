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
    