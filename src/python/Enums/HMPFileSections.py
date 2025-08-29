from enum import Enum

class FileSections(Enum):
    GENERAL_KEYBOARD_DATA = "[GeneralKeyData]"
    KEYBOARD_DATA = "<KeyboardData>"
    MOUSE_DATA = "<MouseData>"

    ALL_CHUNK_DATA = "<AllChunkData>"
    CHUNK_DATA = "CHUNK_DATA_"
    CHUNK_KEY_DATA = "<ChunkKeyData>"