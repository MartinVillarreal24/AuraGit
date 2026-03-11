import click
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from git_ai.git_manager import GitManager
from git_ai.ai_client import AIClientFactory
from git_ai.config import Config, global_config_path
from git_ai.memory import MemoryManager, Engram, VALID_TYPES
import shutil
from pathlib import Path

console = Console()

@click.group()
def cli():
    """AI-Powered Auto-Commit Tool"""
    try:
        Config.validate()
    except ValueError as e:
        console.print(f"[red]Configuration Error: {str(e)}[/red]")
        sys.exit(1)

@cli.group()
def config():
    """Manage global configuration"""
    pass

@config.command()
def init():
    """Initialize global configuration folder and .env template"""
    try:
        config_dir = global_config_path.parent
        env_file = global_config_path
        
        if not config_dir.exists():
            config_dir.mkdir(parents=True)
            console.print(f"[green]✔ Created configuration directory: {config_dir}[/green]")
        
        if not env_file.exists():
            # Try to copy from local .env.example if it exists in the current repo
            template_path = Path(".env.example")
            if template_path.exists():
                shutil.copy(template_path, env_file)
                console.print(f"[green]✔ Created .env from template in: {env_file}[/green]")
            else:
                # Fallback to a basic template if .env.example is not found
                default_content = """# AuraGit Configuration
AI_PROVIDER=ollama
AI_LANGUAGE=es
COMMIT_STYLE=conventional

# Ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:7b

# API Keys (fill these if using cloud providers)
OPENAI_API_KEY=
GEMINI_API_KEY=
ANTHROPIC_API_KEY=
"""
                with open(env_file, "w", encoding="utf-8") as f:
                    f.write(default_content)
                console.print(f"[green]✔ Created default .env in: {env_file}[/green]")
            
            console.print("[yellow]Please edit the .env file with your API keys.[/yellow]")
        else:
            console.print(f"[yellow]! Configuration file already exists at: {env_file}[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Error initializing config: {str(e)}[/red]")

@cli.group()
def memory():
    """Manage persistent memory (Engrams)"""
    pass

@memory.command(name="save")
@click.option("--title", "-t", required=True, help="Short title for the engram (e.g., 'Implemented Login')")
@click.option("--type", "-y", "engram_type", required=True, type=click.Choice(VALID_TYPES, case_sensitive=False), help="Type of engram")
@click.option("--content", "-c", required=True, help="Content: What was done, Why, Where, Learned")
def memory_save(title, engram_type, content):
    """Save a new engram to persistent memory"""
    try:
        mm = MemoryManager()
        engram = Engram(title=title, engram_type=engram_type, content=content)
        filepath = mm.save(engram)
        console.print(f"[green]✔ Engram saved: {filepath.name}[/green]")
        console.print(Panel(f"[bold]{title}[/bold]\n[dim]{engram_type}[/dim]\n\n{content}", title="💾 Engram Saved", border_style="cyan"))
    except Exception as e:
        console.print(f"[red]Error saving engram: {str(e)}[/red]")

@memory.command(name="list")
@click.option("--limit", "-n", default=10, help="Number of engrams to show")
def memory_list(limit):
    """List recent engrams from memory"""
    try:
        mm = MemoryManager()
        engrams = mm.list_engrams(limit=limit)
        if not engrams:
            console.print("[yellow]No engrams found. Use 'git-ai memory save' to create one.[/yellow]")
            return

        table = Table(title="🧠 Memory (Engrams)", border_style="cyan")
        table.add_column("Timestamp", style="dim")
        table.add_column("Type", style="magenta")
        table.add_column("Title", style="bold")
        table.add_column("Content", max_width=50)

        for e in engrams:
            ts = e.timestamp[:19] if e.timestamp else "N/A"
            table.add_row(ts, e.engram_type, e.title, e.content[:50] + "..." if len(e.content) > 50 else e.content)

        console.print(table)
    except Exception as e:
        console.print(f"[red]Error listing engrams: {str(e)}[/red]")

@memory.command(name="search")
@click.argument("query")
@click.option("--limit", "-n", default=5, help="Max results")
def memory_search(query, limit):
    """Search engrams by keyword"""
    try:
        mm = MemoryManager()
        results = mm.search(query, limit=limit)
        if not results:
            console.print(f"[yellow]No engrams found for '{query}'.[/yellow]")
            return

        table = Table(title=f"🔍 Search Results for '{query}'", border_style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Title", style="bold")
        table.add_column("Content", max_width=60)

        for e in results:
            table.add_row(e.engram_type, e.title, e.content[:60] + "..." if len(e.content) > 60 else e.content)

        console.print(table)
    except Exception as e:
        console.print(f"[red]Error searching engrams: {str(e)}[/red]")

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
@click.argument('msg_file', required=False)
def generate(repo, hook, msg_file):
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

        # Include memory context for smarter generation
        mm = MemoryManager()
        context = mm.get_context(limit=3)

        message = ai.generate_commit_message(diff, context=context)

        if hook:
            # If running as a hook, we write to the commit message file
            commit_msg_file = msg_file
            if commit_msg_file and os.path.exists(commit_msg_file):
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
