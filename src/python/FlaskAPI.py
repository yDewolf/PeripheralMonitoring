import sys
import os
import signal
import time
from threading import Thread
import flask
from flask import Flask, Response, request
from flask_cors import CORS
from enum import Enum

from Controllers.PeripheralController import PeripheralController
from Listeners.GeneralListener import GeneralListener
from utils.Config.Config import ConfigData
from utils import HmpUtils
from utils import HmpFileUtils
from utils.Chunk.ScreenChunkController import ScreenChunkController

class APIStatus(Enum):
    DOWN = 0
    SETTING_UP = 1
    READY = 2
    LISTENING = 3
    FINISHING = 4

class FlaskAPI(Flask):
    config_data: ConfigData
    controller: PeripheralController
    listener: GeneralListener

    status: APIStatus = APIStatus.DOWN

    def __init__(self, import_name: str, config_data: ConfigData, static_url_path: str | None = None, static_folder: str | os.PathLike[str] | None = "static", static_host: str | None = None, host_matching: bool = False, subdomain_matching: bool = False, template_folder: str | os.PathLike[str] | None = "templates", instance_path: str | None = None, instance_relative_config: bool = False, root_path: str | None = None):
        super().__init__(import_name, static_url_path, static_folder, static_host, host_matching, subdomain_matching, template_folder, instance_path, instance_relative_config, root_path)
        self.config_data = config_data
        
        self.add_url_rule("/", view_func=self.index)
        self.add_url_rule("/shutdown/<save_before_shutting_down>", view_func=self.shutdown, methods=["POST"])
        self.add_url_rule("/restart", view_func=self.restart, methods=["POST"])
        self.add_url_rule("/listen", view_func=self.listen, methods=["POST"])
        self.add_url_rule("/stop-listening", view_func=self.stop_listening, methods=["POST"])
        self.add_url_rule("/get-data/<property>", view_func=self.get_data)
        self.add_url_rule("/save-file-data/", view_func=self.save_file_data, methods=["POST"])
        self.add_url_rule("/get-config/", view_func=self.get_config)
        self.add_url_rule("/update-config/", view_func=self.update_configs, methods=["POST"])
        self.setup_controller()
        
        self.teardown_request(self.terminate_process)

        print("API Setup Successfully")

    def shutdown(self, save_before_shutting_down: bool = True):
        if self.listener.running:
            if self.config_data.DebugMode:
                print("Stopping Listener... ")
            self.listener.stop()
            
            if self.config_data.DebugMode:
                print("Listener Stopped.")

        message: str = "Shut down the API"
        
        if save_before_shutting_down:
            # Prevent it from trying to save without even having data
            try:
                # start_time = self.controller.start_listen_time
            
                HmpFileUtils.save_hmp_file(self.controller, self.config_data.SavePath)
                message += f" | Saved file to {self.config_data.SavePath}"
                print(f"Saved HMP to {self.config_data.SavePath}")
            
            except AttributeError:
                print("Controller has no data...")

        self.status = APIStatus.FINISHING
        return self.generate_response(message)

    def terminate_process(self, exception):
        if self.status == APIStatus.FINISHING:
            print("Killing API proccess")
            kill_thread = Thread(target=self.kill_function)
            kill_thread.start()
    
    def kill_function(self):
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGINT)


    def index(self):
        return self.generate_response("Waiting...")

    def restart(self):
        self.status = APIStatus.SETTING_UP
        if self.listener.running:
            self.listener.stop()

        try:
            HmpFileUtils.save_hmp_file(self.controller, self.config_data.SavePath)
        except:
            pass

        self.setup_controller()
        return self.generate_response("Restarted Successfully")

    def setup_controller(self):
        self.status = APIStatus.SETTING_UP

        SAVE_PATH: str = str(self.config_data.SavePath)
        if bool(self.config_data.RelativePath):
            SAVE_PATH = os.path.join(os.path.dirname(__file__), SAVE_PATH)

        chunk_controller: ScreenChunkController = ScreenChunkController(
            int(self.config_data.ChunkSize),
            target_monitor=int(self.config_data.ActiveMonitors)
        )
        self.controller = PeripheralController(
            chunk_controller,
            debug_mode=bool(config_data.DebugMode),
            idle_to_afk_threshold=int(config_data.IdleToAfkThreshold)
        )
        self.listener = GeneralListener(self.controller)

        self.status = APIStatus.READY


    def listen(self):
        listener_thread = Thread(target=self.listener.start)
        listener_thread.start()
        
        self.status = APIStatus.LISTENING
        return self.generate_response("Listening to inputs...")

    def stop_listening(self):
        self.listener.stop()
        self.status = APIStatus.READY
        body_data = {
            "chunk_data": HmpUtils.chunk_data_to_dict(self.controller),
            "grid_size": [self.controller.chunk_controller.grid_size.x, self.controller.chunk_controller.grid_size.y], 
            "chunk_size": self.controller.chunk_controller.chunk_size, 
        }
        return self.generate_response("Stopped listening to inputs", body_data)

    def get_data(self, property: str = "times_hovered"):
        body_data = {
            "chunk_data": HmpUtils.chunk_data_to_dict(self.controller, property),
            "grid_size": [self.controller.chunk_controller.grid_size.x, self.controller.chunk_controller.grid_size.y], 
            "chunk_size": self.controller.chunk_controller.chunk_size, 
        }
        return self.generate_response("Fetched Data", body=body_data)

    def save_file_data(self):
        request_data: dict = request.get_json()
        file_path = request_data.get("file_path", self.config_data.SavePath)
        
        # Prevent it from trying to save without even having data
        try:
            # start_time = self.controller.start_listen_time
            HmpFileUtils.save_hmp_file(self.controller, file_path)
            print("Saved file to ", file_path)
            return self.generate_response(f"Saved HMP file to {file_path}")
            
        except AttributeError:
            pass
        
        finally:
            return self.generate_response(f"Didn't have any data to save")

    def get_config(self):
        return self.generate_response(f"Config file path:", {"path": self.config_data._path, "config": self.config_data.to_dict()})

    def update_configs(self):
        data: dict = request.get_json()
        self.config_data.read_dict(data.get("config_data", {}), True)

        return self.generate_response("Updated config successfully!", {"new_config": self.config_data.to_dict()})


    def generate_response(self, message: str, body: dict = {}) -> Response:
        data = {
            "message": message,
            "status": self.status.value
        }
        if body != {}:
            data["body"] = body
        response = flask.jsonify(data)
        
        response.headers['Access-Control-Allow-Origin'] = '*' 
        response.headers['Content-Type'] = 'application/json'

        return response

