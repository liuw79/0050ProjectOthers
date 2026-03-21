# DeepSeek 对话导出工具

批量导出 Deepseek 所有历史对话为 Markdown 文件。

## 安装

```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -e .

# 安装 Playwright 浏览器
playwright install chromium
```

## 使用

```bash
# 激活虚拟环境
source .venv/bin/activate

# 导出所有对话
deepseek-export

# 指定输出目录
deepseek-export -o ./my_exports

# 限制数量（测试用）
deepseek-export -n 5
```

## 流程

1. 工具打开 Deepseek 网页
2. 你手动登录（手机验证码或微信扫码）
3. 工具自动遍历并导出所有对话
4. 完成！

## 输出

所有对话保存在 `exports/` 目录，每个对话一个 `.md` 文件。

**文件格式示例：**

```markdown
# 对话标题

---
messages: 4
---

## User
你好

## Assistant
你好！有什么可以帮助你的？
```

## 注意事项

- 首次运行需要手动登录，登录状态会保存在 `browser_data/` 目录
- 几百条对话导出需要一定时间，请耐心等待
- 如果导出中断，可以重新运行，已导出的文件会被跳过（自动添加序号）
