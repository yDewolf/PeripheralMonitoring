from Enums.EventTypes import EventTypes


class Controller:
    listeners: list = []
    start_listen_time: float

    def add_listener(self, listener):
        if self.listeners.__contains__(listener):
            return

        self.listeners.append(listener)

    def parse_event(self, type: EventTypes, event):
        print(f"Received Event! | type: {type.name} | event: {event}")
    