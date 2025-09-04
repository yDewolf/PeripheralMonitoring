from datetime import datetime
import os
import time
from Listeners.data.BaseKeyStats import BaseKeyStats
import utils.FileUtils as FileUtils
import re as regex
from Listeners.data.KeyDataManager import KeyDataManager
from Listeners.data.KeyboardKeyStats import KeyboardKeyStats
from Listeners.data.MouseButtonStats import MouseButtonStats
from Controllers.PeripheralController import PeripheralController
from Enums.HMPFile import FileSections, FileVariables
from utils.Chunk.Chunk import Vector2i
from utils.Chunk.ScreenChunkController import ScreenChunkController
from utils.Chunk.ScreenChunk import ScreenChunk

FORMAT_VERSION: int = 6
FILE_EXTENSION: str = ".hmp"
CHUNK_CONTROLLER_EXTRA_HEADERS: list[str] = ["PosX", "PosY"]

# Data getters for PeripheralController related classes

def _get_key_manager_data(key_manager: KeyDataManager, with_headers: bool = True) -> str:
    string_data: str = ""
    if not key_manager.has_data():
        return string_data

    keyboard_data: str = ""
    mouse_data: str = ""
    if with_headers:
        
        keyboard_data += FileUtils.generate_header(KeyboardKeyStats)
        mouse_data += FileUtils.generate_header(MouseButtonStats)
    
    sorted_list = sorted(key_manager.key_list, key=KeyDataManager.sort_keys) # type: ignore
    most_pressed: BaseKeyStats | None = None
    for key in sorted_list:
        key_csv = FileUtils.generate_csv_line(key)
        if most_pressed == None:
            most_pressed = key

        if key.times_pressed > most_pressed.times_pressed:
            most_pressed = key

        if type(key) is KeyboardKeyStats:
            if keyboard_data == "":
                keyboard_data += key_csv
                continue
            
            keyboard_data += "\n" + key_csv
            continue
        
        if type(key) is MouseButtonStats:
            if mouse_data == "":
                mouse_data += key_csv
                continue
            
            mouse_data += "\n" + key_csv
            continue
    
    if with_headers and most_pressed != None:
        string_data += f"{get_variable_string(FileVariables.MOST_PRESSED_KEY.value, most_pressed.related_key_name)}\n"
    
    string_data += f"{FileSections.KEYBOARD_DATA.value}\n"
    for line in keyboard_data.splitlines(True):
        string_data += "\t" + line
    
    string_data += f"\n{FileSections.MOUSE_DATA.value}\n"
    for line in mouse_data.splitlines(True):
        string_data += "\t" + line

    return string_data

def _get_chunk_controller_data(chunk_controller: ScreenChunkController, ignore_empty_chunks: bool = True) -> str:
    stringified = ""

    header = f"{",".join(CHUNK_CONTROLLER_EXTRA_HEADERS)},{FileUtils.generate_header(ScreenChunk)}"
    stringified += get_variable_string(FileVariables.CHUNK_DATA_HEADER.value, header)

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
                f"\n[{FileSections.CHUNK_DATA.value}{chunk_controller.posToIdx(chunk.position)}]\n{chunk_data}"]
            )
    
    chunk_strings.sort(key=ScreenChunkController.sort_chunk_strings)
    for str_list in chunk_strings:
        stringified += str_list[1]

    return stringified

def _get_chunk_data(chunk: ScreenChunk, chunk_controller: ScreenChunkController) -> str:
    string_data: str = ""
    string_data += f"{chunk.position.x},{chunk.position.y}," + FileUtils.generate_csv_line(chunk)
    
    key_manager_data: str = ""
    for line in _get_key_manager_data(chunk.key_manager, False).splitlines(True):
        key_manager_data += "\t" + line
    
    string_data += f"\n{FileSections.CHUNK_KEY_DATA.value}\n{key_manager_data}"

    return string_data

def _get_peripheral_controller_data(controller: PeripheralController, ignore_empty_chunks: bool = True) -> str:
    string_data: str = ""
    string_data += f"\n{get_variable_string(FileVariables.RUNTIME_MS.value,int(round((time.time() - controller.start_listen_time) * 1000)))}"
    
    key_manager_data: str = ""
    for line in _get_key_manager_data(controller.key_data_manager, True).splitlines(True):
        key_manager_data += "\t" + line
    
    string_data += f"\n{FileSections.GENERAL_KEYBOARD_DATA.value}\n{key_manager_data}"
    
    chunk_data = ""
    for line in _get_chunk_controller_data(controller.chunk_controller, ignore_empty_chunks).splitlines(True): 
        chunk_data += "\t" + line
    
    string_data += f"\n{FileSections.ALL_CHUNK_DATA.value}\n{chunk_data}"

    return string_data

# Final methods

def get_hmp_file_content(controller: PeripheralController, ignore_empty_chunks: bool = True) -> str:
    file_content: str = f"{FORMAT_VERSION}"
    file_content += "\n" + get_variable_string(FileVariables.CHUNK_SIZE.value, controller.chunk_controller.chunk_size)
    file_content += "\n" + get_variable_string(FileVariables.IDLE_TO_AFK_THRESHOLD.value, controller.mouse_parser.idle_to_afk_threshold)
    file_content += "\n" + get_variable_string(FileVariables.TAGS.value, ",".join(controller.tags))
    
    file_content += _get_peripheral_controller_data(controller, ignore_empty_chunks)
    file_content += "\n[END]"

    return file_content

def save_hmp_file(controller: PeripheralController, file_path: str, ignore_empty_chunks: bool = True):
    start_time = time.time_ns()
    with open(os.path.join(file_path, ((str) (datetime.strftime(datetime.now(),"%d-%m-%Y_%H-%M-%S") + FILE_EXTENSION))), "w+") as file:
        file.write(get_hmp_file_content(controller, ignore_empty_chunks))
        print(f"INFO: Took {(time.time_ns() - start_time) * 10 ** -6}ms to save file")

