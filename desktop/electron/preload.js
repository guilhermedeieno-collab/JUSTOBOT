const { contextBridge, ipcRenderer } = require('electron');

// Expõe API segura para o renderer
contextBridge.exposeInMainWorld('electron', {
  // Configurações
  config: {
    get: (key) => ipcRenderer.invoke('get-config', key),
    set: (key, value) => ipcRenderer.invoke('set-config', key, value),
    getAll: () => ipcRenderer.invoke('get-all-config'),
    delete: (key) => ipcRenderer.invoke('delete-config', key)
  },

  // API
  api: {
    getUrl: () => ipcRenderer.invoke('get-api-url')
  },

  // Info do sistema
  platform: process.platform,
  version: process.versions.electron
});