DEFAULT_CFG_PATH: str = "./config.cfg"
DEFAULT_SAVE_PATH: str = ConfigData.SavePath

cfg_path: str = DEFAULT_CFG_PATH
save_path: str = DEFAULT_SAVE_PATH

previous_argument: str = ""
for idx, argument in enumerate(sys.argv):
    if idx == 0:
        continue
    
    match previous_argument:
        case "--save":
            print("Parsing save path")
            save_path = argument.removeprefix("'").removesuffix("'")
            save_path = save_path.removeprefix("\\\\\\\\?\\\\")

        case "--config":
            print("Parsing config path")
            cfg_path = argument.removeprefix("'").removesuffix("'")
            cfg_path = cfg_path.removeprefix("\\\\\\\\?\\\\")

    previous_argument = argument


config_data: ConfigData = ConfigData(cfg_path, save_path, not os.path.exists(cfg_path))
config_data.to_dict()
if config_data.SavePath != save_path:
    config_data.SavePath = save_path

# print(cfg_path, save_path)
if not os.path.isdir(str(config_data.SavePath)):
    os.mkdir(str(config_data.SavePath))

print(f"API Version: 0.2")
api = FlaskAPI(__name__, config_data)
CORS(api)
api.run(port=config_data.Port)

print("Finished API Process")