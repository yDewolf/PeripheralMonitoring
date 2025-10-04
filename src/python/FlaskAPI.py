
import os
from threading import Thread
import flask
from flask import Flask, request
from enum import Enum

from Controllers.PeripheralController import PeripheralController
from Listeners.GeneralListener import GeneralListener
from utils import CfgUtils
from utils import HmpPlotUtils
from utils.Chunk.ScreenChunkController import ScreenChunkController
import utils.HmpFileUtils as HmpFileUtils

class APIStatus(Enum):
    DOWN = 0
    SETTING_UP = 1
    READY = 2
    LISTENING = 3

class FlaskAPI(Flask):
    DEFAULT_SAVE_PATH: str = os.path.join(os.path.dirname(__file__), "../../saves")
    controller: PeripheralController
    listener: GeneralListener

    status: APIStatus = APIStatus.DOWN

    def __init__(self, import_name: str, static_url_path: str | None = None, static_folder: str | os.PathLike[str] | None = "static", static_host: str | None = None, host_matching: bool = False, subdomain_matching: bool = False, template_folder: str | os.PathLike[str] | None = "templates", instance_path: str | None = None, instance_relative_config: bool = False, root_path: str | None = None):
        super().__init__(import_name, static_url_path, static_folder, static_host, host_matching, subdomain_matching, template_folder, instance_path, instance_relative_config, root_path)
        self.add_url_rule("/", view_func=self.index)
        self.add_url_rule("/listen", view_func=self.listen)
        self.add_url_rule("/stop-listening", view_func=self.stop_listening)
        self.add_url_rule("/get-data/<property>", view_func=self.get_data)
        self.add_url_rule("/save-file-data", view_func=self.save_file_data, methods=["POST"])
        self.setup_controller()

        print("API Setup Successfully")

    def index(self):
        response = flask.jsonify({
            "message": "Waiting for requests",
            "status": self.status.value
        })
        response.headers['Access-Control-Allow-Origin'] = '*' 
        response.headers['Content-Type'] = 'application/json'

        return response

    def setup_controller(self):
        self.status = APIStatus.SETTING_UP

        CONFIG_PATH = os.path.join(os.path.dirname(__file__), "./config.cfg")
        config_data = CfgUtils.load_configs(CONFIG_PATH)

        SAVE_PATH: str = str(config_data["SavePath"])
        if bool(config_data["RelativePath"]):
            SAVE_PATH = os.path.join(os.path.dirname(__file__), SAVE_PATH)

        chunk_controller: ScreenChunkController = ScreenChunkController(int(config_data["ChunkSize"]))
        self.controller = PeripheralController(
            chunk_controller,
            debug_mode=bool(config_data["DebugMode"]),
            idle_to_afk_threshold=int(config_data["IdleToAfkThreshold"])
        )
        self.listener = GeneralListener(self.controller)

        self.status = APIStatus.READY

    def listen(self):
        listener_thread = Thread(target=self.listener.start)
        listener_thread.start()
        
        data = {"message": "Listening..."}
        response = flask.jsonify(data)
        response.headers['Access-Control-Allow-Origin'] = '*' 
        response.headers['Content-Type'] = 'application/json'

        self.status = APIStatus.LISTENING
        return response

    def stop_listening(self):
        self.listener.stop()
        
        data = {
            "message": "Stopped listening", 
            "body": {
                "chunk_data": HmpPlotUtils.chunk_data_to_dict(self.controller),
                "grid_size": [self.controller.chunk_controller.grid_size.x, self.controller.chunk_controller.grid_size.y], 
                "chunk_size": self.controller.chunk_controller.chunk_size, 
            }
        }
        response = flask.jsonify(data)
        response.headers['Access-Control-Allow-Origin'] = '*' 
        response.headers['Content-Type'] = 'application/json'

        self.status = APIStatus.READY
        return response

    def get_data(self, property: str = "times_hovered"):
        data = {
            "message": "Fetching data", 
            "body": {
                "chunk_data": HmpPlotUtils.chunk_data_to_dict(self.controller, property),
                "grid_size": [self.controller.chunk_controller.grid_size.x, self.controller.chunk_controller.grid_size.y], 
                "chunk_size": self.controller.chunk_controller.chunk_size, 
            }
        }
        response = flask.jsonify(data)
        response.headers['Access-Control-Allow-Origin'] = '*' 
        response.headers['Content-Type'] = 'application/json'

        return response

    def save_file_data(self): 
        request_data: dict = request.get_json()
        file_path = request_data.get("file_path", self.DEFAULT_SAVE_PATH)
        if file_path == "":
            file_path = self.DEFAULT_SAVE_PATH
        
        HmpFileUtils.save_hmp_file(self.controller, file_path)
        data = {
            "message": "Saved file contents",
        }

        response = flask.jsonify(data)
        response.headers['Access-Control-Allow-Origin'] = '*' 
        response.headers['Content-Type'] = 'application/json'
        return response


api = FlaskAPI(__name__)
api.run(port=5000)

print("Finished API Process")