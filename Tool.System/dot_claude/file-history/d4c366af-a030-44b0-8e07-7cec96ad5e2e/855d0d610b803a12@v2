# DeepSeek 对话导出工具实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 创建一个命令行工具，自动批量导出 Deepseek 所有历史对话为 Markdown 文件。

**Architecture:** 使用 Playwright 浏览器自动化访问 Deepseek 网页版，等待用户手动登录后，遍历对话列表并逐个抓取内容保存为 MD 文件。

**Tech Stack:** Python 3.10+, Playwright, asyncio, rich (进度显示)

---

## Task 1: 项目初始化

**Files:**
- Create: `pyproject.toml`
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `src/deepseek_export/__init__.py`

**Step 1: 创建项目目录结构**

```bash
mkdir -p src/deepseek_export exports tests
```

**Step 2: 创建 pyproject.toml**

```toml
[project]
name = "deepseek-export"
version = "0.1.0"
description = "Export DeepSeek chat history to Markdown"
requires-python = ">=3.10"
dependencies = [
    "playwright>=1.40.0",
    "rich>=13.0.0",
]

[project.scripts]
deepseek-export = "deepseek_export.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Step 3: 创建 requirements.txt**

```
playwright>=1.40.0
rich>=13.0.0
```

**Step 4: 创建 .gitignore**

```
__pycache__/
*.py[cod]
.env
exports/
.venv/
*.egg-info/
.pytest_cache/
```

**Step 5: 创建 __init__.py**

```python
"""DeepSeek Chat Export Tool"""

__version__ = "0.1.0"
```

**Step 6: 初始化 git 并提交**

```bash
cd /Users/comdir/SynologyDrive/0050Project/Tool.DeepSeek
git init
git add .
git commit -m "chore: init project structure"
```

---

## Task 2: 探索 Deepseek 网页 DOM 结构

**Files:**
- Create: `scripts/explore_dom.py`

**Step 1: 创建 DOM 探索脚本**

```python
"""探索 Deepseek 网页 DOM 结构的辅助脚本"""
import asyncio
from playwright.async_api import async_playwright

async def explore():
    async with async_playwright() as p:
        # 使用持久化上下文，保留登录状态
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="./browser_data",
            headless=False
        )
        page = browser.pages[0]

        # 导航到 Deepseek
        await page.goto("https://chat.deepseek.com/")
        print("请在浏览器中登录 Deepseek...")
        print("登录完成后，按 Enter 继续...")
        input()

        # 获取对话列表
        print("\n=== 探索对话列表 ===")
        # 这里需要实际查看 DOM 来确定选择器
        # 先截图保存
        await page.screenshot(path="screenshots/homepage.png")

        # 尝试查找对话列表元素
        html = await page.content()
        with open("screenshots/homepage.html", "w") as f:
            f.write(html)

        print("已保存截图和 HTML 到 screenshots/ 目录")
        print("请查看并分析 DOM 结构")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(explore())
```

**Step 2: 运行探索脚本**

```bash
mkdir -p screenshots
python scripts/explore_dom.py
```

**注意:** 这一步需要用户配合登录，运行后分析 screenshots/ 目录中的 HTML 来确定正确的选择器。

---

## Task 3: 实现浏览器操作模块

**Files:**
- Create: `src/deepseek_export/browser.py`
- Create: `tests/test_browser.py`

**Step 1: 写测试（先确定选择器后补充）**

```python
# tests/test_browser.py
"""浏览器模块测试 - 需要实际 DOM 结构后完善"""
import pytest

def test_placeholder():
    """占位测试，DOM 探索后完善"""
    assert True
```

**Step 2: 实现浏览器模块**

```python
"""Playwright 浏览器操作封装"""
import asyncio
from pathlib import Path
from typing import Optional
from playwright.async_api import async_playwright, Page, BrowserContext


