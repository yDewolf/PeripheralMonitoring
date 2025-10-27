import { Color } from "@tauri-apps/api/webview";
import { ChunkBody } from "./api_calls";

const SEISMIC_GRADIENT = [
    [0, 0, 85],
    [0, 0, 255],
    [255, 255, 255],
    [255, 7, 7],
    [170, 0, 0],
];

export { parse_chunk_data };

function parse_chunk_data(chunk_data_body: ChunkBody, canvas: any, pixel_size: number) {
    let context = canvas.getContext("2d");
    let gradient = SEISMIC_GRADIENT;

    context.fillStyle = 'rgba('+gradient[0][0] + ',' + gradient[0][1] + ',' + gradient[0][2] +','+ 1 + ')';
    context.fillRect(0, 0, canvas.width, canvas.height);

    let chunk_data = chunk_data_body.chunk_data.chunks;

    for (const key in chunk_data) {
        const split = key.split(",");
        const x = Number(split[0]);
        const y = Number(split[1]);
        let value = Number(chunk_data[key as keyof Object]);
        if (value == undefined) {
            continue;
        }
        let color_rgb = interpolate_between_gradient(gradient, value);
        let color = 'rgba('+color_rgb[0] + ',' + color_rgb[1] + ',' + color_rgb[2] +','+ 1 + ')';
        drawDot(context, x, y, color, pixel_size);
    }
}

function interpolate_between_gradient(gradient: any, delta: number) {
    let total_delta = delta * gradient.length;
    let start_idx = Math.max(Math.floor((gradient.length * delta) - 1), 0);
    let rgb = gradient[start_idx];
    for (let idx = start_idx; idx < gradient.length; idx++) {
        rgb = rgb_interpolate(
            rgb[0], rgb[1], rgb[2],
            gradient[idx][0], gradient[idx][1], gradient[idx][2],
            total_delta
        )
        total_delta = Math.max(total_delta - idx, 0);
    }

    return rgb;
}

function rgb_interpolate(r: number, g: number, b: number, r1: number, g1: number, b1: number, delta: number) {
    let new_r = r + (r1 - r) * delta;
    let new_g = g + (g1 - g) * delta;
    let new_b = b + (b1 - b) * delta;

    return [new_r, new_g, new_b];
}

function drawDot(context: any, x: number, y: any, color: Color, size: number = 1) {
    context.fillStyle = color;
    context.fillRect(x * size, y * size, size, size);
}