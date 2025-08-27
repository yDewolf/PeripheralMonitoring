from Enums.EventTypes import EventTypes
from Listeners.Listener import Listener

class Controller:
    listeners: list[Listener] = []

    def add_listener(self, listener: Listener):
        if self.listeners.__contains__(listener):
            return

        self.listeners.append(listener)


    def parse_event(self, type: EventTypes, event):
        print(f"Received Event! | type: {type.name} | event: {event}")