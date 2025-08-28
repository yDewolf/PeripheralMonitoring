from Listeners.data.KeyDataManager import KeyDataManager
from Listeners.data.KeyboardKeyStats import KeyboardKeyStats
from Listeners.data import MouseButtonStats

FORMAT_VERSION: int = 3
indexed_headers: dict = {}
indexed_property_names: dict = {}


def _get_data_from_keymanager(key_manager: KeyDataManager, with_headers: bool = True) -> str:
    string_data: str = ""
    if not key_manager.has_data():
        return string_data

    keyboard_data: str = ""
    mouse_data: str = ""
    if with_headers:
        keyboard_data = "[KeyboardData]\n" + generate_header(KeyboardKeyStats)
        mouse_data = "[MouseData]\n" + generate_header(MouseButtonStats)
    
    sorted_list = sorted(key_manager.key_list, key=KeyDataManager.sort_keys) # type: ignore
    for key in sorted_list:
        key_csv = generate_csv_line(key)
        if type(key) is KeyboardKeyStats:
            if keyboard_data == "":
                keyboard_data += key_csv
                continue
            
            keyboard_data += "\n" + key_csv
            continue
        
        if type(key) is MouseButtonStats:
            if mouse_data == "":
                keyboard_data += key_csv
                continue
            
            mouse_data += "\n" + key_csv
            continue
    
    string_data += keyboard_data
    string_data += "\n" + mouse_data + "\n"

    return string_data


def get_property_names(instance: type) -> list:
    properties: list = indexed_property_names.get(str(instance), [])
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

def generate_header(instance: type | object) -> str:
    instance_type = instance
    if not type(instance) is type.__class__:
        instance_type = type(instance)
    
    header: str = indexed_headers.get(str(instance_type), "")
    if header != "":
        return header
    
    keys = get_property_names(instance_type)
    for key in keys:
        key_parts = key.split("_")
        key_name: str = ""
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