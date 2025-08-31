from enum import Enum

class FileSections(Enum):
    GENERAL_KEYBOARD_DATA = "[GeneralKeyData]"
    KEYBOARD_DATA = "<KeyboardData>"
    MOUSE_DATA = "<MouseData>"

    ALL_CHUNK_DATA = "<AllChunkData>"
    CHUNK_DATA = "CHUNK_DATA_"
    CHUNK_KEY_DATA = "<ChunkKeyData>"

class FileVariables(Enum):
    CHUNK_SIZE = "ChunkSize"
    TAGS = "Tags"
    MOST_PRESSED_KEY = "MostPressedKey"
    RUNTIME_MS = "RuntimeInMs"
    CHUNK_DATA_HEADER = "ChunkDataHeader"