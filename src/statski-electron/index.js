const { app, BrowserWindow } = require('electron/main');
const { python_api } = require('./js/api_shell.js');
const { PythonShell } = require('python-shell');

const createWindow = () => {
  const win = new BrowserWindow({
    width: 1024,
    height: 768,
    titleBarStyle: 'hidden',
    titleBarOverlay: {
      color: '#06041B',
      symbolColor: '#F5FCFF',
      height: 30
    }
  });

  win.loadFile('html/index.html');
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
});

app.on('window-all-closed', () => {
  python_api.kill()

  if (process.platform !== 'darwin') app.quit();
});
