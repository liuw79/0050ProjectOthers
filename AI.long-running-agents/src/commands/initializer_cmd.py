import click
from pathlib import Path
from rich.console import Console
from src.core.config import load_config
from src.agents.initializer import InitializerAgent

console = Console()


def find_config_file() -> Path:
    """Find config file by searching current and parent directories."""
    current = Path.cwd()

    while current != current.parent:
        config_file = current / "long-agents.yaml"
        if config_file.exists():
            return config_file
        current = current.parent

    # Fallback to default location
    return Path("config/long-agents.yaml")


@click.command()
@click.option("--prompt", "-p", help="Project description for feature generation")
def run(prompt):
    """Run the initializer agent."""
    config_path = find_config_file()

    if not config_path.exists():
        console.print("[red]Error: No config file found. Run 'long-agents init' first.[/red]")
        return

    config = load_config(str(config_path))

    console.print("[bold cyan]Running initializer agent...[/bold cyan]")
    console.print(f"[dim]Config: {config_path}[/dim]")

    if prompt:
        console.print(f"[dim]Prompt: {prompt}[/dim]")

    initializer = InitializerAgent(config, prompt=prompt)
    result = initializer.run()

    if result['status'] == 'success':
        console.print(f"[bold green]Done:[/bold green] {result['message']}")
    else:
        console.print(f"[bold red]Error:[/bold red] {result['message']}")
