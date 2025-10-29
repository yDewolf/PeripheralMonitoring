from datetime import datetime
import os

indexed_property_names: dict = {}
indexed_headers: dict = {}

def save_to_file(data: str, file_path: str, extension: str) -> None:
    with open(os.path.join(file_path, ((str) (datetime.strftime(datetime.now(),"%d-%m-%Y_%H-%M-%S") + extension))), "w+") as file:
        file.write(data)

def get_file_content(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        lines: list[str] = file.readlines()
        
        return lines

# CSV Utils

def get_property_names(instance: type) -> list[str]:
    properties: list[str] = indexed_property_names.get(str(instance), [])
    if properties != []:
        return properties

    if instance.__base__ != None:
        properties += get_property_names(instance.__base__)

    property_names = instance.__dict__.keys()
    for name in property_names:
        if name.startswith("_"):
            continue

        if callable(getattr(instance, name)):
            continue

        properties.append(name)
    
    indexed_property_names[str(instance)] = properties
    return properties

def generate_header(instance: type | object, capitalized: bool = False) -> str:
    instance_type = instance
    if not type(instance) is type.__class__:
        instance_type = type(instance)
    
    header: str = indexed_headers.get(str(instance_type), "")
    if header != "":
        return header
    
    keys = get_property_names(instance_type) # type: ignore
    for key in keys:
        key_name: str = key

        if capitalized:
            key_parts = key_name.split("_")
            for part in key_parts:
                key_name += part.capitalize()

        header += key_name + ","
    
    header = header.removesuffix(",")
    indexed_headers[str(instance_type)] = header

    return header

def generate_csv_line(instance: object) -> str:
    line: str = ""

    properties = get_property_names(type(instance))
    for idx, property in enumerate(properties):
        line += str(instance.__getattribute__(property))
        if idx < len(properties) - 1:
            line += ","
    
    return line

def get_csv_as_dict(csv_line: str, header: str) -> dict:
    values = csv_line.split(",")
    key_names = header.split(",")

    value_dict: dict = {}
    for idx, key in enumerate(key_names):
        value_dict[key] = parse_value(values[idx])
    
    return value_dict

# Returns the value dict used to set the variables
def set_obj_properties(obj: object, csv_line: str, header: str = "") -> dict:
    if header == "":
        header = generate_header(obj)
        
    value_dict: dict = get_csv_as_dict(csv_line, header)
    for key in value_dict.keys():
        if not hasattr(obj, key):
            continue
        
        value = value_dict[key]
        

        obj.__setattr__(key, value)

    return value_dict

def clean_string(string: str) -> str:
    return string.replace("\t", "").replace("\n", "").replace(" ", "").removesuffix(";")

def parse_value(value_str: str) -> float | int | str | bool | list:
    formatted = clean_string(value_str)
    if is_valid_int(formatted):
        return int(formatted)
    elif is_valid_float(formatted):
        return float(formatted)
    elif formatted.startswith("[") and formatted.endswith("]"):
        formatted = formatted.removeprefix("[").removesuffix("]")
        
        value_list: list = []
        for value in formatted.split(","):
            value_list.append(parse_value(value))
        
        return value_list

    elif formatted.lower() == "false":
        return False
    
    elif formatted.lower() == "true":
        return True

    return formatted

def is_valid_int(string: str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False

def is_valid_float(string: str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False