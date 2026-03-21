const { app, BrowserWindow, Tray, Menu, ipcMain, dialog } = require('electron');
const path = require('path');
const isDev = process.argv.includes('--dev');

// 导入代理服务器
const ProxyServer = require('./proxy/proxy.js');
// 导入数据库
const Database = require('./database/db.js');

let mainWindow = null;
let tray = null;
let proxyServer = null;
let database = null;

// 创建主窗口
function createMainWindow() {
  const iconFileName = process.platform === 'win32' ? 'icon.ico' : 'icon.png';
  const iconPath = path.join(__dirname, 'assets', iconFileName);

  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true
    },
    icon: iconPath,
    show: false // 初始不显示，通过托盘菜单控制
  });

  mainWindow.loadFile('renderer/index.html');

  // 开发模式下打开开发者工具
  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  // 窗口关闭时隐藏而不是退出
  mainWindow.on('close', (event) => {
    if (!app.isQuitting) {
      event.preventDefault();
      mainWindow.hide();
    }
  });
}

// 创建系统托盘
function createTray() {
  const nativeImage = require('electron').nativeImage;
  // 根据平台选择图标
  const iconFileName = process.platform === 'win32' ? 'icon.ico' : 'icon.png';
  const iconPath = path.join(__dirname, 'assets', iconFileName);
  
  try {
    // 尝试加载图标
    let icon = nativeImage.createFromPath(iconPath);
    
    // 如果加载失败（比如图标文件损坏或路径错误），尝试使用 png
    if (icon.isEmpty() && process.platform === 'win32') {
      console.warn('icon.ico 加载失败，尝试使用 icon.png');
      icon = nativeImage.createFromPath(path.join(__dirname, 'assets/icon.png'));
    }
    
    // 如果仍然为空，这将导致托盘图标不可见，但不会崩溃
    tray = new Tray(icon);
  } catch (error) {
    console.error('创建托盘失败:', error);
    // 如果图标加载完全失败，使用默认空图标防止程序崩溃
    const emptyIcon = nativeImage.createEmpty();
    tray = new Tray(emptyIcon);
  }

  const contextMenu = Menu.buildFromTemplate([
    {
      label: '显示主窗口',
      click: () => {
        if (mainWindow) {
          mainWindow.show();
          mainWindow.focus();
        } else {
          createMainWindow();
        }
      }
    },
    { type: 'separator' },
    {
      label: '代理服务状态',
      click: () => {
        const status = proxyServer ? proxyServer.isRunning() ? '运行中' : '已停止' : '未初始化';
        dialog.showMessageBox({
          type: 'info',
          title: '代理服务状态',
          message: `当前代理服务状态: ${status}`
        });
      }
    },
    { type: 'separator' },
    {
      label: '退出',
      click: () => {
        app.isQuitting = true;
        if (proxyServer && proxyServer.isRunning()) {
          proxyServer.stop();
        }
        app.quit();
      }
    }
  ]);

  tray.setToolTip('网址限制器');
  tray.setContextMenu(contextMenu);

  // 双击托盘图标显示主窗口
  tray.on('double-click', () => {
    if (mainWindow) {
      if (mainWindow.isVisible()) {
        mainWindow.hide();
      } else {
        mainWindow.show();
        mainWindow.focus();
      }
    } else {
      createMainWindow();
    }
  });
}

// 应用程序准备就绪
app.whenReady().then(async () => {
  try {
    // 初始化数据库
    database = new Database();
    await database.connect();
    
    createMainWindow();
    createTray();
    
    // 初始化代理服务器
    proxyServer = new ProxyServer(database);
    
    // 从数据库加载限制的URL
    const restrictedUrls = await database.getRestrictedUrls();
    restrictedUrls.forEach(urlObj => {
      proxyServer.addRestrictedUrl(urlObj.url);
    });
    
    // 默认启动代理服务器
    proxyServer.start().then(() => {
      console.log('代理服务器已启动');
    }).catch(err => {
      console.error('启动代理服务器失败:', err);
    });
  } catch (error) {
    console.error('应用程序初始化失败:', error);
  }

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow();
    }
  });
});

// 所有窗口关闭时退出应用（macOS除外）
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.hide();
  }
});

// 应用程序退出前清理
app.on('before-quit', async () => {
  app.isQuitting = true;
  if (proxyServer && proxyServer.isRunning()) {
    proxyServer.stop();
  }
  if (database) {
    await database.close();
  }
});

// IPC 处理程序
ipcMain.handle('get-proxy-status', () => {
  return proxyServer ? proxyServer.isRunning() : false;
});

ipcMain.handle('start-proxy', async () => {
  if (!proxyServer) {
    proxyServer = new ProxyServer(database);
  }
  
  try {
    await proxyServer.start();
    return { success: true, message: '代理服务器已启动' };
  } catch (error) {
    return { success: false, message: `启动失败: ${error.message}` };
  }
});

ipcMain.handle('stop-proxy', () => {
  if (proxyServer && proxyServer.isRunning()) {
    proxyServer.stop();
    return { success: true, message: '代理服务器已停止' };
  }
  return { success: false, message: '代理服务器未运行' };
});

ipcMain.handle('get-restricted-urls', async () => {
  if (!database) {
    return [];
  }
  
  try {
    const urls = await database.getRestrictedUrls();
    return urls.map(urlObj => urlObj.url);
  } catch (error) {
    console.error('获取限制URL列表失败:', error);
    return [];
  }
});

ipcMain.handle('add-restricted-url', async (event, url) => {
  if (!database || !proxyServer) {
    return { success: false, message: '数据库或代理服务器未初始化' };
  }
  
  try {
    // 添加到数据库
    await database.addRestrictedUrl(url);
    // 添加到代理服务器
    proxyServer.addRestrictedUrl(url);
    return { success: true, message: `已添加限制: ${url}` };
  } catch (error) {
    console.error('添加限制URL失败:', error);
    return { success: false, message: `添加失败: ${error.message}` };
  }
});

ipcMain.handle('remove-restricted-url', async (event, url) => {
  if (!database || !proxyServer) {
    return { success: false, message: '数据库或代理服务器未初始化' };
  }
  
  try {
    // 从数据库移除
    await database.removeRestrictedUrl(url);
    // 从代理服务器移除
    proxyServer.removeRestrictedUrl(url);
    return { success: true, message: `已移除限制: ${url}` };
  } catch (error) {
    console.error('移除限制URL失败:', error);
    return { success: false, message: `移除失败: ${error.message}` };
  }
});

ipcMain.handle('get-access-log', async (event, limit = 100) => {
  if (!database) {
    return [];
  }
  
  try {
    return await database.getAccessLog(limit);
  } catch (error) {
    console.error('获取访问日志失败:', error);
    return [];
  }
});