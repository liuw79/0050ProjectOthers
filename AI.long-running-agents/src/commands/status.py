import click
import os
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def find_project_root() -> Path:
    """Find project root by looking for long-agents.yaml."""
    current = Path.cwd()

    while current != current.parent:
        config_file = current / "long-agents.yaml"
        if config_file.exists():
            return current
        current = current.parent

    return Path.cwd()


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Show detailed information")
def status(verbose):
    """Show project status."""
    project_root = find_project_root()
    config_file = project_root / "long-agents.yaml"

    # Main status table
    main_table = Table(title="Project Status", show_header=False)
    main_table.add_column("Property", style="cyan")
    main_table.add_column("Value", style="green")

    main_table.add_row("Project Root", str(project_root))
    main_table.add_row("Config File", str(config_file) if config_file.exists() else "Not found")

    # Check feature list
    feature_list_path = project_root / "feature_list.json"
    if feature_list_path.exists():
        try:
            with open(feature_list_path, 'r') as f:
                features = json.load(f)

            total = len(features)
            completed = sum(1 for f in features if f.get("passes", False))
            pending = total - completed

            progress_pct = (completed / total * 100) if total > 0 else 0

            main_table.add_row("Features Total", str(total))
            main_table.add_row("Features Completed", f"{completed} ({progress_pct:.1f}%)")
            main_table.add_row("Features Pending", str(pending))

            if verbose and features:
                # Feature details table
                feature_table = Table(title="\nFeature Details")
                feature_table.add_column("#", style="dim", width=3)
                feature_table.add_column("Category", style="cyan", width=10)
                feature_table.add_column("Description", style="white")
                feature_table.add_column("Status", width=10)

                for i, feature in enumerate(features):
                    status_str = "[green]Done[/green]" if feature.get("passes") else "[yellow]Pending[/yellow]"
                    desc = feature.get("description", "No description")
                    if len(desc) > 50:
                        desc = desc[:47] + "..."
                    feature_table.add_row(
                        str(i + 1),
                        feature.get("category", "unknown"),
                        desc,
                        status_str
                    )

                console.print(feature_table)
        except Exception as e:
            main_table.add_row("Feature List", f"[red]Error reading: {e}[/red]")
    else:
        main_table.add_row("Feature List", "[yellow]Not found[/yellow]")

    # Check git status
    git_dir = project_root / ".git"
    if git_dir.exists():
        try:
            import subprocess
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=project_root,
                capture_output=True,
                text=True
            )

            changes = result.stdout.strip().split('\n') if result.stdout.strip() else []
            if changes and changes[0]:
                main_table.add_row("Git Status", f"[yellow]{len(changes)} uncommitted changes[/yellow]")

                if verbose:
                    changes_table = Table(title="\nUncommitted Changes")
                    changes_table.add_column("Status", width=3)
                    changes_table.add_column("File")

                    for change in changes[:10]:  # Show first 10
                        status_code = change[:2].strip()
                        file_path = change[3:]
                        changes_table.add_row(status_code, file_path)

                    if len(changes) > 10:
                        changes_table.add_row("...", f"and {len(changes) - 10} more")

                    console.print(changes_table)
            else:
                main_table.add_row("Git Status", "[green]Clean[/green]")

            # Get current branch
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=project_root,
                capture_output=True,
                text=True
            )
            if branch_result.returncode == 0:
                main_table.add_row("Git Branch", branch_result.stdout.strip() or "HEAD detached")

            # Get last commit
            log_result = subprocess.run(
                ["git", "log", "-1", "--oneline"],
                cwd=project_root,
                capture_output=True,
                text=True
            )
            if log_result.returncode == 0:
                main_table.add_row("Last Commit", log_result.stdout.strip())

        except Exception as e:
            main_table.add_row("Git Status", f"[red]Error: {e}[/red]")
    else:
        main_table.add_row("Git Status", "[yellow]Not initialized[/yellow]")

    # Check progress file
    progress_file = project_root / "claude-progress.txt"
    if progress_file.exists():
        try:
            with open(progress_file, 'r') as f:
                content = f.read()
                lines = [l for l in content.split('\n') if l.strip() and not l.startswith('#')]
                main_table.add_row("Progress Entries", str(len(lines)))

                if verbose and content:
                    console.print(Panel(content, title="Progress Log"))
        except Exception as e:
            main_table.add_row("Progress File", f"[red]Error reading: {e}[/red]")
    else:
        main_table.add_row("Progress File", "[yellow]Not found[/yellow]")

    console.print(main_table)

    # Check workspace directory
    workspace_dir = project_root / "workspace"
    if workspace_dir.exists():
        py_files = list(workspace_dir.glob("**/*.py"))
        main_table.add_row("Python Files in Workspace", str(len(py_files)))
