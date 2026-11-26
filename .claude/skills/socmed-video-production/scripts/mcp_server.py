"""Local MCP tools for a Claude Code social-video workspace.

All file operations are constrained to CLAUDE_PROJECT_DIR/current project root.
The server never accepts arbitrary shell commands or uploads media.
"""
from __future__ import annotations
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("socmed-video-production")
MEDIA_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi", ".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".opus", ".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}


def project_root() -> Path:
    env_root = os.environ.get("CLAUDE_PROJECT_DIR")
    root = Path(env_root).expanduser().resolve() if env_root else Path.cwd().resolve()
    if not root.is_dir():
        raise ValueError("Project root is not a directory")
    return root


def inside_root(path: str | Path, root: Path | None = None) -> Path:
    root = root or project_root()
    candidate = Path(path).expanduser()
    resolved = (root / candidate).resolve() if not candidate.is_absolute() else candidate.resolve()
    if not resolved.is_relative_to(root):
        raise ValueError("Path must remain inside the Claude project root")
    return resolved


def run_json(args: list[str], timeout: int = 1800) -> dict[str, Any]:
    proc = subprocess.run(args, cwd=project_root(), capture_output=True, text=True, timeout=timeout, check=False)
    result: dict[str, Any] = {"returncode": proc.returncode, "stdout": proc.stdout[-16000:], "stderr": proc.stderr[-5000:]}
    if proc.returncode:
        return result
    try:
        result["result"] = json.loads(proc.stdout)
    except json.JSONDecodeError:
        pass
    return result


@mcp.tool()
def project_status() -> dict[str, Any]:
    """Report the project root, expected folders, manifest and local tool availability."""
    root = project_root()
    expected = ["briefs", "assets/originals", "assets/proxies", "assets/audio", "assets/graphics", "transcripts", "edit", "review", "exports", "logs"]
    return {"project_root": str(root), "production_manifest_exists": (root / "production.json").is_file(), "folders": {name: (root / name).is_dir() for name in expected}, "executables": {name: shutil.which(name) for name in ("ffmpeg", "ffprobe", "kdenlive", "melt")}}


