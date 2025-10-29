from utils import CfgUtils
from utils import FileUtils

class ConfigData:
    _path: str

    ChunkSize: int = 16
    IdleToAfkThreshold: int = 5000
    Port: int = 5000
    ActiveMonitors: list[int] = []

    DebugMode: bool = False
    FastStart: bool = True

    RelativePath: bool = True
    SavePath: str = "saves"

    IgnoreEmptyChunks: bool = True

    def __init__(self, file_path: str = "", save_path: str = "saves", create_file: bool = False) -> None:
        self.SavePath = save_path
        self._path = file_path
        if self.SavePath.__contains__("\\"):
            self.RelativePath = False

        if file_path == "":
            return
                
        if create_file:
            print(f"Creating config file at {file_path}")
            self.save_to_file(file_path)
            return
        
        self.load_from_file(file_path)    
    
    def to_dict(self) -> dict:
        data: dict = {}
        for attribute in ConfigData.__dict__:
            if attribute.startswith("_"):
                continue

            value = self.__getattribute__(attribute)
            if callable(value):
                continue

            data[attribute] = value

        return data

    def read_dict(self, data: dict, save: bool = False):
        for key in data.keys():
            if not hasattr(self, key):
                continue
            
            self.__setattr__(key, data[key])
        
        if save:
            self.save_to_file(self._path)


    def save_to_file(self, file_path: str = ""):
        data = {}
        properties = FileUtils.get_property_names(ConfigData)
        for property in properties:
            data[property] = self.__getattribute__(property)

        CfgUtils.save_configs(data, file_path)
    
    def load_from_file(self, file_path: str = ""):
        self._path = file_path
        data = CfgUtils.load_configs(file_path)

        self.read_dict(data, False)
    