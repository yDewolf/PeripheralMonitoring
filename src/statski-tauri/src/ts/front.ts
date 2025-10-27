import { parse_chunk_data } from './utils';
import { shutdown_api, check_api_status, fetch_chunk_data, start_listening, stop_listening, save_file, get_config, update_config, APIStatus, restart_api} from './api_calls';

const DEFAULT_FILE_PATH = "";
const FETCH_INTERVAL: number = 100;
let current_api_status: APIStatus = APIStatus.DOWN;

const Canvas = document.getElementById("MouseHeatmap")!;
const FetchCheckbox = document.getElementById("FetchCheckbox")! as HTMLInputElement;
const StatisticHolder = document.getElementById("main-content")!;
const LeftPanel = document.getElementById("left-panel")!;
const Navbar = document.getElementById("navbar")!;
const PageContent = document.getElementById("PageContent")!;
const Overlay = document.getElementById("Overlay")!;
const ControlPanel = document.getElementById("ControlPanel")!;
const StatusLabel = document.getElementById("StatusLabel")!;

let chunk_property = "times_hovered";
let grid_size = [16, 16];
let pixel_size = 4;
let ratio = 1;

// FIXME
// window.addEventListener("resize", function() {
//     if (FetchCheckbox.checked) {
//         return;
//     }
//     // update_canva_size();
// })

setInterval(() => {
    if (current_api_status != APIStatus.LISTENING) {
        return;
    }

    if (!FetchCheckbox.checked) {
        return;
    }
    
    fetch_chunk_data(chunk_property, true).then(data => {
        if (data.body) {
            grid_size = data.body.grid_size
            update_canva_size();

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

        fetch_chunk_data(chunk_property, false).then(data => {
        if (data.body) {
            grid_size = data.body.grid_size
            update_canva_size();

            parse_chunk_data(data.body, Canvas, pixel_size * ratio);
        }
    });
    })
}
const StopListeningButton = document.getElementById("StopListening")!;
StopListeningButton.onclick = () => {
    stop_listening().then(data => {
        if (data.body) {
            parse_chunk_data(data.body, Canvas, pixel_size * ratio)
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

const RestartAPIButton = document.getElementById("RestartAPI")!;
RestartAPIButton.onclick = () => {
    FetchCheckbox.checked = false;
    current_api_status = APIStatus.DOWN;
    restart_api();
}

const SettingsButton = document.getElementById("Settings")!;
SettingsButton.onclick = () => {
    get_config().then((data) => {
        show_settings_menu(data.body.config);
    });
}

const CloseSettingsButton = document.getElementById("CloseSettings")!;
CloseSettingsButton.onclick = () => {
    hide_settings_menu();
}

const SettingsForm = document.getElementById("SettingsForm")! as HTMLFormElement;
const UpdateConfigButton = document.getElementById("UpdateConfig")!;
UpdateConfigButton.onclick = () => {
    const formData = new FormData(SettingsForm);
    let data = Object.fromEntries(formData);

    update_config(data);
}

function hide_settings_menu() {
    PageContent.classList.remove("behind-overlay");
    Overlay.classList.add("hidden");
}

function show_settings_menu(config: Object) {
    generate_settings_menu(config);
    Overlay.classList.remove("hidden");
    PageContent.classList.add("behind-overlay");
}

function generate_settings_menu(config: Object) {
    const FieldList = document.getElementById("ConfigFields")!;
    FieldList.innerHTML = "";
    for (let key in config) {
        let value = config[key as keyof Object].toString();
        let input_type = "text";
        let value_str = `value='${value}'`;
        if (value.toLowerCase() == "true" || value.toLowerCase() == "false") {
            input_type = "checkbox";
            FieldList.innerHTML += `<input type='hidden' value='False' name="${key}">`

            value_str = "";
            if (value.toLowerCase() == "true") {
                value_str = "checked";
            }
        } else {
            let number = Number(value.trim());
            if (!isNaN(number) && isFinite(number)) {
                input_type = "number";
            }
        }

        let html = `
            <li class='config-row'>
                <label for='${key}'>${key}:</label>
                <input type='${input_type}' name='${key}' id='${key}' ${value_str}>
            </li>
        `
        FieldList.innerHTML += html;
    }
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

    Canvas.setAttribute("width", (grid_size[0] * pixel_size * ratio).toString());
    Canvas.setAttribute("height", (grid_size[1] * pixel_size * ratio).toString());
}