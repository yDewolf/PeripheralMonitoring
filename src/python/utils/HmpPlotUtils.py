from matplotlib.image import AxesImage
import matplotlib.pyplot as pyplot
import numpy

from Controllers.PeripheralController import PeripheralController
from utils.Chunk.ScreenChunk import ScreenChunk

def create_chunk_property_img(controller: PeripheralController, property: str = "times_hovered") -> AxesImage:
    chunk_data = numpy.zeros((
        controller.chunk_controller.grid_size.y,
        controller.chunk_controller.grid_size.x
    ))

    for chunk_row in controller.chunk_controller.chunks:
        for chunk in chunk_row:
            if type(chunk) is ScreenChunk:
                chunk_data[chunk.position.y][chunk.position.x] = chunk.__getattribute__(property)

    normalized = chunk_data / numpy.amax(chunk_data)
    img = pyplot.imshow(normalized, cmap="seismic")
    pyplot.title(f"{property} Heatmap")

    return img

def chunk_data_to_dict(controller: PeripheralController, property: str = "times_hovered"):
    chunk_data: dict = {
        "property": property,
        "chunks": []
    }

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