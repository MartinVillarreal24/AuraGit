---
name: git-flow-enforcer
description: Enforces branch naming conventions and automated SemVer versioning.
---

# Git Flow Enforcer

This skill ensures that the project follows a strict Git workflow, Semantic Versioning (SemVer), and automated documentation practices.

## Rules

### Branch Naming
All branches must follow the pattern:
- `feature/*`: New features (Minor bump: 0.1.0 -> 0.2.0)
- `fix/*`: Bug fixes (Patch bump: 0.1.0 -> 0.1.1)
- `chore/*`: Maintenance tasks (Patch bump optional)
- `docs/*`: Documentation changes (Patch bump optional)
- `refactor/*`: Code refactoring (Patch bump optional)

### Automated Versioning & Tagging
When a task results in a version bump:
1. Update `version` in `pyproject.toml`.
2. **Tagging**: After merging to `main`, a Git Tag matching the version (e.g., `v0.1.1`) MUST be created and pushed.
3. Every release must be tagged to maintain a visible history on GitHub.

### Changelog Maintenance
Every change that affects the user or the codebase must be documented in `CHANGELOG.md` in **SPANISH** following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.
- Sections: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

### Merge Workflow
- Use **Squash & Merge** on GitHub to maintain a clean, linear history.
- Delete branches immediately after successful merge.

## Usage
When starting a task:
1. Propose the branch name.
2. Propose the new version number based on the type of change.
3. Propose the entry for `CHANGELOG.md`.
4. Ensure tags are created and pushed after completion.
