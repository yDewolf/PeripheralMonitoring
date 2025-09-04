import os
from Controllers.PeripheralController import PeripheralController
# from api.FlaskAPI import FlaskAPI
from utils import FileUtils, HmpPlotUtils
from utils.Menu.ConsoleUtils import ConsoleInputHandler
from utils.Chunk.ScreenChunk import ScreenChunk
from utils.Chunk.ScreenChunkController import ScreenChunkController
from Listeners.GeneralListener import GeneralListener

import utils.HmpFileUtils as HMPUtils
import utils.CfgUtils as CfgUtils

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "./config.cfg")
config_data = CfgUtils.load_configs(CONFIG_PATH)

SAVE_PATH: str = str(config_data["SavePath"])
if bool(config_data["RelativePath"]):
    SAVE_PATH = os.path.join(os.path.dirname(__file__), SAVE_PATH)

print('\x1b[3;37;44m' + "".center(30) + '\x1b[0m')
print('\x1b[3;37;44m' + "Peripheral Monitor".center(30) + '\x1b[0m')
print('\x1b[3;37;44m' + "".center(30) + '\x1b[0m')

chunk_controller = ScreenChunkController(int(config_data["ChunkSize"]))
controller: PeripheralController = PeripheralController(
    chunk_controller, 
    debug_mode=bool(config_data["DebugMode"]),
    idle_to_afk_threshold=int(config_data["IdleToAfkThreshold"])
)

listener = GeneralListener(controller)
if bool(config_data["FastStart"]):
    listener.start()

def statistics_menu():
    keep_on_menu: bool = True
    while keep_on_menu:
        data_type: int = ConsoleInputHandler.selectFromOptions("What type of data are you looking for?", ["Mouse Data", "Key Data"] + ["Quit"])

        match data_type:
            case 0:
                break

            case 1:
                valid_properties: list[str] = FileUtils.get_property_names(ScreenChunk)
                property_idx: int = ConsoleInputHandler.selectFromOptions(
                    "Select one of the options below: ", valid_properties
                )

                property_name = valid_properties[property_idx - 1]
                img = HmpPlotUtils.create_chunk_property_img(controller, property_name)

            case 2:
                selected_key_name: str = input("Type the key name you want to analyze\n>> ")
                img = HmpPlotUtils.create_chunk_key_data_img(controller, selected_key_name)


        HmpPlotUtils.pyplot.show()

def load_menu():
    file_path: str = input("Please input a file path\n>> ")

    return HMPUtils.load_hmp_file(file_path)

looping: bool = True
saved_file: bool = False
while looping:
    opt = ConsoleInputHandler.selectFromOptions("Menu", ["Save HMP File", "See statistics", "Start Listener", "Load HMP file", "Quit"])
    match opt:
        case 0:
            if not saved_file:
                looping = not ConsoleInputHandler.confirmChoice("Are you sure you want to quit? (You didn't save the file)")
            
            else:
                looping = False
                break

        case 1:
            HMPUtils.save_hmp_file(controller, SAVE_PATH, ignore_empty_chunks=bool(config_data["IgnoreEmptyChunks"]))
            saved_file = True

        case 2:
            statistics_menu()
        
        case 3:
            listener.start()
            saved_file = False

        case 4:
            controller = load_menu()
