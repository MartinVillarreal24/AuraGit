import click
import os
import sys
from rich.console import Console
from rich.panel import Panel
from git_ai.git_manager import GitManager
from git_ai.ai_client import AIClientFactory
from git_ai.config import Config

console = Console()

@click.group()
def cli():
    """AI-Powered Auto-Commit Tool"""
    try:
        Config.validate()
    except ValueError as e:
        console.print(f"[red]Configuration Error: {str(e)}[/red]")
        sys.exit(1)

@cli.command()
@click.option('--repo', default='.', help='Path to the git repository')
def install(repo):
    """Install the git hook in the repository"""
    try:
        gm = GitManager(repo)
        gm.install_hook(repo)
        console.print("[green]✔ Git hook installed successfully![/green]")
        console.print(f"[blue]Using AI Provider: {Config.AI_PROVIDER}[/blue]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@cli.command()
@click.option('--repo', default='.', help='Path to the git repository')
@click.option('--hook', is_flag=True, help='Running as a git hook')
def generate(repo, hook):
    """Generate a commit message based on staged changes"""
    try:
        gm = GitManager(repo)
        ai = AIClientFactory.get_provider()

        if not gm.is_repo_dirty():
            console.print("[yellow]No changes found.[/yellow]")
            return

        diff = gm.get_staged_diff()
        if not diff:
            staged_files = gm.get_staged_files()
            if not staged_files:
                console.print("[yellow]No staged changes. Use 'git add' first.[/yellow]")
                return
            diff = f"Modified files: {', '.join(staged_files)}"

        console.print(f"[blue]Generating message using {Config.AI_PROVIDER}...[/blue]")
        
        if not ai.check_connection():
            console.print(f"[red]Error: Could not connect to {Config.AI_PROVIDER}. Check your settings.[/red]")
            return

        message = ai.generate_commit_message(diff)

        if hook:
            # If running as a hook, we write to the commit message file
            commit_msg_file = sys.argv[-1] # Usually the last arg in prepare-commit-msg
            if os.path.exists(commit_msg_file):
                with open(commit_msg_file, 'w') as f:
                    f.write(message)
                console.print("[green]✔ Commit message generated and applied.[/green]")
            else:
                console.print(Panel(message, title="Generated Commit Message", border_style="green"))
        else:
            console.print(Panel(message, title="Generated Commit Message", border_style="green"))
            if click.confirm("Do you want to commit with this message?"):
                gm.repo.index.commit(message)
                console.print("[green]✔ Changes committed successfully![/green]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    cli()
