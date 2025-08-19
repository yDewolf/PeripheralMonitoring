from pynput.keyboard import Key, Listener
import os
import time
from datetime import datetime

FILE_NAME = "test_save"

class KeyboardHeatmap:
    total_key_presses = 0

    key_press_count = {}
    keys_start_hold_time = {}
    keys_hold_time = {}

    keys_max_hold_time = {}

    consecutive_end = 0

    def start_recording(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener: # type: ignore
            listener.join()

        self.save_to_file(FILE_NAME)

    def on_press(self, key):
        print(f"Pressed {key}")
        if self.key_press_count.get(key, -1) == -1:
            self.key_press_count[key] = 0

            self.keys_max_hold_time[key] = 0
            self.keys_hold_time[key] = 0
            self.keys_start_hold_time[key] = time.time()

        self.key_press_count[key] += 1
        self.total_key_presses += 1

        if key == Key.end:
            self.consecutive_end += 1
        else:
            self.consecutive_end = 0
        
        if self.consecutive_end == 3:
            return False
    
    def on_release(self, key):
        self.keys_hold_time[key] += time.time() - self.keys_start_hold_time[key]
        self.keys_max_hold_time[key] = max(self.keys_hold_time[key], self.keys_max_hold_time[key])

    def save_to_file(self, file_name):
        with open(os.path.join(os.path.dirname(__file__), "saves", ((str) (datetime.strftime(datetime.now(),"%d-%m-%Y_%H-%M-%S")) + ".hmp")), "w+") as file:
            stringified = f"v0.3\n[GENERAL_INFO]\ntotal_presses{self.total_key_presses}\n"

            stringified += "[KEY_PRESSES]\n"
            for key in self.key_press_count:
                stringified += f"{key}: {self.key_press_count[key]}\n"

            stringified += "[KEY_HOLD_TIMES]\n"
            for key in self.keys_hold_time:
                stringified += f"{key}: {self.keys_hold_time[key]}\n"
            
            stringified += "[MAX_KEY_HOLD_TIMES]\n"
            for key in self.keys_max_hold_time:
                stringified += f"{key}: {self.keys_max_hold_time[key]}\n"
            
            file.write(stringified)

heatmap = KeyboardHeatmap()
heatmap.start_recording()