
from Listeners.data.BaseKeyStats import BaseKeyStats
from Listeners.data.KeyboardKeyStats import KeyboardKeyStats
from Listeners.data.MouseButtonStats import MouseButtonStats

class KeyDataManager:
    key_index: dict = {}

    key_list: list[BaseKeyStats] = []

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
        string_data: str = "[KeyData]"

        keyboard_data: str = "\n" + KeyboardKeyStats.get_header()
        mouse_data: str = "\n" + MouseButtonStats.get_header()
        for key in self.key_list:
            if type(key) is KeyboardKeyStats:
                keyboard_data += "\n" + key.to_string()
                continue
            
            if type(key) is MouseButtonStats:
                mouse_data += "\n" + key.to_string()
                continue

        return string_data