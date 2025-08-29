from datetime import datetime
import os
import time
import re as regex
from Listeners.data.KeyDataManager import KeyDataManager
from Listeners.data.KeyboardKeyStats import KeyboardKeyStats
from Listeners.data.MouseButtonStats import MouseButtonStats
from Controllers.PeripheralController import PeripheralController
from Enums.HMPFileSections import FileSections
from utils.Chunk.Chunk import Vector2i
from utils.Chunk.ScreenChunkController import ScreenChunkController
from utils.Chunk.ScreenChunk import ScreenChunk

FORMAT_VERSION: int = 5
FILE_EXTENSION: str = ".hmp"
CHUNK_CONTROLLER_EXTRA_HEADERS: list[str] = ["PosX", "PosY"]
indexed_headers: dict = {}
indexed_property_names: dict = {}

# Data getters for PeripheralController related classes

def _get_key_manager_data(key_manager: KeyDataManager, with_headers: bool = True) -> str:
    string_data: str = ""
    if not key_manager.has_data():
        return string_data

    keyboard_data: str = ""
    mouse_data: str = ""
    if with_headers:
        keyboard_data += "\n" + generate_header(KeyboardKeyStats)
        mouse_data += "\n" + generate_header(MouseButtonStats)
    
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
    
    string_data += f"{FileSections.KEYBOARD_DATA}\n"
    for line in keyboard_data.splitlines(True):
        string_data += "\t" + line
    
    string_data += f"\n{FileSections.MOUSE_DATA}\n"
    for line in mouse_data.splitlines(True):
        string_data += "\t" + line

    return string_data

def _get_chunk_controller_data(chunk_controller: ScreenChunkController, ignore_empty_chunks: bool = True) -> str:
    stringified = ""

    header = f"{",".join(CHUNK_CONTROLLER_EXTRA_HEADERS)},{generate_header(ScreenChunk)}"
    stringified += f"ChunkDataHeader: {header}"

    chunk_strings: list = []
    for row in chunk_controller.chunks:
        for chunk in row:
            if not chunk.has_data() and ignore_empty_chunks:
                continue
            
            chunk_idx = chunk_controller.posToIdx(chunk.position)
            
            chunk_data = ""
            for line in _get_chunk_data(chunk, chunk_controller).splitlines(True): chunk_data += "\t" + line # type: ignore
            
            chunk_strings.append(
                [chunk_idx, 
                f"\n[{FileSections.CHUNK_DATA}]\n{chunk_data}"]
            )
    chunk_strings.sort(key=ScreenChunkController.sort_chunk_strings)
    for str_list in chunk_strings:
        stringified += str_list[1]

    return stringified

def _get_chunk_data(chunk: ScreenChunk, chunk_controller: ScreenChunkController) -> str:
    string_data: str = ""
    string_data += f"{chunk.position.x},{chunk.position.y}," + generate_csv_line(chunk)
    
    key_manager_data: str = ""
    for line in _get_key_manager_data(chunk.key_manager, False).splitlines(True):
        key_manager_data += "\t" + line
    string_data += f"\n<ChunkKeyData>\n{key_manager_data}"

    return string_data

def _get_peripheral_controller_data(controller: PeripheralController, ignore_empty_chunks: bool = True) -> str:
    string_data: str = ""
    string_data += f"\nRuntimeInMs: {int(round((time.time() - controller.start_listen_time) * 1000))}"
    
    key_manager_data: str = ""
    for line in _get_key_manager_data(controller.key_data_manager, False).splitlines(True):
        key_manager_data += "\t" + line
    string_data += f"\n{FileSections.GENERAL_KEYBOARD_DATA}\n{key_manager_data}"
    
    chunk_data = ""
    for line in _get_chunk_controller_data(controller.chunk_controller, ignore_empty_chunks).splitlines(True): 
        chunk_data += "\t" + line
    
    string_data += f"\n{FileSections.ALL_CHUNK_DATA}\n{chunk_data}"

    return string_data

# Final methods

