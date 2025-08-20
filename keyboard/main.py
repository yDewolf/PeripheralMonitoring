from utils.KeyboardHeatmapController import KeyboardHeatmapController
import os
from datetime import datetime

controller = KeyboardHeatmapController(True)
data = controller.start_listening()
with open(os.path.join(os.path.dirname(__file__), "saves", ((str) (datetime.strftime(datetime.now(),"%d-%m-%Y_%H-%M-%S")) + ".hmp")), "w+") as file:
    file.write(data)

# print(data)