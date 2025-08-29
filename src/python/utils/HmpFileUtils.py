from datetime import datetime
import os
import time
from Listeners.data.KeyDataManager import KeyDataManager
from Listeners.data.KeyboardKeyStats import KeyboardKeyStats
from Listeners.data import MouseButtonStats
from Controllers.PeripheralController import PeripheralController
from utils.Chunk.ScreenChunkController import ScreenChunkController
from utils.Chunk.ScreenChunk import ScreenChunk

FORMAT_VERSION: int = 4
FILE_EXTENSION: str = ".hmp"
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
    
    string_data += "[KeyboardData]\n"
    for line in keyboard_data.splitlines(True):
        string_data += "\t" + line
    
    string_data += "\n[MouseData]\n"
    for line in mouse_data.splitlines(True):
        string_data += "\t" + line

    return string_data

def _get_chunk_controller_data(chunk_controller: ScreenChunkController, ignore_empty_chunks: bool = True) -> str:
    stringified = ""

    header = f"ChunkIdx,{generate_header(ScreenChunk)}"
    stringified += f"ChunkDataHeader: {header}"

    chunk_strings: list = []
    for row in chunk_controller.chunks:
        for chunk in row:
            if not chunk.has_data() and ignore_empty_chunks:
                continue
            
            chunk_idx = chunk_controller.posToIdx(chunk.position)
            
            chunk_data = ""
            for line in _get_chunk_data(chunk, chunk_controller).splitlines(True): chunk_data += "\t" + line
            
            chunk_strings.append(
                [chunk_idx, 
                f"\n[CHUNK_DATA_{chunk_idx}]\n{chunk_data}"]
            )
    chunk_strings.sort(key=ScreenChunkController.sort_chunk_strings)
    for str_list in chunk_strings:
        stringified += str_list[1]

    return stringified

def _get_chunk_data(chunk: ScreenChunk, chunk_controller: ScreenChunkController) -> str:
    string_data: str = ""
    string_data += f"{chunk_controller.posToIdx(chunk.position)}," + generate_csv_line(chunk)
    
    key_manager_data: str = ""
    for line in _get_key_manager_data(chunk.key_manager, False).splitlines(True):
        key_manager_data += "\t" + line
    string_data += f"\n[ChunkKeyData]\n{key_manager_data}"

    return string_data

def _get_peripheral_controller_data(controller: PeripheralController, ignore_empty_chunks: bool = True) -> str:
    string_data: str = ""
    string_data += f"\nRuntimeInMs: {int(round((time.time() - controller.start_listen_time) * 1000))}"
    
    key_manager_data: str = ""
    for line in _get_key_manager_data(controller.key_data_manager, False).splitlines(True):
        key_manager_data += "\t" + line
    string_data += f"\n[GeneralKeyData]\n{key_manager_data}"
    
    chunk_data = ""
    for line in _get_chunk_controller_data(controller.chunk_controller, ignore_empty_chunks).splitlines(True): 
        chunk_data += "\t" + line
    
    string_data += f"\n[AllChunkData]\n{chunk_data}"

    return string_data

# Final methods

def get_hmp_file_content(controller: PeripheralController, ignore_empty_chunks: bool = True) -> str:
    file_content: str = f"{FORMAT_VERSION}\nChunkSize: {controller.chunk_controller.chunk_size}"
    file_content += _get_peripheral_controller_data(controller, ignore_empty_chunks)

    return file_content

def save_hmp_file(controller: PeripheralController, file_path: str, ignore_empty_chunks: bool = True):
    start_time = time.time_ns()
    with open(os.path.join(file_path, ((str) (datetime.strftime(datetime.now(),"%d-%m-%Y_%H-%M-%S") + FILE_EXTENSION))), "w+") as file:
        file.write(get_hmp_file_content(controller, ignore_empty_chunks))
        print(f"INFO: Took {(time.time_ns() - start_time) * 10 ** -6}ms to save file")

def load_hmp_file(file_path: str) -> PeripheralController:
    file_content: list[str] = []
    with open(file_path, "r") as file:
        file_content = file.readlines()

    # chunk_controller: ScreenChunkController = ScreenChunkController()
    # current_chunk: ScreenChunk
    
    # controller: PeripheralController = PeripheralController(chunk_controller, debug_mode=False)
    section_tree: list[str] = []
    tabs: list[int] = []
    
    for line in file_content:
        formatted_line = line.strip("\t")
        if formatted_line.startswith("["):
           tab_amount = line.count("\t")
           if len(tabs) > 0:
                if tabs[-1] >= tab_amount:
                    section_tree.pop(-1)
                    tabs.pop(-1)
               
           section_tree.append(line)
           tabs.append(tab_amount)
           print(f"Tree: {section_tree}\nTabs: {tabs}")
           continue
        
    
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

def set_obj_properties(obj: object, csv_line: str, header: str = ""):
    if header == "":
        header = generate_header(obj)
        
    properties = header.split(",")
    values = csv_line.split(",")
    for idx, property_name in enumerate(properties):
        obj.__setattr__(property_name, values[idx])