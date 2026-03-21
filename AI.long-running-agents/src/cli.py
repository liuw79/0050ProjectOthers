# src/cli.py
import click
from rich.console import Console

console = Console()

@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """长运行代理开发系统 - 用自然语言驱动开发

    快速开始:
        long-agents "帮我创建一个用户管理 API"
        long-agents "查看状态"
        long-agents "继续开发"
    """
    if ctx.invoked_subcommand is None:
        # 没有子命令时，显示帮助
        console.print("[bold cyan]长运行代理开发系统[/bold cyan]")
        console.print("\n[yellow]用法示例:[/yellow]")
        console.print('  long-agents "帮我创建一个用户管理 API"')
        console.print('  long-agents "查看项目状态"')
        console.print('  long-agents "继续开发下一个功能"')
        console.print("\n[yellow]命令列表:[/yellow]")
        console.print("  init      初始化新项目")
        console.print("  status    查看项目状态")
        console.print("  coder     运行编码代理")
        console.print("\n[dim]运行 long-agents --help 查看更多[/dim]")

# 导入命令
from src.commands.init import init
from src.commands.status import status
from src.commands.initializer_cmd import run as initializer_run
from src.commands.coder_cmd import run as coder_run
from src.commands.dashboard import dashboard
from src.commands.ask import ask, list_projects

main.add_command(init)
main.add_command(status)
main.add_command(initializer_run, name="initializer")
main.add_command(coder_run, name="coder")
main.add_command(dashboard)
main.add_command(ask)
main.add_command(list_projects, name="projects")

if __name__ == "__main__":
    main()
