"""Validation helpers for the intentionally limited sequential-cut timeline format."""
from __future__ import annotations
import json
import math
import os
from pathlib import Path
from typing import Any

VIDEO_CODECS = {"libx264", "libx265", "libvpx-vp9", "libaom-av1"}
AUDIO_CODECS = {"aac", "libopus", "libmp3lame", "pcm_s16le"}
FIT_MODES = {"contain", "cover"}


def resolve_project_root(timeline: Path, explicit: Path | None = None) -> Path:
    """Project root: explicit --root, else CLAUDE_PROJECT_DIR, else <timeline>/../.. (edit/timeline.json layout)."""
    if explicit is not None:
        return explicit.expanduser().resolve()
    env_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_root:
        return Path(env_root).expanduser().resolve()
    resolved = timeline.resolve()
    if resolved.parent.name != "edit":
        raise ValueError("Cannot infer the project root: keep the timeline in <project>/edit/ or pass --root")
    return resolved.parent.parent


def load_timeline(path: Path, root: Path | None = None) -> tuple[dict[str, Any] | None, list[str], Path | None]:
    errors: list[str] = []
    try:
        root = resolve_project_root(path, root)
    except ValueError as exc:
        return None, [str(exc)], None
    if not path.resolve().is_relative_to(root) or path.resolve().parent == root:
        return None, [f"Timeline must live in a subfolder (normally edit/) of the project root {root}"], None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"Cannot read timeline JSON: {exc}"], None
    if not isinstance(data, dict):
        return None, ["Timeline root must be a JSON object."], None
    profile = data.get("profile")
    if not isinstance(profile, dict):
        errors.append("profile must be an object")
        profile = {}
    width, height = profile.get("width"), profile.get("height")
    if not isinstance(width, int) or not isinstance(height, int):
        errors.append("profile.width and profile.height must be integers")
    elif not (2 <= width <= 8192 and 2 <= height <= 8192 and width % 2 == 0 and height % 2 == 0):
        errors.append("profile dimensions must be even integers between 2 and 8192")
    n, d = profile.get("fps_num"), profile.get("fps_den", 1)
    if not isinstance(n, int) or not isinstance(d, int) or n <= 0 or d <= 0 or n / d > 120:
        errors.append("profile.fps_num/fps_den must define a positive frame rate no greater than 120 fps")
    if profile.get("video_codec", "libx264") not in VIDEO_CODECS:
        errors.append(f"Unsupported video codec. Allowed values: {sorted(VIDEO_CODECS)}")
    if profile.get("audio_codec", "aac") not in AUDIO_CODECS:
        errors.append(f"Unsupported audio codec. Allowed values: {sorted(AUDIO_CODECS)}")
    if profile.get("fit_mode", "contain") not in FIT_MODES:
        errors.append(f"fit_mode must be one of {sorted(FIT_MODES)}")
    crf = profile.get("crf", 23)
    if not isinstance(crf, int) or not 0 <= crf <= 51:
        errors.append("profile.crf must be an integer from 0 to 51")
    preset = profile.get("preset", "medium")
    if preset not in {"ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"}:
        errors.append("profile.preset is not in the supported x264 preset allowlist")
    clips = data.get("clips")
    if not isinstance(clips, list) or not clips:
        errors.append("clips must be a non-empty array")
        clips = []
    if len(clips) > 200:
        errors.append("At most 200 clips are allowed in this draft renderer")
    for index, clip in enumerate(clips):
        label = f"clips[{index}]"
        if not isinstance(clip, dict):
            errors.append(f"{label} must be an object")
            continue
        source = clip.get("source")
        if not isinstance(source, str) or not source.strip():
            errors.append(f"{label}.source must be a non-empty path")
            continue
        src = Path(source).expanduser()
        resolved = (root / src).resolve() if not src.is_absolute() else src.resolve()
        if not resolved.is_relative_to(root):
            errors.append(f"{label}.source resolves outside the project root: {source}")
        elif not resolved.is_file():
            errors.append(f"{label}.source does not exist or is not a file: {source}")
        in_sec, out_sec = clip.get("in_sec"), clip.get("out_sec")
        if (not isinstance(in_sec, (int, float)) or isinstance(in_sec, bool) or
            not isinstance(out_sec, (int, float)) or isinstance(out_sec, bool) or
            not math.isfinite(float(in_sec)) or not math.isfinite(float(out_sec)) or
            in_sec < 0 or out_sec <= in_sec):
            errors.append(f"{label} needs finite in_sec >= 0 and out_sec > in_sec")
    return data, errors, root
