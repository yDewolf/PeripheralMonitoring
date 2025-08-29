
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
    
    def has_data(self) -> bool:
        return len(self.key_list) > 0

    @staticmethod
    def sort_keys(key_a: BaseKeyStats) -> str:
        return key_a.related_key_name
