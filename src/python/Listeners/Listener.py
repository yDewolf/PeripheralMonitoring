from Enums.EventTypes import EventTypes
from Controllers.Controller import Controller

class Listener:
    controller: Controller

    def __init__(self, controller):
        self.set_controller(controller)

    def set_controller(self, controller):
        self.controller = controller
        controller.add_listener(self)

    def send_event(self, type: EventTypes, event):
        self.controller.parse_event(type, event)
