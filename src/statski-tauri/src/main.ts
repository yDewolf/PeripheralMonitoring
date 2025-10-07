import { Command } from '@tauri-apps/plugin-shell';
const command = Command.sidecar('FlaskAPI');
const child = await command.spawn();

window.onclose = (ev: Event) => {
    child.kill();
};