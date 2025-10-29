import { shutdown_api } from "./ts/api_calls";
import { getCurrentWindow } from '@tauri-apps/api/window';

const appWindow = getCurrentWindow();
appWindow.onCloseRequested(async (event) => {
    // TODO: Add popup to ask if it should save before closing
    console.log("Asked to the API to shutdown");
    shutdown_api(true).then((data) => {
        console.log(data);
    });
    console.log("API shutted down | Event id: ", event.id);
});

document
  .getElementById('titlebar-minimize')
  ?.addEventListener('click', () => appWindow.minimize());
document
  .getElementById('titlebar-maximize')
  ?.addEventListener('click', () => appWindow.toggleMaximize());
document
  .getElementById('titlebar-close')
  ?.addEventListener('click', () => appWindow.close());

export let isFocused: boolean = true;
export let isMouseInside: boolean = true;

setInterval(async () => {
  if (isMouseInside) {
    return;
  }
  isFocused = await appWindow.isFocused();
}, 250);

document.addEventListener("mouseenter", () => {
  isFocused = true;
  isMouseInside = true;
});

document.addEventListener("mouseleave", () => {
  isFocused = false;
  isMouseInside = false;
});