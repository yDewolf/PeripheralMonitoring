import os
from utils.MonitorChunkController import MonitorChunkController
import numpy
import matplotlib.pyplot as pyplot

print('\x1b[3;37;43m' + "".center(30) + '\x1b[0m')
print('\x1b[3;37;43m' + "Mouse Heatmap".center(30) + '\x1b[0m')
print('\x1b[3;37;43m' + "".center(30) + '\x1b[0m')


controller = MonitorChunkController(16, os.path.join(os.path.dirname(__file__), "saves"))
data = controller.start_listening()

chunk_hovers = numpy.zeros((controller.grid_size[1], controller.grid_size[0]))

for chunk_row in controller.chunks:
    for chunk in chunk_row:
        chunk_hovers[chunk.position[1]][chunk.position[0]] = chunk.times_hovered

img = pyplot.imshow(chunk_hovers, cmap="gray")
pyplot.show()