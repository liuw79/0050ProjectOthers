#!/usr/bin/env python3
import json
import subprocess
import sys

def execute_js_in_chrome(page_id, js_code):
    """通过Chrome DevTools协议执行JavaScript"""
    # 创建WebSocket命令
    cmd_data = {
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {
            "expression": js_code,
            "returnByValue": True
        }
    }

    # 转换为curl命令
    json_data = json.dumps(cmd_data).replace('"', '\\"')

    curl_cmd = f'''
    curl -s -X POST "http://localhost:9222/json" \\
         -H "Content-Type: application/json" \\
         -d "{json_data}"
    '''

    try:
        result = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout:
            try:
                response = json.loads(result.stdout)
                if "result" in response and "value" in response["result"]:
                    return response["result"]["value"]
            except:
                pass
        return result.stdout
    except Exception as e:
        return f"错误: {e}"

def copy_to_clipboard(text):
    """复制文本到系统剪贴板"""
    try:
        # macOS
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
        return True
    except:
        try:
            # Linux
            process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            return True
        except:
            return False

def main():
    print("🔍 开始从Chrome浏览器中提取搜索结果...")

    # Google搜索结果页面ID
    page_id = "F86FF4AB11A81DD8824FC785E498333D"

    # JavaScript代码：提取搜索结果
    extract_js = '''
    (function() {
        const results = [];

        // 尝试不同的选择器来找到搜索结果
        const selectors = [
            'h3 a[href]',
            '.yuRUbf > a[href]',
            '.g .yuRUbf a',
            '.g h3 a',
            '[data-ved] h3 a',
            '.r > a',
            '.rc .r > a'
        ];

        let links = [];
        for (const selector of selectors) {
            links = document.querySelectorAll(selector);
            if (links.length > 0) {
                console.log('使用选择器: ' + selector + ', 找到 ' + links.length + ' 个链接');
                break;
            }
        }

        // 提取链接信息
        for (let i = 0; i < Math.min(10, links.length); i++) {
            const link = links[i];
            if (link.href && link.href.startsWith('http') && !link.href.includes('google.com/search')) {
                const title = link.textContent.trim() ||
                            link.querySelector('h3')?.textContent?.trim() ||
                            link.getAttribute('aria-label') ||
                            '无标题';

                if (title && title !== '无标题' && title.length > 3) {
                    results.push({
                        index: results.length + 1,
                        title: title,
                        url: link.href
                    });

                    // 高亮复制的链接
                    link.style.background = 'lightgreen';
                    link.style.border = '2px solid green';
                    link.style.padding = '3px';
                }
            }
        }

        // 也尝试备用方法
        if (results.length === 0) {
            const allLinks = document.querySelectorAll('a[href]');
            for (const link of allLinks) {
                if (link.href && link.href.match(/^https?:\\/\\//) &&
                    !link.href.includes('google.com') &&
                    !link.href.includes('googleusercontent.com') &&
                    link.textContent.trim().length > 10) {
                    results.push({
                        index: results.length + 1,
                        title: link.textContent.trim(),
                        url: link.href
                    });
                    if (results.length >= 10) break;
                }
            }
        }

        return {
            count: results.length,
            results: results,
            pageTitle: document.title,
            currentUrl: window.location.href
        };
    })();
    '''

    print(f"📄 从页面 {page_id} 执行JavaScript...")

    # 执行JavaScript
    result = execute_js_in_chrome(page_id, extract_js)

    if isinstance(result, str):
        try:
            data = json.loads(result)
            if "results" in data:
                results = data["results"]
                count = data.get("count", 0)

                print(f"✅ 成功提取 {count} 个搜索结果！")
                print(f"📄 页面标题: {data.get('pageTitle', '未知')}")
                print()

                # 格式化输出
                output_lines = []
                output_lines.append("=== 企业实战型商学院 - Google搜索结果 (前10条) ===")
                output_lines.append("")

                for item in results:
                    output_lines.append(f"{item['index']}. {item['title']}")
                    output_lines.append(f"   {item['url']}")
                    output_lines.append("")

                output_text = "\\n".join(output_lines)

                # 显示结果
                print("📋 提取的搜索结果:")
                print(output_text)

                # 复制到剪贴板
                print("\\n📎 正在复制到剪贴板...")
                if copy_to_clipboard(output_text):
                    print("✅ 已成功复制到剪贴板！")
                    print("💡 你现在可以在任何地方粘贴 (Cmd+V) 这些链接")
                else:
                    print("❌ 复制到剪贴板失败，但内容已显示在上方")

                return True
            else:
                print("❌ 未找到搜索结果数据")
                print(f"原始返回: {result}")
        except json.JSONDecodeError:
            print("❌ 解析JSON失败")
            print(f"原始返回: {result}")
    else:
        print(f"❌ 执行失败: {result}")

    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)