# Warning!
This project is made for fun and can be potentially dangerous!!
- This project consists of generating statistics of your peripheral use

# How to Run:
This project has 2 main running methods:
1. **By running the backend standalone**:
    You can run it by running ``src/python/main.py``
    You can also run the compiled backend at ``src/python/dist/``
2. **By running / installing the Tauri application**:
    You can download any release of it at the [releases tab](https://github.com/yDewolf/PeripheralMonitoring/releases)
    (for development you can use ``npm run tauri dev`` at ``src/statski-tauri/``)

## Dependencies:
- Backend (Python Dependencies):
    Dependencies are listed at [Requirements.txt](https://github.com/yDewolf/PeripheralMonitoring/blob/main/requirements.txt)
    use ```pip install -r requirements.txt``` to install them
- Frontend (Development):
    Are listed at [src/statski-tauri/package.json](https://github.com/yDewolf/PeripheralMonitoring/blob/main/src/statski-tauri/package.json)
    The main dependency are ``Tauri``, ``Vite`` and ``typescript``;
    you can install them with ``npm install``.

## About key logging:
- This program **doesn't track when you pressed a key**, but it will count how many times you pressed each key of your keyboard **(detects every key press at any time)**
