
class ConsoleInputHandler:
    @staticmethod
    def selectFromOptions(message: str, options: list[str], last_as_zero: bool = True) -> int:
        # Print options:
        options_str = ""
        for idx, option in enumerate(options):
            pos = idx + 1
            if last_as_zero:
                
                if idx == len(options) - 1:
                    pos = 0

            options_str += f"[{pos}]-{option}\n"
        
        print(f"{message}\n{options_str}")
        while True:
            choice_idx = int(input(">> ")) - int(not last_as_zero)

            if choice_idx >= 0 and choice_idx < len(options):
                if last_as_zero:
                    if choice_idx == 0:
                        return choice_idx

                    return choice_idx


                return choice_idx
    
    @staticmethod
    def confirmChoice(message: str):
        return bool(ConsoleInputHandler.selectFromOptions(message, ["Yes", "No"]))