import { Window } from "@tauri-apps/api/window";
import { shutdown_api } from "./ts/api_calls";

let currentWindow = Window.getCurrent();
currentWindow.onCloseRequested(async (event) => {
    // TODO: Add popup to ask if it should save before closing
    console.log("Asked to the API to shutdown");
    await shutdown_api(true);
    console.log("API shutted down | Event id: ", event.id);
});
