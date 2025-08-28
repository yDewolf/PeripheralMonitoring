class BaseKeyStats:
    related_key_name: str

    times_pressed: int = 0

    def __init__(self, key_name: str) -> None:
        self.related_key_name = key_name

    def to_string(self) -> str:
        stringified = ""
        stringified += f"{self.related_key_name},"
        stringified += f"{self.times_pressed},"

        return stringified

    @staticmethod
    def get_header() -> str:
        return "KeyName,TimesPressed"