def load_hmp_file(file_path: str) -> PeripheralController: # type: ignore
    start_time = time.time_ns()
    
    file_content: list[str] = []
    with open(file_path, "r") as file:
        file_content = file.readlines()

    content_str: str = "".join(file_content)
    variables_match: list[str] = regex.findall("(.*)?:(.*)", content_str)
    
    variables: dict = {}
    for key_value_tup in variables_match:
        key, value = key_value_tup
        variables[FileUtils.clean_string(key)] = FileUtils.parse_value(value)

    # chunk_controller: ScreenChunkController = ScreenChunkController()
    chunk_data_match = regex.search(f"{FileSections.ALL_CHUNK_DATA.value}(.*)", content_str, regex.S)
    chunk_data_section: str = ""
    if chunk_data_match != None:
        chunk_data_section = chunk_data_match.group()

    chunk_index, loaded_chunks = _parse_all_chunk_data(chunk_data_section, variables)

    key_data_match = regex.search(f"{FileSections.GENERAL_KEYBOARD_DATA.value}(.*)?(?:{FileSections.ALL_CHUNK_DATA.value})", content_str, regex.S)
    key_data_section: str = ""
    if key_data_match != None:
        key_data_section = key_data_match.group()

    key_manager = _parse_key_manager_section(key_data_section)
    chunk_controller: ScreenChunkController = ScreenChunkController(variables.get(FileVariables.CHUNK_SIZE.value, -1), chunk_index)
    peripheral_controller = PeripheralController(
        chunk_controller, 
        key_manager,
        tags=variables.get(FileVariables.TAGS.value, []),
        idle_to_afk_threshold=variables.get(FileVariables.IDLE_TO_AFK_THRESHOLD.value, 5000)
    )

    print(f"Took {(time.time_ns() - start_time) * 10 ** -6}ms to parse file")
    
    return peripheral_controller

# Section Parsing methods:

def _parse_all_chunk_data(section_str: str, variables: dict) -> tuple[dict[str, ScreenChunk], list[ScreenChunk]]:
    matches = regex.findall(f"(?:{FileSections.CHUNK_DATA.value}.*?\\])(.*?\\[)", section_str, regex.S)
    
    loaded_chunks: list[ScreenChunk] = []
    chunk_index: dict = {}
    for match in matches:
        chunk = _parse_chunk_data_section(match, variables[FileVariables.CHUNK_DATA_HEADER.value])
        loaded_chunks.append(chunk)
        chunk_index[str(chunk.position)] = chunk
    
    return chunk_index, loaded_chunks

def _parse_chunk_data_section(section_str: str, chunk_data_header: str) -> ScreenChunk:
    section_lines = section_str.split("\n")

    chunk_properties_csv: str = section_lines.pop(1).replace("\t", "")
    key_data_match = regex.search(f"(?:{FileSections.CHUNK_KEY_DATA.value})(.*)", section_str, regex.S)
    key_manager: KeyDataManager = KeyDataManager() 

    # Fix this
    if key_data_match != None:
        if key_data_match.group(1) != "":
            key_manager: KeyDataManager = _parse_key_manager_section(key_data_match.group(1))
        # print(f"ERROR: Couldn't read {FileSections.CHUNK_KEY_DATA.value} Section | chunk_properties: {chunk_properties_csv}")

    new_chunk: ScreenChunk = ScreenChunk(Vector2i(-1, -1))
    new_chunk.key_manager = key_manager
    FileUtils.set_obj_properties(new_chunk, chunk_properties_csv, chunk_data_header)
    value_dict = FileUtils.get_csv_as_dict(chunk_properties_csv, chunk_data_header)
    chunk_pos = Vector2i(
        value_dict[CHUNK_CONTROLLER_EXTRA_HEADERS[0]],
        value_dict[CHUNK_CONTROLLER_EXTRA_HEADERS[1]]
    )
    new_chunk.position = chunk_pos

    return new_chunk

def _parse_key_manager_section(section_str: str):
    pattern = f"(?:{FileSections.KEYBOARD_DATA.value})(.*)?(?:{FileSections.MOUSE_DATA.value})"
    keyboard_match = regex.search(pattern, section_str, regex.S)
    keyboard_csv: str = ""
    if keyboard_match != None:
        keyboard_csv = keyboard_match.group(1)

    pattern = f"(?:{FileSections.MOUSE_DATA.value})(.*)?<"
    mouse_match = regex.search(pattern, section_str, regex.S)
    mouse_csv: str = ""
    if mouse_match != None:
        mouse_csv = mouse_match.group(1)

    key_manager: KeyDataManager = KeyDataManager()
    for idx, line in enumerate(keyboard_csv.splitlines()):
        # Skip the header
        if idx == 1:
            continue

        line = FileUtils.clean_string(line)
        if line == "":
            continue

        keyboard_key_stats: KeyboardKeyStats = KeyboardKeyStats("")
        FileUtils.set_obj_properties(keyboard_key_stats, line)

        key_manager.register_key(keyboard_key_stats)

    for idx, line in enumerate(mouse_csv.splitlines()):
        # Skip the header
        if idx == 1:
            continue

        line = FileUtils.clean_string(line)
        if line == "":
            continue
        
        mouse_button_stats: MouseButtonStats = MouseButtonStats("")
        FileUtils.set_obj_properties(mouse_button_stats, line)

        key_manager.register_key(mouse_button_stats)

    return key_manager

# General Utility functions:

def get_variable_string(variable_name: str, value) -> str:
    return f"{variable_name}: {value};"