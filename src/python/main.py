import os
from Controllers.PeripheralController import PeripheralController
from utils.Chunk.ScreenChunk import ScreenChunk
from utils.Chunk.ScreenChunkController import ScreenChunkController
from utils.Chunk.ChunkHolder import ChunkHolder
from Listeners.GeneralListener import GeneralListener

import utils.HmpFileUtils as HMPUtils

import matplotlib.pyplot as pyplot
import numpy

print('\x1b[3;37;44m' + "".center(30) + '\x1b[0m')
print('\x1b[3;37;44m' + "Peripheral Monitor".center(30) + '\x1b[0m')
print('\x1b[3;37;44m' + "".center(30) + '\x1b[0m')


chunk_controller = ScreenChunkController(16)
controller = PeripheralController(chunk_controller, False)

listener = GeneralListener(controller)
listener.start()

HMPUtils.save_hmp_file(controller, f"{os.path.dirname(__file__)}/../../saves", ignore_empty_chunks=True)

chunk_data = numpy.zeros((
    controller.chunk_controller.grid_size.y,
    controller.chunk_controller.grid_size.x
))

for chunk_row in controller.chunk_controller.chunks:
    for chunk in chunk_row:
        if type(chunk) is ScreenChunk:
            chunk_data[chunk.position.y][chunk.position.x] = chunk.times_hovered

normalized = chunk_data / numpy.amax(chunk_data)
img = pyplot.imshow(normalized, cmap="seismic")
pyplot.show()