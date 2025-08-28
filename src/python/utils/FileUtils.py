from datetime import datetime
import os

def save_to_file(data: str, file_path: str, extension: str) -> None:
    with open(os.path.join(file_path, ((str) (datetime.strftime(datetime.now(),"%d-%m-%Y_%H-%M-%S") + extension))), "w+") as file:
        file.write(data)