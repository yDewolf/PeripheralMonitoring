import os
from Controllers.PeripheralController import PeripheralController
from utils.Chunk.ScreenChunkController import ScreenChunkController
from utils.Chunk.ChunkHolder import ChunkHolder
from Listeners.GeneralListener import GeneralListener

import utils.HmpFileUtils as HMPUtils

holder = ChunkHolder(32, 32)

chunk_controller = ScreenChunkController(32)
controller = PeripheralController(chunk_controller, True)

listener = GeneralListener(controller)
listener.start()

HMPUtils.save_hmp_file(f"{os.path.dirname(__file__)}/../../saves", controller)
# data = controller.get_data_str()
# FileUtils.save_to_file(data, f"{os.path.dirname(__file__)}/../../saves", ".hmp")
