import click
import os
import shutil
import yaml
from pathlib import Path
from rich.console import Console
from rich.table import Table

from src.core.config import Config, LLMConfig, ProjectConfig, TestConfig, GitConfig, DashboardConfig
from src.agents.initializer import InitializerAgent

console = Console()

DEFAULT_CONFIG_TEMPLATE = """# LLM Configuration
llm:
  provider: anthropic
  api_key: ${ANTHROPIC_API_KEY}
  model: claude-sonnet-4-5-20250929
  max_tokens: 4096

# Project Configuration
project:
  work_dir: ./workspace
  feature_list_path: ./feature_list.json
  progress_file: ./claude-progress.txt
  init_script: ./init.sh

# Test Configuration
test:
  tool: puppeteer
  headless: true
  screenshot_dir: ./screenshots

# Git Configuration
git:
  auto_commit: true
  commit_message_format: "feat: {description}"

# Web Dashboard (optional)
dashboard:
  enabled: false
  host: 0.0.0.0
  port: 8000
"""


@click.command()
@click.argument("project_name")
@click.option("--prompt", "-p", help="Project description for feature generation")
@click.option("--config", "-c", "config_path", help="Path to config file")
def init(project_name, prompt, config_path):
    """Initialize a new project."""
    console.print(f"[bold green]Creating project: {project_name}[/bold green]")

    if prompt:
        console.print(f"[dim]Prompt: {prompt}[/dim]")

    project_dir = Path(project_name).resolve()

    # Check if project already exists
    if project_dir.exists():
        console.print(f"[yellow]Warning: Directory '{project_name}' already exists[/yellow]")
        if not click.confirm("Continue with existing directory?"):
            console.print("[red]Aborted[/red]")
            return

    # Create project directory
    project_dir.mkdir(parents=True, exist_ok=True)
    console.print(f"[green]Created directory: {project_dir}[/green]")

    # Create config file
    config_file = project_dir / "long-agents.yaml"
    if config_path:
        # Copy from specified config
        shutil.copy(config_path, config_file)
        console.print(f"[green]Copied config from: {config_path}[/green]")
    else:
        # Create default config
        config_file.write_text(DEFAULT_CONFIG_TEMPLATE)
        console.print(f"[green]Created default config: {config_file}[/green]")

    # Change to project directory
    original_dir = os.getcwd()
    os.chdir(project_dir)

    try:
        # Load configuration
        from src.core.config import load_config
        config = load_config(str(config_file))

        # Update project paths to be relative to project directory
        config.project.work_dir = str(project_dir / config.project.work_dir)
        config.project.feature_list_path = str(project_dir / config.project.feature_list_path)
        config.project.progress_file = str(project_dir / config.project.progress_file)
        config.project.init_script = str(project_dir / config.project.init_script)

        # Run initializer agent
        console.print("[bold blue]Running initializer agent...[/bold blue]")
        agent = InitializerAgent(config, prompt=prompt)
        result = agent.run()

        if result["status"] == "success":
            console.print("[bold green]Project initialized successfully![/bold green]")

            # Display summary
            table = Table(title="Project Summary")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")
            table.add_row("Project Name", project_name)
            table.add_row("Project Path", str(project_dir))
            table.add_row("Config File", str(config_file))
            table.add_row("Work Directory", config.project.work_dir)

            if prompt:
                table.add_row("Prompt", prompt[:50] + "..." if len(prompt) > 50 else prompt)

            console.print(table)

            console.print("\n[bold]Next steps:[/bold]")
            console.print(f"  cd {project_name}")
            console.print("  long-agents status")
            console.print("  long-agents coder run")
        else:
            console.print(f"[bold red]Initialization failed: {result['message']}[/bold red]")

    except Exception as e:
        console.print(f"[bold red]Error during initialization: {e}[/bold red]")
        raise
    finally:
        os.chdir(original_dir)
