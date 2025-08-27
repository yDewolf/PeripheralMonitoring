from Controllers.Controller import Controller
from Enums.EventTypes import EventTypes

from pynput.keyboard import KeyboardEvents

class ListenerController(Controller):
    def parse_event(self, type: EventTypes, event):
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

    def parse_keyboard_event(type: EventTypes, event: KeyboardEvents):
        pass


    def parse_mouse_event(type: EventTypes, event: KeyboardEvents):
        pass