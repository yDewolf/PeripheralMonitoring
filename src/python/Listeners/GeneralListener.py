from pynput.mouse import Controller as MouseController, Listener as MouseListener
from pynput.keyboard import Controller as KeyboardController, Listener as KeyboardListener
from pynput import keyboard
from pynput import mouse
import threading
import atexit
import time

class GeneralListener:
    keyboard_listener: KeyboardListener
    running: bool = True

    mouse_thread: threading.Thread
    keyboard_thread: threading.Thread

    def __init__(self):
        self.mouse_thread = threading.Thread(target=self.listen_mouse, daemon=True)
        self.keyboard_thread = threading.Thread(target=self.listen_keyboard, daemon=True)

    def start(self):
        atexit.register(self.stop)
        
        self.mouse_thread.start()
        self.keyboard_thread.start()

        try:
            while True:
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
            with keyboard.Events() as events:
                event = events.get(1)
                print(f"Keyboard event: {event}")
        
        print("Stopped keyboard listener")

    def listen_mouse(self):
        while self.running:
            with mouse.Events() as events:
                event = events.get(1)
                print(f"Mouse event: {event}")                    
        
        print("Stopped mouse listener")