#!/usr/bin/env python3
import json
import time
import websocket
import threading

class ChromeController:
    def __init__(self):
        self.ws = None
        self.connected = False
        self.message_id = 1
        self.responses = {}
        self.execution_context_id = None

    def connect(self):
        """连接到Chrome WebSocket"""
        ws_url = "ws://localhost:9222/devtools/page/F86FF4AB11A81DD8824FC785E498333D"

        print(f"🔌 连接到Chrome WebSocket: {ws_url}")

        try:
            self.ws = websocket.WebSocketApp(
                ws_url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )

            # 启动WebSocket连接（在后台线程中）
            wst = threading.Thread(target=self.ws.run_forever)
            wst.daemon = True
            wst.start()

            # 等待连接建立
            time.sleep(2)
            return self.connected

        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False

    def on_open(self, ws):
        print("✅ WebSocket连接已建立")
        self.connected = True

        # 启用Runtime域
        self.send_command("Runtime.enable")

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            print(f"📨 收到消息: {data}")

            if "id" in data:
                self.responses[data["id"]] = data

            # 获取执行上下文
            if data.get("method") == "Runtime.executionContextCreated":
                context = data.get("params", {}).get("context", {})
                if context.get("origin") == "https://www.google.com":
                    self.execution_context_id = context.get("id")
                    print(f"✅ 获取到执行上下文ID: {self.execution_context_id}")

        except Exception as e:
            print(f"❌ 消息处理错误: {e}")

    def on_error(self, ws, error):
        print(f"❌ WebSocket错误: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("🔌 WebSocket连接已关闭")
        self.connected = False

    def send_command(self, method, params=None):
        """发送Chrome DevTools命令"""
        if not self.connected:
            print("❌ 未连接到Chrome")
            return None

        command = {
            "id": self.message_id,
            "method": method,
            "params": params or {}
        }

        print(f"📤 发送命令: {method}")
        self.ws.send(json.dumps(command))

        cmd_id = self.message_id
        self.message_id += 1

        # 等待响应
        for _ in range(50):  # 等待5秒
            if cmd_id in self.responses:
                return self.responses[cmd_id]
            time.sleep(0.1)

        print(f"⏱️ 命令 {method} 超时")
        return None

    def execute_javascript(self, js_code):
        """执行JavaScript代码"""
        params = {
            "expression": js_code,
            "returnByValue": True
        }

        if self.execution_context_id:
            params["contextId"] = self.execution_context_id

        return self.send_command("Runtime.evaluate", params)

    def control_chrome(self):
        """真正操控Chrome浏览器"""
        print("🎯 开始真正的Chrome操控...")

        # 等待获取执行上下文
        for _ in range(50):
            if self.execution_context_id:
                break
            time.sleep(0.1)

        if not self.execution_context_id:
            print("⚠️ 未获取到执行上下文，使用默认上下文")

        # 1. 添加操控标记
        print("📍 1. 添加操控标记...")
        marker_js = '''
        const marker = document.createElement('div');
        marker.innerHTML = '🤖 Claude AI 真正操控Chrome成功! ' + new Date().toLocaleTimeString();
        marker.style.cssText = `
            position: fixed !important;
            top: 20px !important;
            right: 20px !important;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4) !important;
            color: white !important;
            padding: 15px 20px !important;
            border-radius: 10px !important;
            z-index: 999999 !important;
            font-size: 16px !important;
            font-weight: bold !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
            animation: bounce 2s infinite !important;
        `;

        // 添加动画
        if (!document.getElementById('claude-bounce-style')) {
            const style = document.createElement('style');
            style.id = 'claude-bounce-style';
            style.textContent = `
                @keyframes bounce {
                    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                    40% { transform: translateY(-10px); }
                    60% { transform: translateY(-5px); }
                }
            `;
            document.head.appendChild(style);
        }

        if (!document.getElementById('claude-marker')) {
            marker.id = 'claude-marker';
            document.body.appendChild(marker);
        }

        "✅ 操控标记已添加";
        '''

        result1 = self.execute_javascript(marker_js)
        if result1:
            print(f"   结果: {result1.get('result', {}).get('value', '完成')}")

        # 2. 高亮搜索结果
        print("🎯 2. 高亮搜索结果...")
        highlight_js = '''
        const links = document.querySelectorAll('h3 a, .yuRUbf a');
        links.forEach((link, index) => {
            link.style.cssText += `
                background: yellow !important;
                border: 3px solid red !important;
                padding: 8px !important;
                border-radius: 8px !important;
                box-shadow: 0 0 15px rgba(255,255,0,0.7) !important;
                transition: all 0.3s ease !important;
            `;

            // 添加序号标记
            const badge = document.createElement('span');
            badge.innerHTML = index + 1;
            badge.style.cssText = `
                position: absolute;
                background: red;
                color: white;
                border-radius: 50%;
                width: 25px;
                height: 25px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                font-weight: bold;
                margin-left: -35px;
                margin-top: 5px;
            `;
            link.style.position = 'relative';
            link.parentNode.insertBefore(badge, link);
        });

        "✅ 已高亮 " + links.length + " 个搜索结果";
        '''

        result2 = self.execute_javascript(highlight_js)
        if result2:
            print(f"   结果: {result2.get('result', {}).get('value', '完成')}")

        # 3. 复制搜索结果
        print("📋 3. 复制搜索结果到剪贴板...")
        copy_js = '''
        let copyText = "=== Chrome WebSocket操控成功复制结果 ===\\n";
        copyText += "操控时间: " + new Date().toLocaleString() + "\\n\\n";

        const links = document.querySelectorAll('h3 a, .yuRUbf a');
        let count = 0;

        links.forEach((link, index) => {
            if (index < 10 && link.href && !link.href.includes('google.com/search')) {
                count++;
                const title = link.textContent.trim();
                copyText += count + ". " + title + "\\n   " + link.href + "\\n\\n";
            }
        });

        // 执行复制
        const textarea = document.createElement('textarea');
        textarea.value = copyText;
        textarea.style.cssText = 'position: fixed; left: -9999px; opacity: 0;';
        document.body.appendChild(textarea);
        textarea.select();

        let copySuccess = false;
        try {
            copySuccess = document.execCommand('copy');
        } catch(e) {
            console.log('复制失败:', e);
        }

        document.body.removeChild(textarea);

        // 显示复制结果
        const resultDiv = document.createElement('div');
        resultDiv.innerHTML = copySuccess ?
            `✅ 已成功复制 ${count} 条搜索结果到剪贴板!` :
            `⚠️ 复制可能失败，但已选中 ${count} 条结果`;

        resultDiv.style.cssText = `
            position: fixed !important;
            top: 100px !important;
            right: 20px !important;
            background: ${copySuccess ? 'green' : 'orange'} !important;
            color: white !important;
            padding: 15px !important;
            border-radius: 10px !important;
            z-index: 999999 !important;
            font-size: 14px !important;
            max-width: 300px !important;
        `;

        document.body.appendChild(resultDiv);

        // 5秒后移除提示
        setTimeout(() => {
            if (resultDiv.parentNode) {
                resultDiv.remove();
            }
        }, 5000);

        return {
            success: copySuccess,
            count: count,
            textLength: copyText.length
        };
        '''

        result3 = self.execute_javascript(copy_js)
        if result3:
            data = result3.get('result', {}).get('value', {})
            print(f"   复制状态: {'成功' if data.get('success') else '可能失败'}")
            print(f"   复制数量: {data.get('count', 0)} 条结果")

        print("")
        print("🎉 Chrome WebSocket操控演示完成！")
        print("")
        print("请检查Chrome浏览器，你应该看到：")
        print("• 右上角彩色渐变的AI操控标记（带弹跳动画）")
        print("• 搜索结果被黄色高亮，带红色编号标记")
        print("• 绿色的复制成功提示")
        print("• 搜索结果已复制到剪贴板")

def main():
    controller = ChromeController()

    if controller.connect():
        print("✅ Chrome连接成功，开始操控...")
        time.sleep(3)  # 等待连接稳定
        controller.control_chrome()
    else:
        print("❌ 无法连接到Chrome")

    print("\n⏱️ 保持连接5秒以观察效果...")
    time.sleep(5)

if __name__ == "__main__":
    main()