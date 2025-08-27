from Listeners.Listener import Listener, EventTypes
from pynput import keyboard
from pynput import mouse
import threading
import atexit
import time

from Controllers.Controller import Controller

class GeneralListener(Listener):
    paused: bool = False
    running: bool = True

    mouse_thread: threading.Thread
    keyboard_thread: threading.Thread

    def __init__(self, controller: Controller):
        super().__init__(controller)

        self.mouse_thread = threading.Thread(target=self.listen_mouse, daemon=True)
        self.keyboard_thread = threading.Thread(target=self.listen_keyboard, daemon=True)

    def start(self):
        atexit.register(self.stop)
        
        self.mouse_thread.start()
        self.keyboard_thread.start()

        try:
            while self.running:
                # Change this to a update rate
                time.sleep(0.0016)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def stop(self):
        self.running = False
        print("Quitting properly")

        self.mouse_thread.join()
        self.keyboard_thread.join()


    def listen_keyboard(self):
        while self.running:
            if self.paused:
                continue
            
            thread_paused: bool = False
            try:
                with keyboard.Events() as events:
                    event = events.get(1)
                    if event is None:
                        continue

                    event_type: EventTypes

                    if type(event) is keyboard.Events.Press:
                        event_type = EventTypes.KEYBOARD_PRESS
                    if type(event) is keyboard.Events.Release:
                        event_type = EventTypes.KEYBOARD_RELEASE

                    self.send_event(event_type, event)
            except Exception:
                self.paused = True
                thread_paused = True
            
            finally:
                if thread_paused:
                    self.paused = False
                # print(f"Keyboard event: {event}")
        
        print("Stopped keyboard listener")

    def listen_mouse(self):
        while self.running:
            if self.paused:
                continue
            
            thread_paused: bool = False
            try:
                with mouse.Events() as events:
                    event = events.get(1)
                    if event is None:
                        continue

                    event_type: EventTypes
                    if type(event) is mouse.Events.Click:
                        event_type = EventTypes.MOUSE_CLICK
                    if type(event) is mouse.Events.Move:
                        event_type = EventTypes.MOUSE_MOVE

                    self.send_event(event_type, event)
                    # print(f"Mouse event: {event}")                    
            except Exception:
                self.paused = True
                thread_paused = True
            
            finally:
                if thread_paused:
                    self.paused = False

        print("Stopped mouse listener")
    