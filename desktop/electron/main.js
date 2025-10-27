const { app, BrowserWindow, ipcMain, Menu } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const Store = require('electron-store');

const store = new Store();
let mainWindow;
let pythonProcess;

// Configuração do servidor Python
const PYTHON_PORT = 8000;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 700,
    titleBarStyle: 'hiddenInset',
    backgroundColor: '#0a0a0a',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, '../assets/icons/icon.png')
  });

  // Menu customizado
  const template = [
    {
      label: 'JustoBot',
      submenu: [
        { role: 'about', label: 'Sobre JustoBot' },
        { type: 'separator' },
        { role: 'services' },
        { type: 'separator' },
        { role: 'hide', label: 'Ocultar JustoBot' },
        { role: 'hideOthers', label: 'Ocultar Outros' },
        { role: 'unhide', label: 'Mostrar Tudo' },
        { type: 'separator' },
        { role: 'quit', label: 'Sair' }
      ]
    },
    {
      label: 'Editar',
      submenu: [
        { role: 'undo', label: 'Desfazer' },
        { role: 'redo', label: 'Refazer' },
        { type: 'separator' },
        { role: 'cut', label: 'Recortar' },
        { role: 'copy', label: 'Copiar' },
        { role: 'paste', label: 'Colar' },
        { role: 'selectAll', label: 'Selecionar Tudo' }
      ]
    },
    {
      label: 'Visualizar',
      submenu: [
        { role: 'reload', label: 'Recarregar' },
        { role: 'forceReload', label: 'Forçar Recarga' },
        { role: 'toggleDevTools', label: 'Ferramentas de Desenvolvimento' },
        { type: 'separator' },
        { role: 'resetZoom', label: 'Zoom Normal' },
        { role: 'zoomIn', label: 'Aumentar Zoom' },
        { role: 'zoomOut', label: 'Diminuir Zoom' },
        { type: 'separator' },
        { role: 'togglefullscreen', label: 'Tela Cheia' }
      ]
    },
    {
      label: 'Janela',
      submenu: [
        { role: 'minimize', label: 'Minimizar' },
        { role: 'zoom', label: 'Zoom' },
        { type: 'separator' },
        { role: 'front', label: 'Trazer para Frente' }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);

  // Carrega a aplicação
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Inicia o servidor Python
function startPythonServer() {
  const pythonPath = path.join(__dirname, '../../venv/bin/python3');
  const mainPath = path.join(__dirname, '../../app/main.py');

  pythonProcess = spawn(pythonPath, [
    '-m', 'uvicorn',
    'app.main:app',
    '--host', '127.0.0.1',
    '--port', String(PYTHON_PORT),
    '--log-level', 'info'
  ], {
    cwd: path.join(__dirname, '../..'),
    env: {
      ...process.env,
      PYTHONPATH: path.join(__dirname, '../..')
    }
  });

  pythonProcess.stdout.on('data', (data) => {
    console.log(`[Python] ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`[Python Error] ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
  });
}

// Para o servidor Python
function stopPythonServer() {
  if (pythonProcess) {
    pythonProcess.kill();
    pythonProcess = null;
  }
}

// IPC Handlers
ipcMain.handle('get-config', (event, key) => {
  return store.get(key);
});

ipcMain.handle('set-config', (event, key, value) => {
  store.set(key, value);
  return true;
});

ipcMain.handle('get-all-config', () => {
  return store.store;
});

ipcMain.handle('delete-config', (event, key) => {
  store.delete(key);
  return true;
});

ipcMain.handle('get-api-url', () => {
  return `http://127.0.0.1:${PYTHON_PORT}`;
});

// Lifecycle
app.on('ready', () => {
  startPythonServer();

  // Aguarda servidor iniciar
  setTimeout(createWindow, 3000);
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    stopPythonServer();
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

app.on('before-quit', () => {
  stopPythonServer();
});

// Tratamento de erros
process.on('uncaughtException', (error) => {
  console.error('Uncaught exception:', error);
});
