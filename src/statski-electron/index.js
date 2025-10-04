const { app, BrowserWindow } = require('electron/main');
const { execFile } = require('child_process');
// const { api_child } = require('./js/api_shell.js');
// const { PythonShell } = require('python-shell');
var api_child = execFile("../python/dist/FlaskAPI.exe");
console.log(api_child.pid)

api_child.stdout.on('message', function(message) {
  console.log(message);
})

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
  // python_api.kill()
  api_child.kill();

  if (process.platform !== 'darwin') app.quit();
});
