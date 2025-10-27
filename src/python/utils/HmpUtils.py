# from Controllers.PeripheralController import PeripheralController
from utils.Chunk.Chunk import Chunk, Vector2i
from utils.Chunk.ScreenChunk import ScreenChunk
# import numpy

def chunk_data_to_dict(chunks: list[list[Chunk]], property: str = "times_hovered") -> dict:
    chunk_data: dict = {
        "property": property,
        "chunks": {}
    }
    
    try:
        chunks[0][0].__getattribute__(property)
    except AttributeError:
        return chunk_data

    chunk_values: dict[str, float] = {}
    maximum: float = 0.0
    for chunk_row in chunks:
        for chunk in chunk_row:
            if type(chunk) is ScreenChunk:
                value: float = chunk.__getattribute__(property)
                if value == 0:
                    continue
                
                chunk_values[f"{chunk.position.x},{chunk.position.y}"] = value
                maximum = max(maximum, value)

    for key in chunk_values:
        chunk_values[key] = chunk_values[key] / maximum

    chunk_data["chunks"] = chunk_values
    return chunk_data

def chunk_data_to_dict_from_pos(chunks: list[list[Chunk]], positions: list[Vector2i], property: str = "times_hovered"):
    chunk_data: dict = {
        "property": property,
        "chunks": {}
    }
    
    try:
        chunks[0][0].__getattribute__(property)
    except AttributeError:
        return chunk_data

    chunk_values: dict[str, float] = {}
    maximum: float = 0.0
    for pos in positions:
        chunk = chunks[pos.x][pos.y]
        if type(chunk) is ScreenChunk:
            value: float = chunk.__getattribute__(property)
            if value == 0:
                continue
            
            chunk_values[f"{chunk.position.x},{chunk.position.y}"] = value
            maximum = max(maximum, value)

    for key in chunk_values:
        chunk_values[key] = chunk_values[key] / maximum

    chunk_data["chunks"] = chunk_values
    return chunk_data