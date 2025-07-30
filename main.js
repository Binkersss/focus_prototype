const { app, BrowserWindow, ipcMain } = require('electron/main')
const path = require('path')

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: {
        preload: path.join(__dirname, 'preload.js')
    }
  })

  mainWindow.loadFile('pages/welcome.html');
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

ipcMain.on('navigate', (_, page) => {
  mainWindow.loadFile(`pages/${page}.html`);
});