class DeepSeekBrowser:
    """Deepseek 网页操作封装"""

    BASE_URL = "https://chat.deepseek.com"

    # 选择器（DOM 探索后更新）
    SELECTORS = {
        "chat_list": "[data-testid='chat-list']",  # 待确认
        "chat_item": "[data-testid='chat-item']",  # 待确认
        "chat_title": ".chat-title",  # 待确认
        "message_container": ".message-list",  # 待确认
        "message_user": ".message.user",  # 待确认
        "message_assistant": ".message.assistant",  # 待确认
        "new_chat_btn": "[data-testid='new-chat']",  # 待确认
    }

    def __init__(self, user_data_dir: str = "./browser_data", headless: bool = False):
        self.user_data_dir = Path(user_data_dir)
        self.headless = headless
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def start(self):
        """启动浏览器"""
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self._playwright = await async_playwright().start()
        self.context = await self._playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.user_data_dir),
            headless=self.headless
        )
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()

    async def close(self):
        """关闭浏览器"""
        if self.context:
            await self.context.close()
        if hasattr(self, '_playwright'):
            await self._playwright.stop()

    async def goto_home(self):
        """导航到 Deepseek 首页"""
        await self.page.goto(self.BASE_URL)
        await self.page.wait_for_load_state("networkidle")

    async def wait_for_login(self) -> bool:
        """等待用户登录，返回是否登录成功"""
        # 检测登录状态的方式需要 DOM 探索后确定
        # 暂时用简单的元素检测
        try:
            # 等待对话列表出现（登录后的标志）
            await self.page.wait_for_selector(self.SELECTORS["chat_list"], timeout=300000)  # 5分钟超时
            return True
        except Exception:
            return False

    async def get_chat_list(self) -> list[dict]:
        """获取对话列表"""
        # 返回 [{"id": "...", "title": "..."}, ...]
        chat_items = await self.page.query_selector_all(self.SELECTORS["chat_item"])
        chats = []
        for item in chat_items:
            # 提取对话 ID 和标题
            # 具体实现需要 DOM 探索后确定
            pass
        return chats

    async def open_chat(self, chat_id: str):
        """打开指定对话"""
        # 实现需要 DOM 探索后确定
        pass

    async def get_chat_content(self) -> list[dict]:
        """获取当前对话内容"""
        # 返回 [{"role": "user/assistant", "content": "..."}, ...]
        messages = []
        # 具体实现需要 DOM 探索后确定
        return messages

    async def scroll_to_load_all_messages(self):
        """滚动加载所有消息"""
        # 如果对话很长，需要滚动加载
        pass
```

**Step 3: 运行测试验证模块可导入**

```bash
cd /Users/comdir/SynologyDrive/0050Project/Tool.DeepSeek
python -c "from deepseek_export.browser import DeepSeekBrowser; print('OK')"
```

**Step 4: 提交**

```bash
git add src/deepseek_export/browser.py tests/test_browser.py
git commit -m "feat: add browser module skeleton"
```

---

## Task 4: 实现内容解析和导出模块

**Files:**
- Create: `src/deepseek_export/parser.py`
- Create: `src/deepseek_export/exporter.py`
- Create: `tests/test_exporter.py`

**Step 1: 实现 MD 导出器**

```python
"""Markdown 导出器"""
import re
from pathlib import Path
from datetime import datetime
from typing import Optional


def sanitize_filename(title: str) -> str:
    """清理文件名，移除非法字符"""
    # 移除不允许出现在文件名中的字符
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    # 移除首尾空格
    title = title.strip()
    # 限制长度
    if len(title) > 100:
        title = title[:100]
    # 如果为空，使用时间戳
    if not title:
        title = f"untitled-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return title


