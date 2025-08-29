import time
from Controllers.Controller import Controller
from Enums.EventTypes import EventTypes

from pynput.keyboard import Events as KeyboardEvents
from pynput.mouse import Events as MouseEvents

from Listeners.data.KeyDataManager import KeyDataManager
from Listeners.data.MouseButtonStats import MouseButtonStats
from utils.EventParsing.MouseEventParser import MouseEventParser
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
    mouse_parser: MouseEventParser

    def __init__(self, chunk_controller: ScreenChunkController, debug_mode: bool = False) -> None:
        super().__init__()
        self.debug = debug_mode
        self.chunk_controller = chunk_controller

        self.key_data_manager = KeyDataManager()
        self.keyboard_parser = KeyboardEventParser()
        self.mouse_parser = MouseEventParser()


    def parse_event(self, type: EventTypes, event):
        # if self.debug:
        #     print(f"Received Event! | type: {type.name} | event: {event}")
        
        # TODO: Optmize this
        match type:
            case EventTypes.KEYBOARD_PRESS:
                self.parse_keyboard_event(type, event)
                return
            
            case EventTypes.KEYBOARD_RELEASE:
                self.parse_keyboard_event(type, event)
                return

            case EventTypes.MOUSE_BUTTON_PRESS:
                self.parse_mouse_event(type, event)
                return

            case EventTypes.MOUSE_BUTTON_RELEASE:
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
        if key_stats == None:
            key_stats = KeyboardKeyStats(key_name) 
            self.key_data_manager.register_key(key_stats)

        self.match_keyboard_event_type(type, key_stats)

        if self.current_chunk != None:
            chunk_key_stats: KeyboardKeyStats = self.current_chunk.key_manager.get_key(key_name) # type: ignore
            if chunk_key_stats == None:
                chunk_key_stats = KeyboardKeyStats(key_name) 
                self.current_chunk.key_manager.register_key(chunk_key_stats)

            self.match_keyboard_event_type(type, chunk_key_stats)

    def match_keyboard_event_type(self, type: EventTypes, key_stats: KeyboardKeyStats):
        match type:
            case EventTypes.KEYBOARD_PRESS:
                if self.debug:
                    print(f"DEBUG: Parsing {type}")
                self.keyboard_parser.parse_key_press(key_stats) # type: ignore
            
            case EventTypes.KEYBOARD_RELEASE:
                if self.debug:
                    print(f"DEBUG: Parsing {type}")
                self.keyboard_parser.parse_key_release(key_stats) # type: ignore

            case _:
                print(f"ERROR: Event Type not handled... | type: {type}")


    def parse_mouse_event(self, event_type: EventTypes, event: MouseEvents.Click):
        x = min(max(event.x // self.chunk_controller.chunk_size, 0), self.chunk_controller.grid_size.x - 1)
        y = min(max(event.y // self.chunk_controller.chunk_size, 0), self.chunk_controller.grid_size.y - 1)
        self.current_chunk = self.chunk_controller.getChunkAt(
            x, y
        )

        if self.current_chunk == None:
            print(f"ERROR: Current chunk is None on Mouse Event | Pos: ({x}, {y})")
            return

        button_stats: MouseButtonStats = None # type: ignore
        if type(event) is MouseEvents.Click:
            key_name = MouseButtonStats.get_button_name(event.button)
            button_stats = self.key_data_manager.get_key(key_name) # type: ignore
            if button_stats == None:
                button_stats = MouseButtonStats(key_name)
                self.key_data_manager.register_key(button_stats)

        self.match_mouse_event_type(event_type, self.current_chunk, button_stats) # type: ignore
        # general_stats = self.key_data_manager.get_key(button_stats.related_key_name)

    def match_mouse_event_type(self, type: EventTypes, chunk: ScreenChunk, button_stats: MouseButtonStats):
        match type:
            case EventTypes.MOUSE_MOVE:
                if self.debug:
                    print(f"DEBUG: Parsing {type}")
                self.mouse_parser.parse_mouse_move(chunk)
                return
            
            case EventTypes.MOUSE_BUTTON_PRESS:
                if self.debug:
                    print(f"DEBUG: Parsing {type}")

                self.mouse_parser.parse_mouse_press(chunk, button_stats)
                return

            case EventTypes.MOUSE_BUTTON_RELEASE:
                if self.debug:
                    print(f"DEBUG: Parsing {type}")

                self.mouse_parser.parse_mouse_release(chunk, button_stats)
                return
            
            case _:
                print(f"ERROR: Event Type not handled... | type: {type}")
