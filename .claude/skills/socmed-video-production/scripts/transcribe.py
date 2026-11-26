#!/usr/bin/env python3
"""Transcribe project media locally with faster-whisper and write SRT, VTT and JSON.

Runs entirely on this machine (CPU, int8). The first run downloads the chosen
Whisper model weights from Hugging Face into the local cache; media is never
uploaded. Output is a machine draft: correct names, numbers and quotes before
using it as captions.
Run with the project virtual environment: .venv/bin/python transcribe.py ...
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path
from project_paths import existing_input, inside, project_root, require_tools, write_new_text

MODELS = {"tiny", "tiny.en", "base", "base.en", "small", "small.en", "medium", "medium.en",
          "large-v3", "large-v3-turbo", "distil-large-v3"}


def decode_audio(ffmpeg: str, media: Path):
    """Decode the first audio stream to 16 kHz mono float32 with system FFmpeg (avoids PyAV version drift)."""
    import numpy as np
    proc = subprocess.run([ffmpeg, "-nostdin", "-hide_banner", "-loglevel", "error", "-i", str(media), "-map", "0:a:0",
                           "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, timeout=3600, check=False)
    if proc.returncode or not proc.stdout:
        raise RuntimeError(f"could not decode audio from {media}: {proc.stderr.decode(errors='replace')[-1500:]}")
    return np.frombuffer(proc.stdout, dtype=np.float32)


def ts(seconds: float, sep: str) -> str:
    ms = max(0, int(round(seconds * 1000)))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def wrap(words: list[str], max_chars: int) -> list[str]:
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if current and len(trial) > max_chars:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def build_cues(words: list[dict], max_chars: int, max_lines: int, max_seconds: float) -> list[dict]:
    """Group timed words into readable caption cues; break on punctuation, length and duration."""
    merged: list[dict] = []
    for word in words:  # Whisper word pieces without a leading space belong to the previous word ("step" "-by" "-step")
        if merged and word["word"] and not word["word"][0].isspace():
            merged[-1] = {**merged[-1], "word": merged[-1]["word"] + word["word"], "end": word["end"]}
        else:
            merged.append(dict(word))
    cues, bucket = [], []
    limit = max_chars * max_lines
    for word in merged:
        text = word["word"].strip()
        if not text:
            continue
        candidate = bucket + [{**word, "word": text}]
        joined = " ".join(w["word"] for w in candidate)
        too_long = len(joined) > limit or len(wrap([w["word"] for w in candidate], max_chars)) > max_lines
        too_slow = candidate[-1]["end"] - candidate[0]["start"] > max_seconds
        if bucket and (too_long or too_slow):
            cues.append(bucket)
            bucket = [{**word, "word": text}]
        else:
            bucket = candidate
        if bucket and bucket[-1]["word"][-1:] in ".?!":
            cues.append(bucket)
            bucket = []
    if bucket:
        cues.append(bucket)
    return [{"start": c[0]["start"], "end": c[-1]["end"],
             "lines": wrap([w["word"] for w in c], max_chars)} for c in cues]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("media", type=Path, help="Audio/video file inside the project")
    ap.add_argument("--root", type=Path, default=None, help="Project root (default: CLAUDE_PROJECT_DIR, else cwd)")
    ap.add_argument("--output-dir", type=Path, default=Path("transcripts"), help="Project-relative folder (default: transcripts)")
    ap.add_argument("--name", help="Output base name (default: <media stem>.whisper-<model>)")
    ap.add_argument("--model", default="small", choices=sorted(MODELS), help="Whisper model (default: small; medium/large are slower on CPU)")
    ap.add_argument("--language", help="ISO code such as en; default auto-detect")
    ap.add_argument("--max-chars", type=int, default=32, help="Max characters per caption line (default 32 for vertical video)")
    ap.add_argument("--max-lines", type=int, default=2, choices=(1, 2, 3))
    ap.add_argument("--max-seconds", type=float, default=5.0, help="Max caption duration in seconds")
    ap.add_argument("--threads", type=int, default=0, help="CPU threads (0 = library default)")
    args = ap.parse_args()
    if not 12 <= args.max_chars <= 60 or not 1.0 <= args.max_seconds <= 10.0:
        ap.error("--max-chars must be 12-60 and --max-seconds 1-10")
    try:
        root = project_root(args.root)
        media = existing_input(args.media, root)
        out_dir = inside(args.output_dir, root)
        out_dir.mkdir(parents=True, exist_ok=True)
        if not out_dir.resolve().is_relative_to(root):
            raise ValueError("output folder resolves outside the project root")
    except ValueError as exc:
        ap.error(str(exc))
    base = args.name or f"{media.stem}.whisper-{args.model}"
    if "/" in base or base.startswith("."):
        ap.error("--name must be a plain file name")
    targets = {ext: out_dir / f"{base}.{ext}" for ext in ("srt", "vtt", "json")}
    clash = [str(p) for p in targets.values() if p.exists() or p.is_symlink()]
    if clash:
        ap.error(f"refusing to overwrite existing transcript files: {clash}")
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        ap.error("faster-whisper is not installed; run with .venv/bin/python after installing requirements-transcribe.txt")

    try:
        audio = decode_audio(require_tools("ffmpeg")["ffmpeg"], media)
    except RuntimeError as exc:
        ap.error(str(exc))
    model = WhisperModel(args.model, device="cpu", compute_type="int8", cpu_threads=args.threads)
    segments, info = model.transcribe(audio, language=args.language, word_timestamps=True, vad_filter=True)
    seg_out, words = [], []
    for seg in segments:
        seg_words = [{"word": w.word, "start": float(w.start), "end": float(w.end), "probability": round(float(w.probability), 3)}
                     for w in (seg.words or [])]
        words.extend(seg_words)
        seg_out.append({"start": float(seg.start), "end": float(seg.end), "text": seg.text.strip(),
                        "avg_logprob": round(float(seg.avg_logprob), 3), "words": seg_words})
    cues = build_cues(words, args.max_chars, args.max_lines, args.max_seconds)
    srt = "".join(f"{i}\n{ts(c['start'], ',')} --> {ts(c['end'], ',')}\n" + "\n".join(c["lines"]) + "\n\n"
                  for i, c in enumerate(cues, 1))
    vtt = "WEBVTT\n\n" + "".join(f"{ts(c['start'], '.')} --> {ts(c['end'], '.')}\n" + "\n".join(c["lines"]) + "\n\n" for c in cues)
    low_conf = [w for w in words if w["probability"] < 0.5]
    record = {"source": media.relative_to(root).as_posix(), "model": args.model, "language": info.language,
              "language_probability": round(float(info.language_probability), 3), "duration_seconds": round(float(info.duration), 3),
              "status": "machine_draft_needs_review", "low_confidence_words": len(low_conf), "segments": seg_out}
    write_new_text(targets["srt"], srt)
    write_new_text(targets["vtt"], vtt)
    write_new_text(targets["json"], json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"source": record["source"], "language": info.language, "duration_seconds": record["duration_seconds"],
                      "segments": len(seg_out), "caption_cues": len(cues), "low_confidence_words": len(low_conf),
                      "files": {k: str(v) for k, v in targets.items()},
                      "note": "Machine draft: review names, numbers, quotes and timing before publishing captions."}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
