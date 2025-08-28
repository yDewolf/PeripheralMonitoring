from Enums.EventTypes import EventTypes


class Controller:
    listeners: list = []

    def add_listener(self, listener):
        if self.listeners.__contains__(listener):
            return

        self.listeners.append(listener)

    def parse_event(self, type: EventTypes, event):
        print(f"Received Event! | type: {type.name} | event: {event}")
    
    def get_data_str(self) -> str:
        return ""