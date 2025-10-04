
import os
from threading import Thread
import flask

from Controllers.PeripheralController import PeripheralController
from Listeners.GeneralListener import GeneralListener
from utils import HmpPlotUtils
from utils.Chunk.ScreenChunkController import ScreenChunkController

class FlaskAPI(flask.Flask):
    controller: PeripheralController
    listener: GeneralListener

    def __init__(self, import_name: str, static_url_path: str | None = None, static_folder: str | os.PathLike[str] | None = "static", static_host: str | None = None, host_matching: bool = False, subdomain_matching: bool = False, template_folder: str | os.PathLike[str] | None = "templates", instance_path: str | None = None, instance_relative_config: bool = False, root_path: str | None = None):
        super().__init__(import_name, static_url_path, static_folder, static_host, host_matching, subdomain_matching, template_folder, instance_path, instance_relative_config, root_path)
        self.add_url_rule("/", view_func=self.index)
        # self.add_url_rule("/setup", view_func=self.setup_controller)
        self.add_url_rule("/listen", view_func=self.listen)
        self.add_url_rule("/stop-listening", view_func=self.stop_listening)
        self.add_url_rule("/get-data/<property>", view_func=self.get_data)
        self.setup_controller()

        print("API Setup Successfully")

    def index(self):
        return {"message": "Waiting for requests"}

    def setup_controller(self):
        chunk_controller: ScreenChunkController = ScreenChunkController(16)
        self.controller = PeripheralController(chunk_controller)
        self.listener = GeneralListener(self.controller)

    def listen(self):
        listener_thread = Thread(target=self.listener.start)
        listener_thread.start()
        
        data = {"message": "Listening..."}
        response = flask.jsonify(data)
        response.headers['Access-Control-Allow-Origin'] = '*' 
        response.headers['Content-Type'] = 'application/json'

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
        return response

        

api = FlaskAPI(__name__)
api.run(port=5000)