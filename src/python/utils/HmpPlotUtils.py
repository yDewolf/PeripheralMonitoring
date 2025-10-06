from matplotlib.image import AxesImage
import matplotlib.pyplot as pyplot
import numpy

from Controllers.PeripheralController import PeripheralController
from Listeners.data.BaseKeyStats import BaseKeyStats
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

def create_chunk_key_data_img(controller: PeripheralController, key_name: str) -> AxesImage | None:
    chunk_data = numpy.zeros((
        controller.chunk_controller.grid_size.y,
        controller.chunk_controller.grid_size.x
    ))

    for chunk_row in controller.chunk_controller.chunks:
        for chunk in chunk_row:
            if type(chunk) is ScreenChunk:
                key_stats: BaseKeyStats | None = chunk.key_manager.get_key(key_name)
                value: int = 0
                if key_stats != None:
                    value = key_stats.times_pressed

                chunk_data[chunk.position.y][chunk.position.x] = value

    normalized = chunk_data / numpy.amax(chunk_data)
    img = pyplot.imshow(normalized, cmap="seismic")
    pyplot.title(f"{property} Heatmap")

    return img


