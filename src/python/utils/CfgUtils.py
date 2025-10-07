import utils.FileUtils as FileUtils

def save_configs(data: dict[str, object], file_path: str):
    with open(file_path, "w+") as file:
        file_contents: str = ""
        for key in data:
            file_contents += f"{key}: {data[key]}\n"

        file.write(file_contents) 

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
