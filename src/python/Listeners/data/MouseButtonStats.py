
from Listeners.data.BaseKeyStats import BaseKeyStats


class MouseButtonStats(BaseKeyStats):
    @staticmethod
    def get_header() -> str:
        return BaseKeyStats.get_header()
    
    @staticmethod 
    def get_button_name(button) -> str:
        return str(button).lower()