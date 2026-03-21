#!/usr/bin/env python3
import json
import subprocess
import time

def send_chrome_command(method, params=None):
    """发送Chrome DevTools命令"""
    if params is None:
        params = {}

    command = {
        "id": 1,
        "method": method,
        "params": params
    }

    # 转义JSON字符串
    json_str = json.dumps(command).replace('"', '\\"')

    curl_cmd = f'curl -s -X POST "http://localhost:9222/json" -H "Content-Type: application/json" -d "{json_str}"'

    try:
        result = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}

def main():
    print("🎯 真正开始通过Chrome DevTools操控浏览器...")
    print("📍 目标: Google搜索结果页面")
    print("")

    # 获取搜索结果页面
    print("🔍 1. 获取Chrome中的搜索结果页面...")

    # 执行JavaScript来操控页面
    print("🖱️ 2. 在Chrome中选择搜索结果...")

    # JavaScript代码：选择和复制搜索结果
    select_and_copy_js = '''
    (function() {
        // 查找搜索结果
        const searchResults = document.querySelectorAll('h3 a, .yuRUbf a');
        let selectedText = "=== 企业实战型商学院 - Chrome操控复制结果 ===\\n\\n";

        // 添加操控标记
        if (!document.getElementById('claude-control-marker')) {
            const marker = document.createElement('div');
            marker.id = 'claude-control-marker';
            marker.innerHTML = '🤖 Claude正在操控Chrome复制内容...';
            marker.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: red;
                color: white;
                padding: 15px;
                border-radius: 10px;
                z-index: 10000;
                font-size: 16px;
                font-weight: bold;
                animation: blink 1s infinite;
            `;
            document.head.insertAdjacentHTML('beforeend', `
                <style>
                    @keyframes blink {
                        0% { opacity: 1; }
                        50% { opacity: 0.5; }
                        100% { opacity: 1; }
                    }
                </style>
            `);
            document.body.appendChild(marker);
        }

        // 选择并高亮前10个搜索结果
        for (let i = 0; i < Math.min(10, searchResults.length); i++) {
            const link = searchResults[i];
            if (link.href && !link.href.includes('google.com/search')) {
                // 高亮选中的链接
                link.style.cssText += `
                    background: yellow !important;
                    border: 2px solid red !important;
                    padding: 5px !important;
                    animation: selectAnimation 0.5s ease-in-out !important;
                `;

                // 添加到选中文本
                selectedText += `${i + 1}. ${link.textContent.trim()}\\n   ${link.href}\\n\\n`;
            }
        }

        // 添加选择动画
        document.head.insertAdjacentHTML('beforeend', `
            <style>
                @keyframes selectAnimation {
                    0% { transform: scale(1); }
                    50% { transform: scale(1.05); }
                    100% { transform: scale(1); }
                }
            </style>
        `);

        // 创建临时文本区域来复制文本
        const textArea = document.createElement('textarea');
        textArea.value = selectedText;
        textArea.style.position = 'fixed';
        textArea.style.left = '-9999px';
        document.body.appendChild(textArea);

        // 选择文本
        textArea.select();
        textArea.setSelectionRange(0, 99999); // For mobile devices

        // 尝试复制到剪贴板
        let copySuccess = false;
        try {
            copySuccess = document.execCommand('copy');
        } catch(err) {
            console.log('复制命令失败:', err);
        }

        // 移除临时元素
        document.body.removeChild(textArea);

        // 显示复制结果
        const resultDiv = document.createElement('div');
        resultDiv.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: ${copySuccess ? 'green' : 'orange'};
            color: white;
            padding: 15px;
            border-radius: 10px;
            z-index: 10001;
            font-size: 14px;
            max-width: 300px;
        `;
        resultDiv.innerHTML = copySuccess ?
            '✅ 已成功复制到剪贴板!<br>包含10条搜索结果' :
            '⚠️ 复制可能失败，但内容已选中';

        document.body.appendChild(resultDiv);

        // 5秒后移除提示
        setTimeout(() => {
            if (resultDiv.parentNode) {
                resultDiv.parentNode.removeChild(resultDiv);
            }
        }, 5000);

        return {
            success: copySuccess,
            selectedCount: Math.min(10, searchResults.length),
            textLength: selectedText.length,
            preview: selectedText.substring(0, 200) + '...'
        };
    })();
    '''

    print("🔄 执行JavaScript操控命令...")

    # 发送命令到Chrome
    result = send_chrome_command("Runtime.evaluate", {
        "expression": select_and_copy_js,
        "returnByValue": True
    })

    if "error" in result:
        print(f"❌ 命令执行失败: {result['error']}")
    elif "result" in result and "value" in result["result"]:
        data = result["result"]["value"]
        print("✅ Chrome操控成功!")
        print(f"📊 选中结果数量: {data.get('selectedCount', 0)}")
        print(f"📝 文本长度: {data.get('textLength', 0)} 字符")
        print(f"📋 复制状态: {'成功' if data.get('success') else '可能失败'}")
        print("")
        print("🎯 现在请查看Chrome浏览器:")
        print("• 搜索结果应该被黄色高亮")
        print("• 右上角显示操控标记")
        print("• 显示复制状态提示")
        print("• 内容已尝试复制到剪贴板")

        if data.get('preview'):
            print("")
            print("📄 复制内容预览:")
            print(data['preview'])
    else:
        print("❌ 未收到有效响应")
        print(f"原始结果: {result}")

    print("")
    print("🎉 Chrome浏览器操控和复制演示完成！")

if __name__ == "__main__":
    main()