@mcp.tool()
def list_media(subdirectory: str = "assets") -> dict[str, Any]:
    """List supported media beneath a project-relative directory; symlinks are skipped."""
    root = project_root()
    folder = inside_root(subdirectory, root)
    if not folder.is_dir():
        raise ValueError("The requested project-relative directory does not exist")
    items = []
    for path in sorted(folder.rglob("*")):
        if path.is_symlink() or not path.is_file() or path.suffix.lower() not in MEDIA_EXTENSIONS:
            continue
        items.append({"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size})
    return {"count": len(items), "items": items[:1000], "truncated": len(items) > 1000}


@mcp.tool()
def probe_media(path: str) -> dict[str, Any]:
    """Read technical metadata for one media file inside the project root using ffprobe."""
    root = project_root(); media = inside_root(path, root)
    if not media.is_file() or media.suffix.lower() not in MEDIA_EXTENSIONS:
        raise ValueError("Expected an existing supported media file within the project")
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise RuntimeError("ffprobe is not installed")
    return run_json([ffprobe, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(media)], timeout=90)


@mcp.tool()
def validate_timeline(timeline_path: str = "edit/timeline.json") -> dict[str, Any]:
    """Validate timeline JSON paths, clips, frame profile and codec settings without rendering."""
    root = project_root(); timeline = inside_root(timeline_path, root)
    if not timeline.is_file():
        raise ValueError("Timeline file does not exist")
    script = root / ".claude/skills/socmed-video-production/scripts/validate_timeline.py"
    if not script.is_file():
        raise RuntimeError("The project skill tools are missing; rerun the workspace bootstrapper")
    return run_json([sys.executable, str(script), str(timeline), "--root", str(root)], timeout=90)


@mcp.tool()
def render_roughcut(timeline_path: str = "edit/timeline.json", output_path: str = "review/roughcut_v001.mp4") -> dict[str, Any]:
    """Render a validated sequential hard-cut draft; refuses existing outputs and external paths."""
    root = project_root(); timeline = inside_root(timeline_path, root); output = inside_root(output_path, root)
    if not timeline.is_file():
        raise ValueError("Timeline file does not exist")
    if output.exists() or output.is_symlink():
        raise ValueError("Output already exists; choose a new versioned output path")
    script = root / ".claude/skills/socmed-video-production/scripts/render_roughcut.py"
    if not script.is_file():
        raise RuntimeError("The project skill tools are missing; rerun the workspace bootstrapper")
    return run_json([sys.executable, str(script), str(timeline), "--root", str(root), "--output", str(output)], timeout=7200)


@mcp.tool()
def validate_export(media_path: str, profile_path: str = "production.json", profile_id: str = "") -> dict[str, Any]:
    """Probe an in-project export and compare basic size/frame-rate fields to the chosen profile."""
    root = project_root(); media = inside_root(media_path, root); profile = inside_root(profile_path, root)
    if not media.is_file() or not profile.is_file():
        raise ValueError("Media and profile paths must exist inside the project root")
    script = root / ".claude/skills/socmed-video-production/scripts/validate_export.py"
    cmd = [sys.executable, str(script), str(media), "--profile", str(profile)]
    if profile_id:
        cmd += ["--profile-id", profile_id]
    return run_json(cmd, timeout=120)


def _script(root: Path, name: str) -> Path:
    script = root / ".claude/skills/socmed-video-production/scripts" / name
    if not script.is_file():
        raise RuntimeError("The project skill tools are missing; rerun the workspace bootstrapper")
    return script


@mcp.tool()
def transcribe_media(media_path: str, model: str = "small", language: str = "", output_dir: str = "transcripts",
                     max_chars: int = 32, max_lines: int = 2) -> dict[str, Any]:
    """Transcribe in-project media locally (faster-whisper, CPU) to draft SRT/VTT/JSON with word timings; never overwrites."""
    root = project_root(); media = inside_root(media_path, root); out = inside_root(output_dir, root)
    if not media.is_file():
        raise ValueError("Media file does not exist inside the project")
    cmd = [sys.executable, str(_script(root, "transcribe.py")), str(media), "--root", str(root), "--output-dir", str(out),
           "--model", model, "--max-chars", str(int(max_chars)), "--max-lines", str(int(max_lines))]
    if language:
        cmd += ["--language", language]
    return run_json(cmd, timeout=7200)


@mcp.tool()
def normalize_loudness(media_path: str, output_path: str, target_lufs: float = -14.0, true_peak: float = -1.0) -> dict[str, Any]:
    """Two-pass loudness normalization to a new in-project file; video is stream-copied. Confirm the platform target first."""
    root = project_root(); media = inside_root(media_path, root); output = inside_root(output_path, root)
    if not media.is_file():
        raise ValueError("Media file does not exist inside the project")
    return run_json([sys.executable, str(_script(root, "normalize_loudness.py")), str(media), "--root", str(root),
                     "--output", str(output), "--target-lufs", str(float(target_lufs)), "--true-peak", str(float(true_peak))], timeout=7200)


@mcp.tool()
def reframe_video(media_path: str, output_path: str, width: int = 1080, height: int = 1920, mode: str = "crop",
                  x_center: float = 0.5, y_center: float = 0.5) -> dict[str, Any]:
    """Reframe in-project video to a new size (crop / blur_pad / pad) into a new .mp4; audio is stream-copied."""
    root = project_root(); media = inside_root(media_path, root); output = inside_root(output_path, root)
    if not media.is_file():
        raise ValueError("Media file does not exist inside the project")
    if mode not in {"crop", "blur_pad", "pad"}:
        raise ValueError("mode must be crop, blur_pad or pad")
    return run_json([sys.executable, str(_script(root, "reframe.py")), str(media), "--root", str(root), "--output", str(output),
                     "--width", str(int(width)), "--height", str(int(height)), "--mode", mode,
                     "--x-center", str(float(x_center)), "--y-center", str(float(y_center))], timeout=7200)


def main() -> None:
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
