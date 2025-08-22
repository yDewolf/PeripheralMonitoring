import time
import os
from utils.KeyboardHeatmapController import KeyboardHeatmapController


print('\x1b[3;37;44m' + "".center(30) + '\x1b[0m')
print('\x1b[3;37;44m' + "Keyboard Heatmap".center(30) + '\x1b[0m')
print('\x1b[3;37;44m' + "".center(30) + '\x1b[0m')

controller = KeyboardHeatmapController(os.path.join(os.path.dirname(__file__), "saves"), False)
data = controller.start_listening()

# print(data)