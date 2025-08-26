import os
from utils.MonitorChunkController import MonitorChunkController

controller = MonitorChunkController(64, os.path.join(os.path.dirname(__file__), "saves"))
controller.start_listening()