from pynput.mouse import Controller, Listener
from screeninfo import get_monitors
import math

CHUNK_SIZE: int = 32
class Chunk:
    position: tuple

    times_hovered: int = 0

    idle_time: int = 0
    max_idle_time: int = 0

    times_pressed: dict

    def __init__(self, pos: tuple) -> None:
        self.position = pos
        self.times_pressed = {
            "left": 0,
            "right": 0,
        }


    def getIdx(self) -> int:
        return self.position[0] + self.position[1] * CHUNK_SIZE

mouse = Controller()

total_width: int = 0
max_height: int = 0
for monitor in get_monitors():
    max_height = max(max_height, monitor.height)
    total_width += monitor.width

chunks = []
for x in range(round(total_width / CHUNK_SIZE)):
    row: list[Chunk] = []
    for y in range(round(max_height / CHUNK_SIZE)):
        row.append(Chunk((x, y)))
    
    chunks.append(row)


def on_mouse_move(x, y):
    x = math.floor(x / CHUNK_SIZE)
    y = math.floor(y / CHUNK_SIZE)

    print(f"Current Chunk: {chunks[x][y].position} | Times Pressed: {chunks[x][y].times_pressed}")

    # print(f"Moved to {x}, {y}")

def on_mouse_click(x, y, button, pressed):
    if button.name == "middle":
        return False

    x = math.floor(x / CHUNK_SIZE)
    y = math.floor(y / CHUNK_SIZE)

    chunks[x][y].times_pressed["left"] += 1
    print(f"Clicked {button} at {x}, {y} | pressed: {pressed} | button: {button}")

with Listener(
    on_move=on_mouse_move,
    on_click=on_mouse_click,
) as listener:
    listener.join()
