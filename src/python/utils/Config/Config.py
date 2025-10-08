from utils import CfgUtils
from utils import FileUtils

class ConfigData:
    ChunkSize: int = 16
    IdleToAfkThreshold: int = 5000
    Port: int = 5000

    DebugMode: bool = False
    FastStart: bool = True

    RelativePath: bool = True
    SavePath: str = "saves"

    IgnoreEmptyChunks: bool = True

    def __init__(self, file_path: str = "", create_file: bool = False) -> None:
        if file_path == "":
            return
                
        if create_file:
            print(f"Creating config file at {file_path}")
            self.save_to_file(file_path)
            return
        
        self.load_from_file(file_path)    
    
    def save_to_file(self, file_path: str = ""):
        data = {}
        properties = FileUtils.get_property_names(ConfigData)
        for property in properties:
            data[property] = self.__getattribute__(property)

        CfgUtils.save_configs(data, file_path)
    
    def load_from_file(self, file_path: str = ""):
        data = CfgUtils.load_configs(file_path)
        for key in data.keys():
            if not self.__getattribute__(key):
                continue
                
            self.__setattr__(key, data[key])