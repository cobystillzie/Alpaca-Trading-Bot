from __future__ import annotations

from pathlib import Path
import subprocess

from .config import Settings


def _run(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _inside_git_repo(root: Path) -> bool:
    result = _run(root, ["rev-parse", "--is-inside-work-tree"])
    return result.returncode == 0 and result.stdout.strip() == "true"


def commit_and_push_memory(settings: Settings, message: str) -> str:
    if not settings.auto_git_push:
        return "AUTO_GIT_PUSH=false; skipped git commit."
    if not _inside_git_repo(settings.root):
        return "No git repo found; skipped git commit."

    memory_dir = settings.root / "memory"
    if not memory_dir.exists():
        return "No memory directory found; skipped git commit."

    _run(settings.root, ["add", "memory/*.md"])
    diff = _run(settings.root, ["diff", "--cached", "--name-only"])
    staged = [line.strip() for line in diff.stdout.splitlines() if line.strip()]
    if not staged:
        return "No markdown memory changes to commit."
    disallowed = [path for path in staged if not path.startswith("memory/") or not path.endswith(".md")]
    if disallowed:
        _run(settings.root, ["reset", "--", *disallowed])
        return f"Refused disallowed staged files: {', '.join(disallowed)}"

    commit = _run(settings.root, ["commit", "-m", message])
    if commit.returncode != 0:
        return f"Git commit failed: {commit.stderr.strip() or commit.stdout.strip()}"

    remotes = _run(settings.root, ["remote"])
    if "origin" not in remotes.stdout.split():
        return "Committed markdown memory locally; no origin remote to push."

    push = _run(settings.root, ["push"])
    if push.returncode != 0:
        return f"Committed locally; git push failed: {push.stderr.strip() or push.stdout.strip()}"
    return "Committed and pushed markdown memory changes."

