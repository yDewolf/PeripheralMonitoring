const API_URL = "http://127.0.0.1:5000/";

export {check_api_status, shutdown_api, fetch_chunk_data, toggle_listening, save_file, update_config, get_config, restart_api};

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

async function toggle_listening() {
    const response: ChunkResponse = await fetch(API_URL + "toggle-listen", {
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

async function update_config(form_data: FormData): Promise<ConfigResponse> {
    let config_data: Map<string, any> = new Map();
    form_data.forEach((value: any, key: string) => {
        config_data.set(key, value);
        if (typeof value == 'string') {
            switch (value.toString().toLowerCase()) {
                case "on":
                    config_data.set(key, true);
                    break;
                case "off":
                    config_data.set(key, false);
                    break;
                case "true": 
                    config_data.set(key, true);
                    break;
                case "false":
                    config_data.set(key, false);
                    break;
            }
            return;
        }
    })

    const response: ConfigResponse = await fetch(API_URL + "update-config/", {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"config_data": Object.fromEntries(config_data.entries())})
    }).then(
        response => {
            return response.json()
        }
    ).catch(error => {
        console.error('Error fetching data:', error);
    });

    return response;
}