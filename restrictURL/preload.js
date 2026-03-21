const { contextBridge, ipcRenderer } = require('electron');

// 暴露受保护的方法给渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
  // 代理服务控制
  getProxyStatus: () => ipcRenderer.invoke('get-proxy-status'),
  startProxy: () => ipcRenderer.invoke('start-proxy'),
  stopProxy: () => ipcRenderer.invoke('stop-proxy'),
  
  // URL限制管理
  getRestrictedUrls: () => ipcRenderer.invoke('get-restricted-urls'),
  addRestrictedUrl: (url) => ipcRenderer.invoke('add-restricted-url', url),
  removeRestrictedUrl: (url) => ipcRenderer.invoke('remove-restricted-url', url),
  
  // 访问日志
  getAccessLog: (limit) => ipcRenderer.invoke('get-access-log', limit)
});