def get_hmp_file_content(controller: PeripheralController, ignore_empty_chunks: bool = True) -> str:
    file_content: str = f"{FORMAT_VERSION}\nChunkSize: {controller.chunk_controller.chunk_size}"
    file_content += _get_peripheral_controller_data(controller, ignore_empty_chunks)
    file_content += "\n[END]"

    return file_content

def save_hmp_file(controller: PeripheralController, file_path: str, ignore_empty_chunks: bool = True):
    start_time = time.time_ns()
    with open(os.path.join(file_path, ((str) (datetime.strftime(datetime.now(),"%d-%m-%Y_%H-%M-%S") + FILE_EXTENSION))), "w+") as file:
        file.write(get_hmp_file_content(controller, ignore_empty_chunks))
        print(f"INFO: Took {(time.time_ns() - start_time) * 10 ** -6}ms to save file")

def load_hmp_file(file_path: str) -> PeripheralController: # type: ignore
    file_content: list[str] = []
    with open(file_path, "r") as file:
        file_content = file.readlines()

    start_time = time.time_ns()

    content_str: str = "".join(file_content)
    matches = regex.findall(f"(?:{FileSections.CHUNK_DATA}.*?\\])(.*?\\[)", content_str, regex.S)
    for match in matches:
        chunk = _parse_chunk_data_section(match)
        print(match)
    
    print(f"Took {(time.time_ns() - start_time) * 10 ** -6}ms to look at all file lines")

# Section Parsing methods:

def _parse_chunk_data_section(section_str: str) -> ScreenChunk:
    section_lines = section_str.split("\n")

    chunk_properties_csv: str = section_lines.pop(1).replace("\t", "")
    key_data_match = regex.search(f"(?:<{FileSections.CHUNK_KEY_DATA}>)(.*)", section_str)
    key_manager: KeyDataManager
    if key_data_match != None:
        key_manager: KeyDataManager = _parse_key_manager_section(key_data_match.group(0))
    else:
        key_manager = KeyDataManager()
        print(f"ERROR: Couldn't read {FileSections.CHUNK_KEY_DATA} Section | chunk_properties: {chunk_properties_csv}")

    new_chunk: ScreenChunk = ScreenChunk(Vector2i(-1, -1))
    new_chunk.key_manager = key_manager
    set_obj_properties(new_chunk, chunk_properties_csv)
    value_dict = get_csv_as_dict(chunk_properties_csv, ",".join(CHUNK_CONTROLLER_EXTRA_HEADERS))
    chunk_pos = Vector2i(
        value_dict[CHUNK_CONTROLLER_EXTRA_HEADERS[0]],
        value_dict[CHUNK_CONTROLLER_EXTRA_HEADERS[1]]
    )
    new_chunk.position = chunk_pos

    return new_chunk

def _parse_key_manager_section(section_str: str):
    pattern = f"(?:<{FileSections.KEYBOARD_DATA}>)(.*)?<"
    keyboard_match = regex.search(pattern, section_str)
    keyboard_csv: str = ""
    if keyboard_match != None:
        keyboard_csv = keyboard_match.group(0)

    pattern = f"(?:<{FileSections.MOUSE_DATA}>)(.*)?<"
    mouse_match = regex.search(pattern, section_str)
    mouse_csv: str = ""
    if mouse_match != None:
        mouse_csv = mouse_match.group(0)

    key_manager: KeyDataManager = KeyDataManager()
    for line in keyboard_csv.splitlines():
        keyboard_key_stats: KeyboardKeyStats = KeyboardKeyStats("")
        set_obj_properties(keyboard_key_stats, line)
        key_manager.register_key(keyboard_key_stats)

    for line in mouse_csv.splitlines():
        mouse_button_stats: MouseButtonStats = MouseButtonStats("")
        set_obj_properties(mouse_button_stats, line)
        key_manager.register_key(mouse_button_stats)

    return key_manager

# General Utility functions:

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
        value_dict[key] = values[idx]
    
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
        if is_valid_int(value):
            value = int(value)
        elif is_valid_float(value):
            value = float(value)

        obj.__setattr__(key, value)

    return value_dict


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