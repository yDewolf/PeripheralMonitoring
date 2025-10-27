const API_URL = "http://127.0.0.1:5000/";

export {check_api_status, shutdown_api, fetch_chunk_data, start_listening, stop_listening, save_file, update_config, get_config, restart_api};

export enum APIStatus {
    DOWN = 0,
    SETTING_UP = 1,
    READY = 2,
    LISTENING = 3,
    FINISHING = 4
}

export interface BaseResponse {
    message: string;
    body: ChunkBody | ConfigBody;
    status: number;
}

export interface ChunkResponse {
    message: string;
    body: ChunkBody;
    status: number;
}

export interface ConfigResponse {
    message: string;
    body: ConfigBody;
    status: number;
}

export interface ChunkBody {
    chunk_data: ChunkData;
    grid_size: [number, number];
    chunk_size: number;
}

export interface ConfigBody {
    config: Object
}

interface ChunkData {
    property: string;
    chunks: Map<string, number>;
    maximum: number;
}

async function check_api_status(): Promise<BaseResponse> {
    const response: BaseResponse = await fetch(API_URL, {
        method: 'GET',
        headers: {}
    }).then(
        response => {
            return response.json()
        }
    ).catch(error => {
        console.error('Error fetching data:', error); 
    });

    return response;
}

async function shutdown_api(save_before_shutting_down: boolean = true): Promise<BaseResponse> {
    const response: BaseResponse = await fetch(API_URL + "shutdown/" + save_before_shutting_down, {
        method: 'POST',
        headers: {
        },
    }).then(
    response => {
        return response.json()
    }
    ).then().catch(error => {
        console.error('Error fetching data:', error); 
    });

    return response;
}

async function restart_api(): Promise<BaseResponse> {
    const response: BaseResponse = await fetch(API_URL + "restart", {
        method: 'POST',
        headers: {
        },
    }).then(
    response => {
        return response.json()
    }
    ).then().catch(error => {
        console.error('Error fetching data:', error); 
    });

    return response;
}

async function start_listening() {
    await fetch(API_URL + "listen", {
        method: 'POST',
        headers: {
        }
    }).then(
    response => {
        return response.json()
    }
    ).then().catch(error => {
        console.error('Error fetching data:', error); 
    });
}

async function stop_listening(): Promise<ChunkResponse> {
    const response: ChunkResponse = await fetch(API_URL + "stop-listening", {
        method: 'POST',
        headers: {
            
        }
    }).then(
        response => {
            return response.json();
        }
    ).catch(error => {
        console.error('Error fetching data:', error); 
    });
    
    let chunks: Map<string, number> = new Map(Object.entries(response.body.chunk_data.chunks));
    response.body.chunk_data.chunks = chunks;
    return response;
}

async function fetch_chunk_data(chunk_property: string, recent_only: boolean): Promise<ChunkResponse> {
    const response: ChunkResponse = await fetch(API_URL + "get-data/" + chunk_property + "/" + recent_only, {
        method: 'GET',
        headers: {

        }
    }).then(
        response => {
            return response.json()
        }
    ).catch(error => {
        console.error('Error fetching data:', error);
    });
    
    let chunks: Map<string, number> = new Map(Object.entries(response.body.chunk_data.chunks));
    response.body.chunk_data.chunks = chunks;
    return response;
}

async function save_file(file_path: string): Promise<BaseResponse> {
    const response: BaseResponse = await fetch(API_URL + "save-file-data/", {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "file_path": file_path
        })
    }).then(
        response => {
            return response.json()
        }
    ).catch(error => {
        console.error('Error fetching data:', error);
    });

    return response;
}

async function get_config(): Promise<ConfigResponse> {
    const response: ConfigResponse = await fetch(API_URL + "get-config/", {
        method: 'GET',
        headers: {
            
        },
    }).then(
        response => {
            return response.json()
        }
    ).catch(error => {
        console.error('Error fetching data:', error);
    });

    return response;
}

async function update_config(config_data: Object): Promise<ConfigResponse> {
    console.log(config_data);
    for (let key in config_data) {
        // @ts-expect-error    
        switch (config_data[key].toLowerCase()) {
            case "on":
                // @ts-expect-error    
                config_data[key] = true;
                break;
            case "off":
                // @ts-expect-error    
                config_data[key] = false;
                break;
            case "true": 
                // @ts-expect-error    
                config_data[key] = true;
                break;
            case "false":
                // @ts-expect-error    
                config_data[key] = false;
                break;
        }
    }
    console.log(JSON.stringify({"config_data": config_data}));
    
    const response: ConfigResponse = await fetch(API_URL + "update-config/", {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"config_data": config_data})
    }).then(
        response => {
            return response.json()
        }
    ).catch(error => {
        console.error('Error fetching data:', error);
    });

    return response;
}