from Controllers.Controller import Controller
from Enums.EventTypes import EventTypes

from pynput.keyboard import Events as KeyboardEvents
from pynput.mouse import Events as MouseEvents

from Listeners.data.KeyDataManager import KeyDataManager
from utils.Chunk.ScreenChunk import ScreenChunk
from utils.EventParsing.KeyboardEventParser import KeyboardEventParser
from utils.Chunk.ScreenChunkController import ScreenChunkController
from utils.Chunk.Chunk import Chunk
from Listeners.data.KeyboardKeyStats import KeyboardKeyStats

class PeripheralController(Controller):
    debug: bool = False

    chunk_controller: ScreenChunkController
    current_chunk: ScreenChunk | None
    key_data_manager: KeyDataManager

    # Parsers
    keyboard_parser: KeyboardEventParser

    def __init__(self, chunk_controller: ScreenChunkController, debug_mode: bool = False) -> None:
        super().__init__()
        self.debug = debug_mode
        self.chunk_controller = chunk_controller

        self.key_data_manager = KeyDataManager()
        self.keyboard_parser = KeyboardEventParser()

    def get_data_str(self) -> str:
        string_data: str = "v1.6"
        string_data += "\n" + self.key_data_manager.get_data_as_str()

        return string_data


    def parse_event(self, type: EventTypes, event):
        if self.debug:
            print(f"Received Event! | type: {type.name} | event: {event}")
        
        match type:
            case EventTypes.KEYBOARD_PRESS:
                self.parse_keyboard_event(type, event)
                return
            
            case EventTypes.KEYBOARD_RELEASE:
                self.parse_keyboard_event(type, event)
                return


            case EventTypes.MOUSE_CLICK:
                self.parse_mouse_event(type, event)
                return

            case EventTypes.MOUSE_MOVE:
                self.parse_mouse_event(type, event)
                return

    def parse_keyboard_event(self, type: EventTypes, event: KeyboardEvents.Press):
        if event.key == None:
            return

        key_name = KeyboardKeyStats.get_key_name(event.key)
        key_stats: KeyboardKeyStats = self.key_data_manager.get_key(key_name) # type: ignore
        if key_stats == -1:
            key_stats = KeyboardKeyStats(key_name) 
            self.key_data_manager.register_key(key_stats)

        self.match_keyboard_event_type(type, key_stats)

        if self.current_chunk != None:
            chunk_key_stats: KeyboardKeyStats = self.current_chunk.key_manager.get_key(key_name) # type: ignore
            self.match_keyboard_event_type(type, chunk_key_stats)

    def parse_mouse_event(self, type: EventTypes, event: MouseEvents.Move):
        self.current_chunk = self.chunk_controller.getChunkAt(event.x, event.y)
        if self.current_chunk == None:
            return

    def match_keyboard_event_type(self, type: EventTypes, key_stats: KeyboardKeyStats):
        match type:
            case EventTypes.KEYBOARD_PRESS:
                self.keyboard_parser.parse_key_press(key_stats) # type: ignore
            
            case EventTypes.KEYBOARD_RELEASE:
                self.keyboard_parser.parse_key_release(key_stats) # type: ignore