def format_markdown(
    title: str,
    messages: list[dict],
    created_at: Optional[datetime] = None,
    message_count: Optional[int] = None
) -> str:
    """格式化为 Markdown"""
    lines = [f"# {title}", ""]

    # 元数据
    if created_at or message_count:
        lines.append("---")
        if created_at:
            lines.append(f"created: {created_at.strftime('%Y-%m-%d %H:%M')}")
        if message_count:
            lines.append(f"messages: {message_count}")
        lines.append("---")
        lines.append("")

    # 对话内容
    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        role_display = "## User" if role == "user" else "## Assistant"
        lines.append(role_display)
        lines.append("")
        lines.append(content)
        lines.append("")

    return "\n".join(lines)


def export_to_file(
    output_dir: Path,
    title: str,
    messages: list[dict],
    created_at: Optional[datetime] = None,
    overwrite: bool = False
) -> Path:
    """导出为 MD 文件"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = sanitize_filename(title) + ".md"
    filepath = output_dir / filename

    # 处理重名
    if filepath.exists() and not overwrite:
        counter = 1
        while filepath.exists():
            filepath = output_dir / f"{sanitize_filename(title)}-{counter}.md"
            counter += 1

    content = format_markdown(
        title=title,
        messages=messages,
        created_at=created_at,
        message_count=len(messages)
    )

    filepath.write_text(content, encoding="utf-8")
    return filepath
```

**Step 2: 写测试**

```python
# tests/test_exporter.py
import pytest
from pathlib import Path
from deepseek_export.exporter import sanitize_filename, format_markdown, export_to_file


def test_sanitize_filename():
    assert sanitize_filename("hello world") == "hello world"
    assert sanitize_filename('test<>:"/\\|?*name') == "testname"
    assert sanitize_filename("   spaced   ") == "spaced"
    assert sanitize_filename("")  # 应该返回时间戳


def test_format_markdown():
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
    ]
    result = format_markdown("Test Chat", messages)
    assert "# Test Chat" in result
    assert "## User" in result
    assert "## Assistant" in result
    assert "Hello" in result
    assert "Hi there!" in result


def test_export_to_file(tmp_path):
    messages = [
        {"role": "user", "content": "Test"},
    ]
    filepath = export_to_file(tmp_path, "Test Chat", messages)
    assert filepath.exists()
    assert filepath.name == "Test Chat.md"
    content = filepath.read_text()
    assert "# Test Chat" in content
```

**Step 3: 运行测试**

```bash
pytest tests/test_exporter.py -v
```

**Step 4: 提交**

```bash
git add src/deepseek_export/exporter.py tests/test_exporter.py
git commit -m "feat: add markdown exporter"
```

---

## Task 5: 实现主程序入口

**Files:**
- Create: `src/deepseek_export/main.py`

**Step 1: 实现主程序**

```python
"""DeepSeek 对话导出工具主入口"""
import asyncio
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Confirm

from .browser import DeepSeekBrowser
from .exporter import export_to_file


console = Console()


async def export_all_chats(
    output_dir: str = "./exports",
    headless: bool = False,
    limit: Optional[int] = None
):
    """导出所有对话"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    console.print("[bold blue]DeepSeek 对话导出工具[/bold blue]")
    console.print(f"输出目录: {output_path.absolute()}")

    async with DeepSeekBrowser(headless=headless) as browser:
        # 1. 导航到首页
        console.print("\n[ yellow]正在打开 Deepseek...[/yellow]")
        await browser.goto_home()

        # 2. 等待登录
        console.print("\n[yellow]请在浏览器中登录 Deepseek...[/yellow]")
        console.print("[dim]登录成功后将自动继续[/dim]")

        logged_in = await browser.wait_for_login()
        if not logged_in:
            console.print("[red]登录超时，请重试[/red]")
            return

        console.print("[green]登录成功！[/green]")

        # 3. 获取对话列表
        console.print("\n[yellow]正在获取对话列表...[/yellow]")
        chats = await browser.get_chat_list()

        if limit:
            chats = chats[:limit]

        console.print(f"[green]找到 {len(chats)} 个对话[/green]")

        if not chats:
            console.print("[yellow]没有找到对话[/yellow]")
            return

        # 4. 确认导出
        if not Confirm.ask(f"\n确认导出 {len(chats)} 个对话？"):
            console.print("[yellow]已取消[/yellow]")
            return

        # 5. 逐个导出
        success_count = 0
        fail_count = 0

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("导出中...", total=len(chats))

            for i, chat in enumerate(chats):
                try:
                    progress.update(task, description=f"导出: {chat['title'][:30]}...")

                    # 打开对话
                    await browser.open_chat(chat["id"])

                    # 获取内容
                    messages = await browser.get_chat_content()

                    # 保存文件
                    export_to_file(
                        output_dir=output_path,
                        title=chat["title"],
                        messages=messages
                    )

                    success_count += 1
                except Exception as e:
                    console.print(f"[red]导出失败: {chat['title']} - {e}[/red]")
                    fail_count += 1

                progress.advance(task)

        # 6. 完成统计
        console.print("\n" + "=" * 50)
        console.print(f"[bold green]导出完成！[/bold green]")
        console.print(f"成功: {success_count} | 失败: {fail_count}")
        console.print(f"文件保存在: {output_path.absolute()}")


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="导出 DeepSeek 对话历史")
    parser.add_argument(
        "-o", "--output",
        default="./exports",
        help="输出目录 (默认: ./exports)"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="无头模式（不显示浏览器窗口）"
    )
    parser.add_argument(
        "-n", "--limit",
        type=int,
        help="限制导出数量（用于测试）"
    )

    args = parser.parse_args()

    try:
        asyncio.run(export_all_chats(
            output_dir=args.output,
            headless=args.headless,
            limit=args.limit
        ))
    except KeyboardInterrupt:
        console.print("\n[yellow]用户中断[/yellow]")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**Step 2: 提交**

