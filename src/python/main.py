from utils.Chunk.ChunkHolder import ChunkHolder
from Listeners.GeneralListener import GeneralListener
from Controllers.Controller import Controller

holder = ChunkHolder(32, 32)

controller = Controller()

listener = GeneralListener(controller)
listener.start()
