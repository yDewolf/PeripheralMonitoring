import { shutdown_api } from "./ts/api_calls";
import { WebviewWindow } from '@tauri-apps/api/webviewWindow';

let currentWindow = WebviewWindow.getCurrent();
currentWindow.listen('tauri://close-requested', async () => {
    // TODO: Add popup to ask if it should save before closing
    shutdown_api(true);
    console.log("Asked to the API to shutdown");
});