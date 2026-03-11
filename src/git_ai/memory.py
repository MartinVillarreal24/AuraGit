import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from git_ai.config import Config

MEMORY_DIR = Path.home() / ".git-ai" / "memory"

VALID_TYPES = ["bugfix", "decision", "architecture", "discovery", "pattern", "config", "feature"]


class Engram:
    """Represents a single memory unit (engram)."""

    def __init__(self, title: str, engram_type: str, content: str, timestamp: str = None):
        self.title = title
        self.engram_type = engram_type
        self.content = content
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "type": self.engram_type,
            "content": self.content,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Engram":
        return cls(
            title=data["title"],
            engram_type=data["type"],
            content=data["content"],
            timestamp=data.get("timestamp"),
        )

    def __repr__(self):
        return f"Engram(title='{self.title}', type='{self.engram_type}')"


class MemoryManager:
    """Manages persistent memory storage for AuraGit."""

    def __init__(self, memory_dir: Path = None):
        self.memory_dir = memory_dir or MEMORY_DIR
        self._ensure_dir()

    def _ensure_dir(self):
        """Create the memory directory if it doesn't exist."""
        if not self.memory_dir.exists():
            self.memory_dir.mkdir(parents=True)

    def _get_filepath(self, engram: Engram) -> Path:
        """Generate a unique filename for an engram."""
        safe_title = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in engram.title)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.memory_dir / f"{timestamp}_{safe_title}.json"

    def save(self, engram: Engram) -> Path:
        """Save an engram to disk."""
        filepath = self._get_filepath(engram)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(engram.to_dict(), f, ensure_ascii=False, indent=2)
        return filepath

    def list_engrams(self, limit: int = 10) -> List[Engram]:
        """List the most recent engrams."""
        files = sorted(self.memory_dir.glob("*.json"), reverse=True)
        engrams = []
        for f in files[:limit]:
            try:
                with open(f, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                    engrams.append(Engram.from_dict(data))
            except (json.JSONDecodeError, KeyError):
                continue
        return engrams

    def search(self, query: str, limit: int = 5) -> List[Engram]:
        """Search engrams by keyword in title or content."""
        query_lower = query.lower()
        results = []
        files = sorted(self.memory_dir.glob("*.json"), reverse=True)
        for f in files:
            try:
                with open(f, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                    engram = Engram.from_dict(data)
                    if query_lower in engram.title.lower() or query_lower in engram.content.lower():
                        results.append(engram)
                        if len(results) >= limit:
                            break
            except (json.JSONDecodeError, KeyError):
                continue
        return results

    def get_context(self, limit: int = 3) -> str:
        """Format recent engrams as context for AI prompt."""
        engrams = self.list_engrams(limit=limit)
        if not engrams:
            return ""

        context_parts = ["Recent project context:"]
        for e in engrams:
            context_parts.append(f"- [{e.engram_type}] {e.title}: {e.content}")

        return "\n".join(context_parts)
