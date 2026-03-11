import git
import os
from typing import List, Optional

class GitManager:
    def __init__(self, repo_path: str = "."):
        try:
            self.repo = git.Repo(repo_path, search_parent_directories=True)
        except git.InvalidGitRepositoryError:
            raise ValueError(f"Directory {repo_path} is not a valid Git repository.")

    def get_staged_diff(self) -> str:
        """Returns the diff of staged changes."""
        return self.repo.git.diff("--staged")

    def get_staged_files(self) -> List[str]:
        """Returns a list of files that are currently staged."""
        return [item.a_path for item in self.repo.index.diff("HEAD")]

    def is_repo_dirty(self) -> bool:
        """Checks if there are any unstaged or staged changes."""
        return self.repo.is_dirty() or len(self.repo.index.diff("HEAD")) > 0

    def install_hook(self, script_path: str):
        """Installs the prepare-commit-msg hook."""
        hook_path = os.path.join(self.repo.git_dir, "hooks", "prepare-commit-msg")
        
        hook_content = f"""#!/bin/sh
# AI Auto-Commit Hook
python {os.path.abspath(script_path)} --hook $1
"""
        with open(hook_path, "w") as f:
            f.write(hook_content)
        
        # Make the hook executable (Unix-like systems, for Windows it's handled differently but good practice)
        if os.name != "nt":
            os.chmod(hook_path, 0o755)

    def get_repo_root(self) -> str:
        return self.repo.working_tree_dir
