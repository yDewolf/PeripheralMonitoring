const API_URL = "http://127.0.0.1:5000/";

async function check_api_status() {
    const response = await fetch(API_URL, {
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

function start_listening() {
    fetch(API_URL + "listen", {
        method: 'GET',
        headers: {
        }
    }).then(
    response => {
        return response.json()
    }
    ).then(data => {}).catch(error => {
        console.error('Error fetching data:', error); 
    });
}

async function stop_listening() {
    const response = await fetch(API_URL + "stop-listening", {
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

async function fetch_chunk_data(chunk_property) {
    const response = await fetch(API_URL + "get-data/" + chunk_property, {
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

async function save_file(file_path) {
    const response = await fetch(API_URL + "save-file-data", {
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