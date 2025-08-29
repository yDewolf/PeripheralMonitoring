from datetime import datetime
import os
import time
from Listeners.data.KeyDataManager import KeyDataManager
from Listeners.data.KeyboardKeyStats import KeyboardKeyStats
from Listeners.data import MouseButtonStats
from Controllers.PeripheralController import PeripheralController
from utils.Chunk.ScreenChunkController import ScreenChunkController
from utils.Chunk.ScreenChunk import ScreenChunk

FORMAT_VERSION: int = 3
FILE_EXTENSION: str = ".hmp"
indexed_headers: dict = {}
indexed_property_names: dict = {}


def _get_key_manager_data(key_manager: KeyDataManager, with_headers: bool = True) -> str:
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
            
            chunk_data = _get_chunk_data(chunk, chunk_controller) # type: ignore
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
    string_data += f"{chunk_controller.posToIdx(chunk.position)}" + generate_csv_line(chunk)
    string_data += f"\n[ChunkKeyData]\n{_get_key_manager_data(chunk.key_manager, False)}"

    return string_data

def _get_peripheral_controller_data(controller: PeripheralController, ignore_empty_chunks: bool = True) -> str:
    string_data: str = ""
    string_data += f"\nRuntimeInMs: {int(round((time.time() - controller.start_listen_time) * 1000))}"
    string_data += "\n[GeneralKeyData]\n" + _get_key_manager_data(controller.key_data_manager, True)
    string_data += "\n[AllChunkData]\n" + _get_chunk_controller_data(controller.chunk_controller, ignore_empty_chunks)

    return string_data

def get_hmp_file_content(controller: PeripheralController, ignore_empty_chunks: bool = True) -> str:
    file_content: str = f"{FORMAT_VERSION}"
    file_content += _get_peripheral_controller_data(controller, ignore_empty_chunks)

    return file_content

def save_hmp_file(controller: PeripheralController, file_path: str, ignore_empty_chunks: bool = True):
    start_time = time.time_ns()
    with open(os.path.join(file_path, ((str) (datetime.strftime(datetime.now(),"%d-%m-%Y_%H-%M-%S") + FILE_EXTENSION))), "w+") as file:
        file.write(get_hmp_file_content(controller, ignore_empty_chunks))
        print(f"INFO: Took {(time.time_ns() - start_time) * 10 ** -6}ms to save file")


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
    
    keys = get_property_names(instance_type) # type: ignore
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