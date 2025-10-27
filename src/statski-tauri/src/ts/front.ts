import { parse_chunk_data } from './utils';
import { shutdown_api, check_api_status, fetch_chunk_data, start_listening, stop_listening, save_file, APIStatus} from './api_calls';

const DEFAULT_FILE_PATH = "";
const FETCH_INTERVAL: number = 100;
let current_api_status: APIStatus = APIStatus.DOWN;

const Canvas = document.getElementById("MouseHeatmap")!;
const FetchCheckbox = document.getElementById("FetchCheckbox")! as HTMLInputElement;
const StatisticHolder = document.getElementById("main-content")!;
const LeftPanel = document.getElementById("left-panel")!;
const Navbar = document.getElementById("navbar")!;
const ControlPanel = document.getElementById("ControlPanel")!;
const StatusLabel = document.getElementById("StatusLabel")!;

let chunk_property = "times_hovered";
let grid_size = [16, 16];
let pixel_size = 4;
let ratio = 1;

// window.addEventListener('resize', function() {
//     update_canva_size();
// });

setInterval(() => {
    if (current_api_status != APIStatus.LISTENING) {
        return;
    }

    if (!FetchCheckbox.checked) {
        return;
    }
    
    fetch_chunk_data(chunk_property).then(data => {
        if (data.body) {
            if (grid_size != data.body.grid_size) {
                grid_size = data.body.grid_size 
                update_canva_size();
            }
            parse_chunk_data(data.body, Canvas, pixel_size * ratio);
        }
    });
}, FETCH_INTERVAL);

setInterval(() => {
    if (FetchCheckbox.checked) {
        return;
    }
    update_api_status();
}, 250);

const StartListeningButton = document.getElementById("StartListening")!;
StartListeningButton.onclick = () => {
    start_listening().then(() => {
        FetchCheckbox.checked = true;
        update_api_status();
    })
}
const StopListeningButton = document.getElementById("StopListening")!;
StopListeningButton.onclick = () => {
    stop_listening().then(data => {
        if (data.body) {
            parse_chunk_data(data.body, Canvas, pixel_size)
        }
        FetchCheckbox.checked = false;
    })
}

const SaveButton = document.getElementById("SaveFile")!;
SaveButton.onclick = () => {
    save_file(DEFAULT_FILE_PATH)
}

const FinishAPIButton = document.getElementById("FinishAPI")!;
FinishAPIButton.onclick = () => {
    shutdown_api(false).then(data => {
        console.log(data);
    });
}

function update_api_status() {
    check_api_status().then(data => {
        current_api_status = data.status;
        StatusLabel.innerText = "API Status: " + APIStatus[current_api_status];
        
        if (current_api_status == APIStatus.LISTENING) {
            StartListeningButton.classList.add("hidden")
            StopListeningButton.classList.remove("hidden")
        } else {
            StartListeningButton.classList.remove("hidden")
            StopListeningButton.classList.add("hidden")
        }
    });
}

function update_canva_size() {
    let grid_to_pixel = [grid_size[0] * pixel_size, grid_size[1] * pixel_size];
    // TODO: Fix this
    let margin = 5;
    let free_width = window.innerWidth - LeftPanel.clientWidth - margin;
    let free_height = StatisticHolder.clientHeight - Navbar.clientHeight - ControlPanel.clientHeight - margin;

    let target_width_ratio = free_width / grid_to_pixel[0];
    let target_height_ratio = free_height / grid_to_pixel[1];
    if (grid_to_pixel[1] * target_width_ratio <= free_height) {
        ratio = target_width_ratio;
    }
    
    if (grid_to_pixel[0] * target_height_ratio <= free_width) {
        ratio = target_height_ratio;
    }
}