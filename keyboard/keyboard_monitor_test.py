from pynput.keyboard import Key, Listener, KeyCode
import os
import time
from datetime import datetime

from pynput.keyboard._base import KeyCode

FILE_NAME = "test_save"


class KeyboardHeatmap :
    total_key_presses = 0
    key_pressed = {}

    last_moment_key_pressed = {}

    longest_key_press_interval = {}
    smallest_key_press_interval = {}

    key_press_count = {}
    keys_hold_time = {}

    keys_max_hold_time = {}

    consecutive_end = 0

    def start_recording(self):
            with Listener(on_press=self.on_key_press, on_release=self.on_key_release) as listener: # type: ignore
                listener.join()
            
            self.save_to_file()

    def on_key_press(self, key: Key | KeyCode):
        key_name = str(key).lower()
        
        if self.key_pressed.get(key_name, False) == True:
            return
        
        if self.key_press_count.get(key_name, -1) == -1:
            self.key_press_count[key_name] = 0

            self.keys_max_hold_time[key_name] = 0
            self.keys_hold_time[key_name] = 0
            self.last_moment_key_pressed[key_name] = time.time()
        
        print(f"Pressed {key_name}")

        self.key_pressed[key_name] = True

        interval = time.time() - self.last_moment_key_pressed[key_name]
        self.last_moment_key_pressed[key_name] = time.time()
        
        if self.key_press_count[key_name] == 0:
            self.smallest_key_press_interval[key_name] = 2 ** 16
            self.longest_key_press_interval[key_name] = interval
        else:
            self.longest_key_press_interval[key_name] = max(self.longest_key_press_interval[key_name], interval)
            self.smallest_key_press_interval[key_name] = min(self.smallest_key_press_interval[key_name], interval)

        self.key_press_count[key_name] += 1
        self.total_key_presses += 1

        if key == Key.end:
            self.consecutive_end += 1
        else:
            self.consecutive_end = 0
        
        if self.consecutive_end == 3:
            return False
    
    def on_key_release(self, key: Key | KeyCode):
        key_name = str(key).lower()
        
        if self.key_press_count.get(key_name, None) == None:
            print(f"Skipped key: {key_name}")
            return

        print(f"released {key_name}")
        self.key_pressed[key_name] = False

        current_hold_time = time.time() - self.last_moment_key_pressed[key_name]

        self.keys_hold_time[key_name] += current_hold_time
        self.keys_max_hold_time[key_name] = max(current_hold_time, self.keys_max_hold_time[key_name])

    def save_to_file(self):
        with open(os.path.join(os.path.dirname(__file__), "saves", ((str) (datetime.strftime(datetime.now(),"%d-%m-%Y_%H-%M-%S")) + ".hmp")), "w+") as file:
            stringified = f"v0.4\n[GENERAL_INFO]\ntotal_presses: {self.total_key_presses}\n"

            stringified += "[KEY_PRESSES]\n"
            for key in self.key_press_count:
                stringified += f"{key}: {(self.key_press_count[key])}\n"

            stringified += "[LONGEST_KEY_INTERVAL]\n"
            for key in self.longest_key_press_interval:
                stringified += f"{key}: {int(round(self.longest_key_press_interval[key] * 1000))}\n"

            stringified += "[SMALLEST_KEY_INTERVAL]\n"
            for key in self.smallest_key_press_interval:
                stringified += f"{key}: {int(round(self.smallest_key_press_interval[key] * 1000))}\n"

            stringified += "[KEY_HOLD_TIMES]\n"
            for key in self.keys_hold_time:
                stringified += f"{key}: {int(round(self.keys_hold_time[key] * 1000))}\n"
            
            stringified += "[MAX_KEY_HOLD_TIMES]\n"
            for key in self.keys_max_hold_time:
                stringified += f"{key}: {int(round(self.keys_max_hold_time[key] * 1000))}\n"
            
            file.write(stringified)

heatmap = KeyboardHeatmap()
heatmap.start_recording()