import click
import re
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()

# 默认项目目录
DEFAULT_PROJECT_DIR = Path.home() / "SynologyDrive" / "0050Project"

# 前缀及其用途
PREFIXES = {
    "AI": "AI/机器学习项目",
    "GW": "高维业务项目",
    "Tool": "工具类项目",
    "Game": "游戏项目",
    "Learn": "学习/教学项目",
    "GitHub": "GitHub 相关项目",
}


def find_current_project() -> Path:
    """查找当前目录所属的项目"""
    current = Path.cwd()
    while current != current.parent:
        config_file = current / "long-agents.yaml"
        if config_file.exists():
            return current
        current = current.parent
    return None


def parse_intent(text: str) -> dict:
    """解析用户意图"""
    text_lower = text.lower()

    # 列出项目
    if any(w in text_lower for w in ["项目列表", "所有项目", "哪些项目", "list"]):
        return {"action": "list", "text": text}

    # 创建新项目
    create_patterns = [
        r"创建?.*项目",
        r"新建?.*项目",
        r"帮我?(创建|建|做|写)",
        r"开始?(一个)?项目",
    ]
    for pattern in create_patterns:
        if re.search(pattern, text_lower):
            return {"action": "create", "text": text}

    # 查看状态
    status_patterns = ["状态", "进度", "怎么样", "完成.*多少"]
    for pattern in status_patterns:
        if re.search(pattern, text_lower):
            return {"action": "status", "text": text}

    # 继续开发
    continue_patterns = ["继续", "开发", "实现", "写代码", "运行", "下一个"]
    for pattern in continue_patterns:
        if re.search(pattern, text_lower):
            return {"action": "code", "text": text}

    # 默认：如果是项目描述，就创建项目
    if any(word in text_lower for word in ["api", "网站", "应用", "系统", "服务", "工具", "rest", "crud", "博客", "商城", "管理"]):
        return {"action": "create", "text": text}

    return {"action": "unknown", "text": text}


def extract_project_from_text(text: str, registry) -> tuple:
    """从文本中提取项目名，返回 (项目名, 项目信息)"""
    from src.core.project_registry import ProjectInfo

    projects = registry.list_all()
    if not projects:
        return None, None

    text_lower = text.lower()

    # 尝试匹配项目名
    for project in projects:
        # 完整名称匹配 (如 "GW.Blog")
        if project.name.lower() in text_lower:
            return project.name, project
        # 部分名称匹配 (如 "blog")
        name_part = project.name.split(".")[-1].lower()
        if name_part in text_lower and len(name_part) > 2:
            return project.name, project

    return None, None


def select_project(registry, prompt_text: str = "选择项目") -> tuple:
    """让用户选择一个项目，返回 (项目名, 项目信息)"""
    from src.core.project_registry import ProjectInfo

    projects = registry.list_all()

    if not projects:
        console.print("[yellow]还没有注册的项目[/yellow]")
        console.print('先创建一个: long-agents "创建一个 XX 项目"')
        return None, None

    console.print(f"\n[bold cyan]{prompt_text}:[/bold cyan]")

    for i, p in enumerate(projects, 1):
        desc = f" - {p.description[:30]}..." if p.description and len(p.description) > 30 else f" - {p.description}" if p.description else ""
        console.print(f"  [yellow]{i}[/yellow]. {p.name}{desc}")

    console.print(f"  [yellow]c[/yellow]. 取消")

    choice = Prompt.ask("\n选择", default="1")

    if choice.lower() == 'c':
        return None, None

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(projects):
            project = projects[idx]
            return project.name, project
    except:
        pass

    return projects[0].name, projects[0] if projects else (None, None)


def extract_keywords(text: str) -> list:
    """从描述中提取关键词"""
    text_lower = text.lower()

    keywords_map = {
        "博客": "Blog", "blog": "Blog",
        "商城": "Shop", "shop": "Shop",
        "用户": "User", "user": "User",
        "管理": "Admin", "manage": "Admin",
        "系统": "System", "system": "System",
        "工具": "Tool", "tool": "Tool",
        "数据": "Data", "data": "Data",
        "分析": "Analytics", "analysis": "Analytics",
        "接口": "API", "api": "API",
        "网站": "Web", "web": "Web",
        "应用": "App", "app": "App",
        "游戏": "Game", "game": "Game",
        "学习": "Learn", "learn": "Learn",
        "知识": "Knowledge", "knowledge": "Knowledge",
    }

    found = []
    for keyword, name in keywords_map.items():
        if keyword in text_lower and name not in found:
            found.append(name)

    return found if found else ["Project"]


def generate_name_suggestions(text: str) -> list:
    """生成项目名建议"""
    keywords = extract_keywords(text)
    text_lower = text.lower()

    # 判断项目类型
    if any(w in text_lower for w in ["ai", "机器学习", "llm", "gpt", "agent", "智能"]):
        primary_prefix = "AI"
    elif any(w in text_lower for w in ["工具", "tool", "辅助", "批量"]):
        primary_prefix = "Tool"
    elif any(w in text_lower for w in ["游戏", "game", "玩"]):
        primary_prefix = "Game"
    elif any(w in text_lower for w in ["学习", "learn", "课", "教程"]):
        primary_prefix = "Learn"
    elif any(w in text_lower for w in ["github", "开源"]):
        primary_prefix = "GitHub"
    else:
        primary_prefix = "GW"

    suggestions = []
    for name in keywords[:2]:
        suggestions.append(f"{primary_prefix}.{name}")

    secondary_prefix = "Tool" if primary_prefix != "Tool" else "GW"
    if keywords:
        suggestions.append(f"{secondary_prefix}.{keywords[0]}")

    if len(suggestions) < 3:
        suggestions.append(f"{primary_prefix}.NewProject")

    return suggestions[:4]


