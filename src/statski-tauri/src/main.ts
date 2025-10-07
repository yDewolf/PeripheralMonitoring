import { shutdown_api } from "./ts/api_calls";

window.onclose = (_ev: Event) => {
    // TODO: Add popup to ask if it should save before closing
    shutdown_api(true);
    console.log("Asked to the API to shutdown");
};