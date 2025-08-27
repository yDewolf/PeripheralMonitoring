from utils.ChunkHolder import ChunkHolder
from Listeners.GeneralListener import GeneralListener

holder = ChunkHolder(32, 32)

listener = GeneralListener()
listener.start()
