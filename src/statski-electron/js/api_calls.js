const API_URL = "http://127.0.0.1:5000/";

function start_listening() {
    fetch(API_URL + "listen", {
        method: 'GET',
        headers: {
        }
    }).then(
    response => {
        return response.json()
    }
    ).then(data => {console.log(data)}).catch(error => {
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

    return response
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