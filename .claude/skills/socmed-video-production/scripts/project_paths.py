"""Shared path and tool helpers for the bounded social-video scripts.

Every script resolves one project root, keeps inputs and outputs inside it,
never overwrites an existing output and never writes through a symlink.
"""
from __future__ import annotations
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


def project_root(explicit: Path | None = None) -> Path:
    """Explicit --root, else CLAUDE_PROJECT_DIR, else the current directory."""
    if explicit is not None:
        root = explicit.expanduser().resolve()
    elif os.environ.get("CLAUDE_PROJECT_DIR"):
        root = Path(os.environ["CLAUDE_PROJECT_DIR"]).expanduser().resolve()
    else:
        root = Path.cwd().resolve()
    if not root.is_dir():
        raise ValueError(f"project root is not a directory: {root}")
    return root


def inside(path: Path, root: Path) -> Path:
    """Resolve a (possibly relative) path and require it to stay under root."""
    path = path.expanduser()
    resolved = (root / path).resolve() if not path.is_absolute() else path.resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f"path must stay inside the project root {root}: {path}")
    return resolved


def existing_input(path: Path, root: Path) -> Path:
    resolved = inside(path, root)
    if not resolved.is_file() or resolved.stat().st_size == 0:
        raise ValueError(f"input is missing or empty: {resolved}")
    return resolved


def new_output(path: Path, root: Path, suffixes: set[str]) -> Path:
    """Validate a not-yet-existing output path inside root; create its folder."""
    raw = path.expanduser()
    candidate = (root / raw) if not raw.is_absolute() else raw
    if candidate.is_symlink() or candidate.exists():
        raise ValueError(f"refusing to overwrite existing output: {candidate}")
    resolved = inside(raw, root)
    if resolved.suffix.lower() not in suffixes:
        raise ValueError(f"output must end with one of {sorted(suffixes)}: {resolved}")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    if not resolved.parent.resolve().is_relative_to(root):
        raise ValueError("output folder resolves outside the project root")
    return resolved


def write_new_text(path: Path, text: str) -> None:
    """Create a new text file; fails if it exists and never follows a symlink."""
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(text)


def require_tools(*names: str) -> dict[str, str]:
    found = {name: shutil.which(name) for name in names}
    missing = [name for name, where in found.items() if not where]
    if missing:
        raise RuntimeError(f"required tools not found in PATH: {', '.join(missing)}")
    return found  # type: ignore[return-value]


def probe(ffprobe: str, media: Path) -> dict[str, Any]:
    proc = subprocess.run([ffprobe, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(media)],
                          capture_output=True, text=True, timeout=120, check=False)
    if proc.returncode:
        raise RuntimeError(f"ffprobe failed for {media}: {proc.stderr.strip()[-1500:]}")
    return json.loads(proc.stdout)


def stream(meta: dict[str, Any], kind: str) -> dict[str, Any] | None:
    return next((s for s in meta.get("streams", []) if s.get("codec_type") == kind), None)