```bash
git add src/deepseek_export/main.py
git commit -m "feat: add main entry point"
```

---

## Task 6: DOM 探索并完善选择器

**说明:** 这一步需要在实际运行后，根据 Deepseek 网页的真实 DOM 结构来完善 `browser.py` 中的选择器。

**步骤:**
1. 运行 `scripts/explore_dom.py`
2. 分析 `screenshots/homepage.html` 确定选择器
3. 更新 `browser.py` 中的 `SELECTORS` 字典
4. 实现 `get_chat_list()`、`open_chat()`、`get_chat_content()` 方法
5. 测试验证

---

## Task 7: 安装 Playwright 浏览器

**Step 1: 安装项目依赖**

```bash
cd /Users/comdir/SynologyDrive/0050Project/Tool.DeepSeek
pip install -e .
```

**Step 2: 安装 Playwright 浏览器**

```bash
playwright install chromium
```

---

## Task 8: 创建 README

**Files:**
- Create: `README.md`

**Step 1: 写 README**

```markdown
# DeepSeek 对话导出工具

批量导出 Deepseek 所有历史对话为 Markdown 文件。

## 安装

```bash
pip install -e .
playwright install chromium
```

## 使用

```bash
# 导出所有对话
deepseek-export

# 指定输出目录
deepseek-export -o ./my_exports

# 限制数量（测试用）
deepseek-export -n 5
```

## 流程

1. 工具打开 Deepseek 网页
2. 你手动登录
3. 工具自动遍历并导出所有对话
4. 完成！

## 输出

所有对话保存在 `exports/` 目录，每个对话一个 `.md` 文件。
```

**Step 2: 提交**

```bash
git add README.md
git commit -m "docs: add README"
```

---

## 执行顺序

1. **Task 1** - 项目初始化
2. **Task 7** - 安装依赖（提前做，方便后续测试）
3. **Task 2** - DOM 探索
4. **Task 3** - 浏览器模块（根据 Task 2 结果完善）
5. **Task 4** - 导出模块
6. **Task 5** - 主程序
7. **Task 6** - 完善选择器（迭代）
8. **Task 8** - README
