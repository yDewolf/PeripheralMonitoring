import { parse_chunk_data } from './utils';
import { check_api_status, fetch_chunk_data, start_listening, stop_listening, save_file} from './api_calls';

const DEFAULT_FILE_PATH = "";
let current_api_status = 0;

const Canvas = document.getElementById("MouseHeatmap")!;
const FetchCheckbox = document.getElementById("FetchCheckbox")! as HTMLInputElement;
const StatisticHolder = document.getElementById("main-content")!;
const LeftPanel = document.getElementById("left-panel")!;
const Navbar = document.getElementById("navbar")!;
const StatusLabel = document.getElementById("StatusLabel")!;

let chunk_property = "times_hovered";
let grid_size = [16, 16];
let pixel_size = 4;
let ratio = 1;

window.addEventListener('resize', function() {
    let grid_to_pixel = [grid_size[0] * pixel_size, grid_size[1] * pixel_size];
    // TODO: Fix this
    let free_width = this.window.innerWidth - LeftPanel.clientWidth;
    let free_height = StatisticHolder.clientHeight - Navbar.clientHeight;
    if (grid_to_pixel[0] >= free_width) {
        ratio = free_width / grid_to_pixel[0];
    } else {
        ratio = grid_to_pixel[0] / free_width;
    }

    if (grid_to_pixel[1] >= free_height) {
        ratio = Math.min(ratio, free_height / grid_to_pixel[1]);
    }

    Canvas.style.scale = ratio.toString();

    Canvas.setAttribute("width", (grid_size[0] * pixel_size * ratio).toString());
    Canvas.setAttribute("height", (grid_size[1] * pixel_size * ratio).toString());
});

setInterval(() => {
    if (current_api_status != 3) {
        return;
    }

    if (!FetchCheckbox.checked) {
        return;
    }
    fetch_chunk_data(chunk_property).then(data => {
        if (data.body) {
            grid_size = data.body.grid_size 
            parse_chunk_data(data.body, Canvas, pixel_size * ratio);
        }
    });
}, 200);

setInterval(() => {
    if (FetchCheckbox.checked) {
        return;
    }
    check_api_status().then(data => {
        current_api_status = data.status;
        StatusLabel.innerText = "API Status: " + current_api_status;
    });
    if (current_api_status == 3) {
        StartListeningButton.classList.add("hidden")
        StopListeningButton.classList.remove("hidden")
    } else {
        StartListeningButton.classList.remove("hidden")
        StopListeningButton.classList.add("hidden")
    }
}, 250);

const StartListeningButton = document.getElementById("StartListening")!;
StartListeningButton.onclick = () => {
    start_listening().then(() => {
        FetchCheckbox.checked = true;
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