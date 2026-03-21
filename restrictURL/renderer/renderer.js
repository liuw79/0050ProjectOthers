// DOM元素
const proxyStatus = document.getElementById('proxy-status');
const statusDot = proxyStatus.querySelector('.status-dot');
const statusText = proxyStatus.querySelector('.status-text');
const startProxyBtn = document.getElementById('start-proxy');
const stopProxyBtn = document.getElementById('stop-proxy');
const newUrlInput = document.getElementById('new-url');
const addUrlBtn = document.getElementById('add-url');
const restrictedUrlsList = document.getElementById('restricted-urls');
const refreshLogBtn = document.getElementById('refresh-log');
const clearLogBtn = document.getElementById('clear-log');
const accessLogTable = document.getElementById('access-log');
const toast = document.getElementById('toast');

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', () => {
    updateProxyStatus();
    loadRestrictedUrls();
    loadAccessLog();
    
    // 设置定时更新
    setInterval(updateProxyStatus, 5000);
    setInterval(loadAccessLog, 10000);
});

// 更新代理状态
async function updateProxyStatus() {
    try {
        const isRunning = await window.electronAPI.getProxyStatus();
        
        if (isRunning) {
            statusDot.classList.add('running');
            statusDot.classList.remove('stopped');
            statusText.textContent = '运行中';
            startProxyBtn.disabled = true;
            stopProxyBtn.disabled = false;
        } else {
            statusDot.classList.add('stopped');
            statusDot.classList.remove('running');
            statusText.textContent = '已停止';
            startProxyBtn.disabled = false;
            stopProxyBtn.disabled = true;
        }
    } catch (error) {
        console.error('获取代理状态失败:', error);
        statusDot.classList.remove('running', 'stopped');
        statusText.textContent = '状态未知';
        startProxyBtn.disabled = false;
        stopProxyBtn.disabled = true;
    }
}

// 启动代理服务器
startProxyBtn.addEventListener('click', async () => {
    try {
        const result = await window.electronAPI.startProxy();
        if (result.success) {
            showToast(result.message, 'success');
            updateProxyStatus();
        } else {
            showToast(result.message, 'error');
        }
    } catch (error) {
        showToast('启动代理服务器失败', 'error');
        console.error('启动代理服务器失败:', error);
    }
});

// 停止代理服务器
stopProxyBtn.addEventListener('click', async () => {
    try {
        const result = await window.electronAPI.stopProxy();
        if (result.success) {
            showToast(result.message, 'success');
            updateProxyStatus();
        } else {
            showToast(result.message, 'error');
        }
    } catch (error) {
        showToast('停止代理服务器失败', 'error');
        console.error('停止代理服务器失败:', error);
    }
});

// 添加限制URL
addUrlBtn.addEventListener('click', async () => {
    const url = newUrlInput.value.trim();
    if (!url) {
        showToast('请输入要限制的网址', 'error');
        return;
    }
    
    try {
        const result = await window.electronAPI.addRestrictedUrl(url);
        if (result.success) {
            showToast(result.message, 'success');
            newUrlInput.value = '';
            loadRestrictedUrls();
        } else {
            showToast(result.message, 'error');
        }
    } catch (error) {
        showToast('添加限制URL失败', 'error');
        console.error('添加限制URL失败:', error);
    }
});

// 回车键添加URL
newUrlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addUrlBtn.click();
    }
});

// 加载限制的URL列表
async function loadRestrictedUrls() {
    try {
        const urls = await window.electronAPI.getRestrictedUrls();
        restrictedUrlsList.innerHTML = '';
        
        if (urls.length === 0) {
            restrictedUrlsList.innerHTML = '<p class="empty-message">暂无限制的网址</p>';
            return;
        }
        
        urls.forEach(url => {
            const urlItem = document.createElement('div');
            urlItem.className = 'url-item';
            urlItem.innerHTML = `
                <div class="url">${url}</div>
                <button class="remove-btn" data-url="${url}">×</button>
            `;
            restrictedUrlsList.appendChild(urlItem);
        });
        
        // 添加删除按钮事件
        document.querySelectorAll('.remove-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const url = e.target.getAttribute('data-url');
                await removeRestrictedUrl(url);
            });
        });
    } catch (error) {
        console.error('加载限制URL列表失败:', error);
        restrictedUrlsList.innerHTML = '<p class="error-message">加载失败</p>';
    }
}

// 移除限制的URL
async function removeRestrictedUrl(url) {
    try {
        const result = await window.electronAPI.removeRestrictedUrl(url);
        if (result.success) {
            showToast(result.message, 'success');
            loadRestrictedUrls();
        } else {
            showToast(result.message, 'error');
        }
    } catch (error) {
        showToast('移除限制URL失败', 'error');
        console.error('移除限制URL失败:', error);
    }
}

// 刷新访问日志
refreshLogBtn.addEventListener('click', loadAccessLog);

// 清空访问日志
clearLogBtn.addEventListener('click', () => {
    if (confirm('确定要清空所有访问日志吗？')) {
        // 这里应该调用清空日志的API
        // 目前只是一个占位符
        showToast('日志清空功能尚未实现', 'info');
    }
});

// 加载访问日志
async function loadAccessLog() {
    try {
        const logs = await window.electronAPI.getAccessLog(50);
        accessLogTable.innerHTML = '';
        
        if (logs.length === 0) {
            accessLogTable.innerHTML = '<tr><td colspan="3" class="empty-message">暂无访问记录</td></tr>';
            return;
        }
        
        logs.forEach(log => {
            const row = document.createElement('tr');
            const time = new Date(log.timestamp).toLocaleString();
            const statusClass = log.restricted ? 'blocked' : 'allowed';
            const statusText = log.restricted ? '已阻止' : '已允许';
            
            row.innerHTML = `
                <td>${time}</td>
                <td>${log.hostname}</td>
                <td><span class="status ${statusClass}">${statusText}</span></td>
            `;
            accessLogTable.appendChild(row);
        });
    } catch (error) {
        console.error('加载访问日志失败:', error);
        accessLogTable.innerHTML = '<tr><td colspan="3" class="error-message">加载失败</td></tr>';
    }
}

// 显示提示消息
function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}