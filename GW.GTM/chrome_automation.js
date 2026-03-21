const WebSocket = require('ws');

// Chrome页面ID
const pageId = '3A82DB4F2BD93473F7B7C21F9B9E35D2';
const wsUrl = `ws://localhost:9222/devtools/page/${pageId}`;

console.log('连接到Chrome DevTools WebSocket...');
const ws = new WebSocket(wsUrl);

let messageId = 1;

function sendCommand(method, params = {}) {
    return new Promise((resolve, reject) => {
        const id = messageId++;
        const message = JSON.stringify({ id, method, params });

        console.log(`发送命令: ${method}`);

        const timeout = setTimeout(() => {
            reject(new Error('命令超时'));
        }, 10000);

        function handleMessage(data) {
            const response = JSON.parse(data);
            if (response.id === id) {
                clearTimeout(timeout);
                ws.removeListener('message', handleMessage);
                if (response.error) {
                    reject(new Error(response.error.message));
                } else {
                    resolve(response.result);
                }
            }
        }

        ws.on('message', handleMessage);
        ws.send(message);
    });
}

ws.on('open', async () => {
    try {
        console.log('WebSocket连接成功！');

        // 启用Runtime和DOM域
        await sendCommand('Runtime.enable');
        await sendCommand('DOM.enable');

        console.log('等待页面加载...');
        await new Promise(resolve => setTimeout(resolve, 3000));

        // 获取文档
        const doc = await sendCommand('DOM.getDocument');
        console.log('获取到文档');

        // 查找搜索框
        const searchInput = await sendCommand('DOM.querySelector', {
            nodeId: doc.root.nodeId,
            selector: 'input[name="q"], input[title*="搜索"], textarea[name="q"]'
        });

        if (searchInput.nodeId === 0) {
            console.log('未找到搜索框，尝试其他选择器...');
            // 尝试其他可能的选择器
            const altSearch = await sendCommand('DOM.querySelector', {
                nodeId: doc.root.nodeId,
                selector: 'input[type="text"]'
            });

            if (altSearch.nodeId === 0) {
                throw new Error('找不到搜索框');
            }
            console.log('找到搜索框！');
        } else {
            console.log('找到Google搜索框！');
        }

        const inputNodeId = searchInput.nodeId || altSearch.nodeId;

        // 点击搜索框获得焦点
        console.log('点击搜索框...');
        await sendCommand('DOM.focus', { nodeId: inputNodeId });

        // 输入搜索词
        console.log('输入搜索词: 企业实战型商学院');
        await sendCommand('Input.insertText', { text: '企业实战型商学院' });

        // 按Enter键搜索
        console.log('按Enter键执行搜索...');
        await sendCommand('Input.dispatchKeyEvent', {
            type: 'keyDown',
            key: 'Enter',
            code: 'Enter',
            keyCode: 13
        });

        await sendCommand('Input.dispatchKeyEvent', {
            type: 'keyUp',
            key: 'Enter',
            code: 'Enter',
            keyCode: 13
        });

        // 等待搜索结果加载
        console.log('等待搜索结果加载...');
        await new Promise(resolve => setTimeout(resolve, 5000));

        // 获取搜索结果链接
        console.log('提取搜索结果...');
        const result = await sendCommand('Runtime.evaluate', {
            expression: `
                Array.from(document.querySelectorAll('h3 a, .yuRUbf a')).slice(0, 10).map((link, index) => {
                    return {
                        index: index + 1,
                        title: link.textContent.trim(),
                        url: link.href
                    };
                })
            `,
            returnByValue: true
        });

        console.log('\\n=== 搜索结果 ===');
        result.value.forEach(item => {
            console.log(`${item.index}. ${item.title}`);
            console.log(`   ${item.url}\\n`);
        });

        console.log('搜索完成！');

    } catch (error) {
        console.error('操作失败:', error.message);
    } finally {
        ws.close();
    }
});

ws.on('error', (error) => {
    console.error('WebSocket错误:', error);
});

ws.on('close', () => {
    console.log('WebSocket连接已关闭');
});