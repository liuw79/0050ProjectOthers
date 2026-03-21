"""DeepSeek 对话导出工具主入口"""
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Confirm

from .browser import DeepSeekBrowser
from .exporter import export_to_file


console = Console()

# 增量导出记录文件
EXPORT_RECORD_FILE = "exported_chats.json"


def load_exported_records(output_path: Path) -> dict:
    """加载已导出的记录"""
    record_file = output_path / EXPORT_RECORD_FILE
    if record_file.exists():
        return json.loads(record_file.read_text(encoding="utf-8"))
    return {}


def save_exported_records(output_path: Path, records: dict):
    """保存导出记录"""
    record_file = output_path / EXPORT_RECORD_FILE
    record_file.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


async def export_all_chats(
    output_dir: str = "./exports",
    headless: bool = False,
    limit: Optional[int] = None,
    yes: bool = False,
    force: bool = False
):
    """导出所有对话"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    console.print("[bold blue]DeepSeek 对话导出工具[/bold blue]")
    console.print(f"输出目录: {output_path.absolute()}")

    # 加载已导出记录
    exported_records = load_exported_records(output_path)
    exported_count = len(exported_records)
    if exported_count > 0 and not force:
        console.print(f"[dim]已有 {exported_count} 条导出记录[/dim]")

    async with DeepSeekBrowser(headless=headless) as browser:
        console.print("\n[yellow]正在打开 Deepseek...[/yellow]")
        await browser.goto_home()

        console.print("\n[yellow]请在浏览器中登录 Deepseek...[/yellow]")
        console.print("[dim]登录成功后将自动继续[/dim]")

        logged_in = await browser.wait_for_login()
        if not logged_in:
            console.print("[red]登录超时，请重试[/red]")
            return

        console.print("[green]登录成功！[/green]")

        console.print("\n[yellow]正在获取对话列表...[/yellow]")
        chats = await browser.get_chat_list()

        if limit:
            chats = chats[:limit]

        console.print(f"[green]找到 {len(chats)} 个对话[/green]")

        # 过滤已导出的对话
        if not force:
            original_count = len(chats)
            chats = [c for c in chats if c["id"] not in exported_records]
            skipped_count = original_count - len(chats)
            if skipped_count > 0:
                console.print(f"[cyan]跳过 {skipped_count} 条已导出的对话[/cyan]")

        if not chats:
            console.print("[yellow]没有新的对话需要导出[/yellow]")
            return

        console.print(f"[green]需要导出 {len(chats)} 条新对话[/green]")

        if not yes and not Confirm.ask(f"\n确认导出 {len(chats)} 个对话？"):
            console.print("[yellow]已取消[/yellow]")
            return

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
                    await browser.open_chat(chat["id"])
                    messages = await browser.get_chat_content()

                    export_to_file(
                        output_dir=output_path,
                        title=chat["title"],
                        messages=messages
                    )

                    # 记录已导出
                    exported_records[chat["id"]] = {
                        "title": chat["title"],
                        "exported_at": datetime.now().isoformat(),
                        "message_count": len(messages)
                    }

                    # 每 10 条保存一次记录
                    if success_count % 10 == 0:
                        save_exported_records(output_path, exported_records)

                    success_count += 1
                except Exception as e:
                    console.print(f"[red]导出失败: {chat['title']} - {e}[/red]")
                    fail_count += 1

                progress.advance(task)

        # 最终保存记录
        save_exported_records(output_path, exported_records)

        console.print("\n" + "=" * 50)
        console.print(f"[bold green]导出完成！[/bold green]")
        console.print(f"本次成功: {success_count} | 失败: {fail_count}")
        console.print(f"累计导出: {len(exported_records)} 条")
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
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="跳过确认，直接导出"
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="强制重新导出（忽略已导出记录）"
    )

    args = parser.parse_args()

    try:
        asyncio.run(export_all_chats(
            output_dir=args.output,
            headless=args.headless,
            limit=args.limit,
            yes=args.yes,
            force=args.force
        ))
    except KeyboardInterrupt:
        console.print("\n[yellow]用户中断[/yellow]")
        sys.exit(1)


if __name__ == "__main__":
    main()