def select_project_name(text: str) -> str:
    """让用户选择项目名"""
    suggestions = generate_name_suggestions(text)

    console.print("\n[bold cyan]请选择项目名称:[/bold cyan]")
    for i, name in enumerate(suggestions, 1):
        console.print(f"  [yellow]{i}[/yellow]. {name}")
    console.print(f"  [yellow]n[/yellow]. 输入自定义名称")
    console.print(f"  [yellow]q[/yellow]. 取消")

    choice = Prompt.ask("\n选择", default="1")

    if choice.lower() == 'q':
        return None
    elif choice.lower() == 'n':
        return Prompt.ask("输入项目名称 (格式: 前缀.项目名)")
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(suggestions):
                return suggestions[idx]
        except:
            pass
        return suggestions[0]


def select_project_dir(project_name: str) -> Path:
    """让用户确认项目目录"""
    default_dir = DEFAULT_PROJECT_DIR / project_name

    console.print(f"\n[bold cyan]项目将创建在:[/bold cyan]")
    console.print(f"  [green]{default_dir}[/green]")

    confirm = Prompt.ask("确认目录? (y=确认 / 输入新路径 / q=取消)", default="y")

    if confirm.lower() == 'q':
        return None
    elif confirm.lower() == 'y':
        return default_dir
    else:
        return Path(confirm).expanduser() / project_name


@click.command("projects")
def list_projects():
    """列出所有项目"""
    from src.core.project_registry import ProjectRegistry

    registry = ProjectRegistry()
    projects = registry.list_all()

    if not projects:
        console.print("[yellow]还没有注册的项目[/yellow]")
        console.print('先创建一个: long-agents "创建一个 XX 项目"')
        return

    table = Table(title="已注册项目")
    table.add_column("项目名", style="cyan")
    table.add_column("路径", style="dim")
    table.add_column("描述")

    for p in projects:
        desc = p.description[:40] + "..." if len(p.description) > 40 else p.description
        table.add_row(p.name, str(p.path), desc)

    console.print(table)


@click.command()
@click.argument("request", required=False)
def ask(request):
    """用自然语言告诉系统你想做什么

    示例:
        long-agents "创建一个博客系统"
        long-agents "继续开发 GW.Blog"
        long-agents "查看状态"
        long-agents "项目列表"
    """
    from src.core.project_registry import ProjectRegistry

    if not request:
        console.print("[yellow]请告诉我你想做什么:[/yellow]")
        console.print('  long-agents "创建一个博客系统"')
        console.print('  long-agents "继续开发"')
        console.print('  long-agents "继续开发 GW.Blog"')
        console.print('  long-agents "查看状态"')
        console.print('  long-agents "项目列表"')
        return

    console.print(f"[dim]理解中: {request}[/dim]")

    registry = ProjectRegistry()
    intent = parse_intent(request)

    # 列出项目
    if intent["action"] == "list":
        from src.commands.ask import list_projects
        from click.testing import CliRunner
        runner = CliRunner()
        result = runner.invoke(list_projects)
        console.print(result.output)
        return

    # 创建新项目
    if intent["action"] == "create":
        project_name = select_project_name(request)
        if not project_name:
            return

        project_dir = select_project_dir(project_name)
        if not project_dir:
            return

        console.print(f"\n[bold green]创建项目: {project_name}[/bold green]")
        console.print(f"[dim]目录: {project_dir}[/dim]\n")

        from src.commands.init import init as init_cmd
        from click.testing import CliRunner

        runner = CliRunner()
        result = runner.invoke(init_cmd, [str(project_dir), "--prompt", request])
        console.print(result.output)

        # 注册项目
        registry.register(project_name, str(project_dir), request)
        console.print(f"[green]项目已注册: {project_name}[/green]")
        return

    # 查看状态或继续开发 - 需要确定项目
    target_project = None
    target_path = None

    # 1. 先检查文本中是否指定了项目
    name, info = extract_project_from_text(request, registry)
    if info:
        target_project = name
        target_path = Path(info.path)
        console.print(f"[dim]指定项目: {target_project}[/dim]")

    # 2. 如果没指定，检查当前目录
    if not target_project:
        current = find_current_project()
        if current:
            info = registry.find_by_path(str(current))
            if info:
                target_project = info.name
                target_path = current
                console.print(f"[dim]当前项目: {target_project}[/dim]")

    # 3. 如果还是没有，让用户选择
    if not target_project:
        target_project, info = select_project(registry, "选择要操作的项目")
        if not target_project:
            return
        target_path = Path(info.path)

    # 更新访问时间
    registry.update_accessed(target_project)

    # 执行操作
    if intent["action"] == "status":
        import os
        original_dir = os.getcwd()
        try:
            os.chdir(target_path)
            from src.commands.status import status as status_cmd
            from click.testing import CliRunner
            runner = CliRunner()
            result = runner.invoke(status_cmd, ["--verbose"])
            console.print(result.output)
        finally:
            os.chdir(original_dir)

    elif intent["action"] == "code":
        import os
        original_dir = os.getcwd()
        try:
            os.chdir(target_path)
            from src.commands.coder_cmd import run as coder_cmd
            from click.testing import CliRunner
            runner = CliRunner()
            result = runner.invoke(coder_cmd)
            console.print(result.output)
        finally:
            os.chdir(original_dir)

    else:
        console.print("[yellow]不太理解你的意思，试试这样说:[/yellow]")
        console.print('  "创建一个 XX 项目"')
        console.print('  "继续开发 项目名"')
        console.print('  "查看状态"')
        console.print('  "项目列表"')
