const API_URL = "http://127.0.0.1:5000/";

export {check_api_status, fetch_chunk_data, start_listening, stop_listening, save_file};

export interface BaseResponse {
    message: string;
    body: ChunkBody | null;
    status: number;
}

export interface ChunkBody {
    chunk_data: ChunkData;
    grid_size: [number, number];
    chunk_size: number;
}

interface ChunkData {
    property: string;
    chunks: [Float32Array];
}

async function check_api_status() {
    const response: BaseResponse = await fetch(API_URL, {
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

    return response;
}

async function start_listening() {
    await fetch(API_URL + "listen", {
        method: 'GET',
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

async function stop_listening() {
    const response: BaseResponse = await fetch(API_URL + "stop-listening", {
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

    return response;
}

async function fetch_chunk_data(chunk_property: string) {
    const response: BaseResponse = await fetch(API_URL + "get-data/" + chunk_property, {
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
    
    return response;
}

async function save_file(file_path: string) {
    const response: BaseResponse = await fetch(API_URL + "save-file-data", {
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