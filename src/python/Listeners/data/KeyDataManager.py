
from Listeners.data.BaseKeyStats import BaseKeyStats
from Listeners.data.KeyboardKeyStats import KeyboardKeyStats
from Listeners.data.MouseButtonStats import MouseButtonStats

class KeyDataManager:
    key_index: dict

    key_list: list[BaseKeyStats]

    def __init__(self) -> None:
        self.key_index = {}
        self.key_list = []

    def register_key(self, key_stats: BaseKeyStats) -> int:
        key_idx = len(self.key_list)
        self.key_index[key_stats.related_key_name] = key_idx
        self.key_list.append(key_stats)

        return key_idx

    def get_key(self, key_name: str) -> BaseKeyStats | None:
        idx = self.key_index.get(key_name, -1)
        if idx == -1:
            return None

        return self.key_list[idx]
    
    def get_data_as_str(self) -> str:
        string_data: str = ""

        keyboard_data: str = "[KeyboardData]\n" + KeyboardKeyStats.get_header()
        mouse_data: str = "[MouseData]\n" + MouseButtonStats.get_header()
        
        sorted_list = sorted(self.key_list, key=KeyDataManager.sort_keys) # type: ignore
        for key in sorted_list:
            # print(f"Looking at key {key.related_key_name} with type of: {type(key)}")
            if type(key) is KeyboardKeyStats:
                keyboard_data += "\n" + key.to_string()
                continue
            
            if type(key) is MouseButtonStats:
                mouse_data += "\n" + key.to_string()
                continue
        
        string_data += keyboard_data
        string_data += "\n" + mouse_data + "\n"

        return string_data

    @staticmethod
    def sort_keys(key_a: BaseKeyStats) -> str:
        return key_a.related_key_name
