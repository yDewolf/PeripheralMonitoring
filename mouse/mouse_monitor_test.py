from pynput.mouse import Controller, Listener

mouse = Controller()

def on_mouse_move(x, y):
    print(f"Moved to {x}, {y}")

def on_mouse_click(x, y, button, pressed):
    print(f"Clicked {button} at {x}, {y} | pressed: {pressed}")

with Listener(
    on_move=on_mouse_move,
    on_click=on_mouse_click,
) as listener:
    listener.join()