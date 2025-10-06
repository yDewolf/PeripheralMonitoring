from Controllers.PeripheralController import PeripheralController
from utils.Chunk.ScreenChunk import ScreenChunk
import numpy

def chunk_data_to_dict(controller: PeripheralController, property: str = "times_hovered"):
    chunk_data: dict = {
        "property": property,
        "chunks": []
    }
    
    try:
        controller.chunk_controller.chunks[0][0].__getattribute__(property)
    except AttributeError:
        return chunk_data

    chunks = numpy.zeros((
        controller.chunk_controller.grid_size.y,
        controller.chunk_controller.grid_size.x
    ))

    for chunk_row in controller.chunk_controller.chunks:
        for chunk in chunk_row:
            if type(chunk) is ScreenChunk:
                chunks[chunk.position.y][chunk.position.x] = chunk.__getattribute__(property)

    chunk_data["chunks"] = numpy.ndarray.tolist(chunks / numpy.amax(chunks))

    return chunk_data