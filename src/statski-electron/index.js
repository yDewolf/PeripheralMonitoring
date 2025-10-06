const { app, BrowserWindow } = require('electron/main');
const { execFile } = require('child_process');
// const { api_child } = require('./js/api_shell.js');
// const { PythonShell } = require('python-shell');
const api_child = execFile("../python/dist/FlaskAPI.exe", [__dirname + "../python/config.cfg"], (error, stdout, stderr) => {
  if (error) {
    throw error;
  }

  console.log(stdout);
});

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
  api_child.kill();
  api_child.kill();

  if (process.platform !== 'darwin') app.quit();
});
