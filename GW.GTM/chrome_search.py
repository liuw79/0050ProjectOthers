#!/usr/bin/env python3
import json
import requests
import time

# Chrome页面ID
page_id = "3A82DB4F2BD93473F7B7C21F9B9E35D2"
base_url = f"http://localhost:9222"

def send_command(method, params=None):
    """发送Chrome DevTools协议命令"""
    if params is None:
        params = {}

    # 使用Runtime.evaluate来执行JavaScript
    if method == "evaluate":
        url = f"{base_url}/json/runtime/evaluate"
        data = {
            "expression": params.get("expression", ""),
            "returnByValue": True
        }
    else:
        url = f"{base_url}/json"
        data = {
            "method": method,
            "params": params
        }

    try:
        # 对于简单操作，我们直接使用HTTP API
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"HTTP错误: {response.status_code}")
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def main():
    print("开始自动化Google搜索...")

    # 等待页面加载
    print("等待页面加载...")
    time.sleep(3)

    # 使用JavaScript直接操作页面
    search_script = """
    // 查找搜索框
    const searchInput = document.querySelector('input[name="q"]') ||
                       document.querySelector('input[title*="搜索"]') ||
                       document.querySelector('textarea[name="q"]') ||
                       document.querySelector('input[type="text"]');

    if (searchInput) {
        // 设置搜索词
        searchInput.value = '企业实战型商学院';
        searchInput.focus();

        // 触发搜索（模拟回车键）
        const event = new KeyboardEvent('keydown', {
            key: 'Enter',
            code: 'Enter',
            keyCode: 13,
            which: 13
        });
        searchInput.dispatchEvent(event);

        console.log('搜索已执行');
        return '搜索词已输入并执行';
    } else {
        return '未找到搜索框';
    }
    """

    # 执行搜索
    print("输入搜索词并执行搜索...")
    result = send_command("evaluate", {"expression": search_script})

    if result:
        print("搜索脚本执行结果:", result)

    # 等待搜索结果加载
    print("等待搜索结果加载...")
    time.sleep(5)

    # 提取搜索结果
    extract_script = """
    const results = [];
    const links = document.querySelectorAll('h3 a, .yuRUbf a, [data-ved] h3 a');

    for (let i = 0; i < Math.min(10, links.length); i++) {
        const link = links[i];
        if (link.href && link.href.startsWith('http') && link.textContent.trim()) {
            results.push({
                index: i + 1,
                title: link.textContent.trim(),
                url: link.href
            });
        }
    }

    console.log('找到', results.length, '个搜索结果');
    JSON.stringify(results);
    """

    print("提取搜索结果...")
    result = send_command("evaluate", {"expression": extract_script})

    if result:
        try:
            search_results = json.loads(result.get('result', {}).get('value', '[]'))
            print("\n=== 企业实战型商学院 - 前10条搜索结果 ===\n")

            for item in search_results:
                print(f"{item['index']}. {item['title']}")
                print(f"   {item['url']}\n")

            if not search_results:
                print("未能提取到搜索结果，可能页面结构发生变化")

        except Exception as e:
            print(f"解析搜索结果失败: {e}")

    print("搜索完成！")

if __name__ == "__main__":
    main()