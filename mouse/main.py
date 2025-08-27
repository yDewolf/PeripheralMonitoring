import os
from utils.MonitorChunkController import MonitorChunkController

print('\x1b[3;37;43m' + "".center(30) + '\x1b[0m')
print('\x1b[3;37;43m' + "Mouse Heatmap".center(30) + '\x1b[0m')
print('\x1b[3;37;43m' + "".center(30) + '\x1b[0m')


controller = MonitorChunkController(64, os.path.join(os.path.dirname(__file__), "saves"))
controller.start_listening()