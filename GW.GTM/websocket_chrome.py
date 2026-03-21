#!/usr/bin/env python3
import json
import subprocess
import time

def get_websocket_url():
    """获取Chrome页面的WebSocket URL"""
    try:
        result = subprocess.run([
            'curl', '-s', 'http://localhost:9222/json'
        ], capture_output=True, text=True)

        if result.returncode == 0:
            pages = json.loads(result.stdout)
            for page in pages:
                if 'google.com/search' in page.get('url', ''):
                    return page.get('webSocketDebuggerUrl')
        return None
    except:
        return None

def test_simple_websocket():
    """测试简单的WebSocket连接方法"""
    print("🔍 找到的问题:")
    print("1. ❌ 我之前使用的是HTTP API而不是WebSocket")
    print("2. ❌ 缺少执行上下文ID (executionContextId)")
    print("3. ❌ 没有先启用Runtime域")
    print("")

    ws_url = get_websocket_url()
    if ws_url:
        print(f"✅ 找到WebSocket URL: {ws_url}")
        print("")
        print("💡 正确的方法应该是:")
        print("1. 通过WebSocket连接到Chrome")
        print("2. 发送 Runtime.enable 命令")
        print("3. 获取执行上下文ID")
        print("4. 使用正确的executionContextId执行Runtime.evaluate")
        print("")
        print("🛠️ 由于没有WebSocket库，让我尝试一个替代方案...")
        return True
    else:
        print("❌ 未找到Google搜索页面的WebSocket URL")
        return False

def try_alternative_approach():
    """尝试替代方案：使用更简单的方法"""
    print("🔄 尝试替代方案：直接导航到包含JavaScript的URL...")

    # 创建一个包含JavaScript的data URL
    js_code = '''
    // 添加操控标记
    const marker = document.createElement('div');
    marker.innerHTML = '🤖 Claude AI 成功操控Chrome!';
    marker.style.cssText = `
        position: fixed !important;
        top: 20px !important;
        right: 20px !important;
        background: red !important;
        color: white !important;
        padding: 15px !important;
        border-radius: 10px !important;
        z-index: 999999 !important;
        font-size: 16px !important;
        font-weight: bold !important;
    `;
    document.body.appendChild(marker);

    // 高亮搜索结果
    const links = document.querySelectorAll('h3 a, .yuRUbf a');
    links.forEach(link => {
        link.style.cssText += `
            background: yellow !important;
            border: 3px solid red !important;
            padding: 5px !important;
            border-radius: 5px !important;
        `;
    });

    // 复制内容
    let copyText = '=== Chrome操控成功复制结果 ===\\n\\n';
    links.forEach((link, i) => {
        if (i < 10 && link.href && !link.href.includes('google.com/search')) {
            copyText += `${i+1}. ${link.textContent.trim()}\\n   ${link.href}\\n\\n`;
        }
    });

    // 执行复制
    const textarea = document.createElement('textarea');
    textarea.value = copyText;
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    document.body.appendChild(textarea);
    textarea.select();

    const success = document.execCommand('copy');
    document.body.removeChild(textarea);

    // 显示结果
    const result = document.createElement('div');
    result.innerHTML = success ? '✅ 复制成功!' : '⚠️ 复制可能失败';
    result.style.cssText = `
        position: fixed !important;
        top: 80px !important;
        right: 20px !important;
        background: green !important;
        color: white !important;
        padding: 15px !important;
        border-radius: 10px !important;
        z-index: 999999 !important;
    `;
    document.body.appendChild(result);

    setTimeout(() => result.remove(), 5000);

    alert('🎉 Chrome操控演示完成!\\n\\n✅ 已添加操控标记\\n✅ 已高亮搜索结果\\n✅ 已执行复制操作');
    '''.replace('\\n', '\\\\n').replace("'", "\\\\'")

    # 注入JavaScript到页面
    try:
        data_url = f"javascript:{js_code}"

        # 尝试通过Chrome创建新标签页执行JavaScript
        result = subprocess.run([
            'curl', '-s', '-X', 'PUT',
            f'http://localhost:9222/json/new?{data_url}'
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ 已发送JavaScript注入命令")
            print("📱 检查Chrome是否弹出了确认对话框")
            return True
        else:
            print(f"❌ 命令失败: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return False

def main():
    print("🔧 Chrome DevTools问题诊断和修复")
    print("=" * 50)

    if test_simple_websocket():
        print("🚀 尝试修复方案...")
        if try_alternative_approach():
            print("✅ 修复命令已发送!")
            print("")
            print("请检查Chrome浏览器中的Google搜索页面")
        else:
            print("❌ 修复尝试失败")

    print("")
    print("💡 总结:")
    print("• Chrome DevTools协议主要通过WebSocket工作")
    print("• HTTP API有限制，需要正确的执行上下文")
    print("• JavaScript注入是一个可行的替代方案")

if __name__ == "__main__":
    main()