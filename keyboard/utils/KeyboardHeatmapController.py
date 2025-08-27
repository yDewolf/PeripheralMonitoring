from pynput.keyboard import Key, Listener, KeyCode
from utils.KeyStats import KeyStats
import os
from datetime import datetime
import time
class KeyboardHeatmapController:
    version: str = 'v1.0'
    save_path: str
    debug: bool = False

    interrupt_key: Key = Key.end
    keys: dict = {}

    previous_key_name: str = ''

    def __init__(self, save_path: str, debug_mode: bool = False) -> None:
        interrupt_name = self.get_key_name(self.interrupt_key)
        self.add_key_to_list(interrupt_name)
        self.debug = debug_mode
        self.save_path = save_path

    def save_to_file(self, data):
        with open(os.path.join(self.save_path, ((str) (datetime.strftime(datetime.now(),"%d-%m-%Y_%H-%M-%S")) + ".hmp")), "w+") as file:
            print("Saving...".center(30))
            file.write(data)


    def start_listening(self):
        try:
            with Listener(on_press=self.on_key_press, on_release=self.on_key_release) as listener: # type: ignore
                print("Listening...".center(30))
                print(f"To quit and save press {self.interrupt_key} 3 times".center(30))
                while listener.running:
                    listener.is_alive()
                    time.sleep(0.006)
                
        except KeyboardInterrupt:
            pass

        finally:
            self.save_to_file(self.get_data_as_string())


    def on_key_press(self, key: Key | KeyCode):
        key_name = self.get_key_name(key)

        key_stats: KeyStats = self.keys.get(key_name, -1)
        if key_stats == -1:
            key_stats = self.add_key_to_list(key_name)
            # return

        is_consecutive: bool = self.previous_key_name == key_name
        if self.debug:
            print(f"Pressed: {key_name}")
        
        key_stats.update_on_pressed(is_consecutive)
        if self.keys[self.get_key_name(self.interrupt_key)].current_streak >= 3:
            return False
        
        self.previous_key_name = key_name

    def on_key_release(self, key: Key | KeyCode):
        key_name = self.get_key_name(key)
        if self.debug:
            print(f"Released: {key_name}")
        key_stats: KeyStats = self.keys.get(key_name, -1)
        if key_stats == -1:
            return
        
        key_stats.update_on_released()

    def get_data_as_string(self) -> str:
        stringified = ""
        stringified += f"{self.version}"
        
        most_pressed_key: str = ''

        total_key_presses: int = 0
        highest_press_count: int = 0

        for key in self.keys:
            key_stats: KeyStats = self.keys[key]
            total_key_presses += key_stats.times_pressed
            if key_stats.times_pressed > highest_press_count:
                most_pressed_key = key
                highest_press_count = key_stats.times_pressed

        stringified += "\n[GENERAL_INFO]"
        stringified += f"\nTotalKeyPresses: {total_key_presses}"
        stringified += f"\nMostPressedKey: {most_pressed_key}"

        stringified += "\n[KEY_DATA]"
        # Header:
        stringified += "\nKeyName,TimesPressed,MaxPressStreak,LongestInterval,SmallestInterval,TotalHoldTime,MaxHoldTime"
        
        sorted_keys = dict(sorted(self.keys.items()))
        for key in sorted_keys:
            key_stats: KeyStats = self.keys[key]
            stringified += f"\n{key_stats.to_string()}"
        
        return stringified

    def add_key_to_list(self, key_name: str) -> KeyStats:
        key_stats = KeyStats(key_name)
        self.keys[key_name] = key_stats
        
        return key_stats

    @staticmethod
    def get_key_name(key):
        return str(key).lower()