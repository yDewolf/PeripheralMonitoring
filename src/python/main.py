from Controllers.PeripheralController import PeripheralController
from utils.Chunk.ScreenChunkController import ScreenChunkController
from utils.Chunk.ChunkHolder import ChunkHolder
from Listeners.GeneralListener import GeneralListener

holder = ChunkHolder(32, 32)

chunk_controller = ScreenChunkController(32, "../../saves")
controller = PeripheralController(chunk_controller, True)

listener = GeneralListener(controller)
listener.start()

