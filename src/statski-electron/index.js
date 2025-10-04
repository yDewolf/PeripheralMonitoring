const { app, BrowserWindow } = require('electron/main');
// import { python_api } from 'js/api_shell.js'; 
const { python_api } = require('./js/api_shell.js')

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
  if (process.platform !== 'darwin') app.quit();
});
