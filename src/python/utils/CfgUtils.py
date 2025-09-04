import utils.FileUtils as FileUtils
import re as regex
import os

def save_configs(data: dict[str, object], file_path: str):
    pass

def load_configs(file_path: str) -> dict[str, int | float | str | bool]:
    data: dict[str, int | float | str | bool] = {}
    lines: list[str] = FileUtils.get_file_content(file_path)
    for line in lines:
        if line == "":
            continue
        
        if line.startswith("#"):
            continue

        line_split: list[str] = line.split(":")
        if len(line_split) < 2:
            continue
        
        data[line_split[0]] = FileUtils.parse_value(line_split[1])

    return data
