# Local MCP and CLI usage

The bundled integration is intentionally a thin, local convenience layer. It exposes project inventory, FFprobe analysis, manifest validation, draft rendering and export QA. It does not send media to a remote service and does not provide an undocumented editor API. Read tool outputs, then use human playback for subjective review.

## Optional Claude Code MCP setup

From the workspace root (after cloning this repository), create a virtual environment and install the pinned-range dependencies in `requirements-mcp.txt`:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r .claude/skills/socmed-video-production/requirements-mcp.txt
```

Review the project-scoped `.mcp.json` before enabling it. It launches the local Python server using the project virtual environment. Then restart/reload Claude Code if needed and inspect `/mcp` to confirm the server and tools appear. Only trust the server after reviewing its code and path boundaries. Claude Code project-scoped MCP configuration is user-approved/trust-gated; do not bypass that gate.

Tools exposed:

- `project_status`: verify the known workspace layout and manifest.
- `list_media`: enumerate supported media beneath `assets/` without following symlinks outside the workspace.
- `probe_media`: read media metadata for an in-project path through `ffprobe`.
- `validate_timeline`: validate source paths, timing, tracks and output profile in a project timeline JSON.
- `render_roughcut`: render only a validated sequential rough cut using the bundled renderer; no arbitrary filter string or command is accepted.
- `validate_export`: probe a rendered file and compare basic properties against the selected profile.
- `transcribe_media`: local faster-whisper transcription to draft SRT/VTT/JSON (word timings, low-confidence count) in `transcripts/`.
- `normalize_loudness`: two-pass EBU R128 loudnorm to a new file; reports before/after LUFS, true peak and LRA.
- `reframe_video`: re-size to a new aspect (`crop` with focus point, `blur_pad`, or `pad`) into a new MP4.

Transcription needs the extra dependency: `.venv/bin/python -m pip install -r .claude/skills/socmed-video-production/requirements-transcribe.txt`. It runs on the CPU (`int8`). The first use of each model downloads its weights from Hugging Face into the local cache; media itself never leaves the machine. `small` is the default balance of speed and accuracy on CPU; use `medium` or `large-v3-turbo` for difficult audio when time allows.

The tools may require explicit user setup/approval depending on the Claude Code version and settings. Do not store credentials in the MCP JSON. Keep original media private; any external AI transcription/generation requires separate informed approval.

## Direct CLI

Run from the repository root. Use explicit, quoted path arguments; scripts use subprocess argument arrays internally.

```bash
python3 scripts/bootstrap_workspace.py --target /home/t0n34781/Projects/socmed_content_creation
python3 .claude/skills/socmed-video-production/scripts/media_inventory.py --root /home/t0n34781/Projects/socmed_content_creation --output /home/t0n34781/Projects/socmed_content_creation/logs/media_inventory.json
python3 .claude/skills/socmed-video-production/scripts/validate_timeline.py /path/to/project/edit/timeline.json
python3 .claude/skills/socmed-video-production/scripts/render_roughcut.py /path/to/project/edit/timeline.json --output /path/to/project/review/roughcut_v001.mp4
python3 .claude/skills/socmed-video-production/scripts/validate_export.py /path/to/project/review/roughcut_v001.mp4 --profile /path/to/project/platform_profiles.json
.venv/bin/python .claude/skills/socmed-video-production/scripts/transcribe.py assets/originals/interview.mp4 --model small --language en
python3 .claude/skills/socmed-video-production/scripts/normalize_loudness.py review/cut_v003.mp4 --output review/cut_v003_loud.mp4 --target-lufs -14
python3 .claude/skills/socmed-video-production/scripts/reframe.py assets/originals/wide.mp4 --output assets/proxies/wide_9x16.mp4 --mode crop --x-center 0.4
```

The three finishing scripts resolve the project root from `--root`, then `CLAUDE_PROJECT_DIR`, then the current directory, and refuse inputs or outputs outside it. They never overwrite an existing file.

If the user changes the target folder, use that path consistently. The default target is configurable; the cloud build environment does not create or access `/home/t0n34781` on the user's actual Ubuntu machine.

## Timeline renderer contract

`timeline.json` is intentionally restricted: sequence/profile (width, height, fps, video/audio codec and CRF/preset), output aspect policy, and an ordered list of clip source paths with in/out seconds. Current renderer supports sequential hard cuts; it normalizes each clip to a compatible frame geometry/frame rate and concatenates. It does not implement nested tracks, transitions, animated graphics, keyframes, or audio mixing; use Kdenlive or a separately reviewed FFmpeg workflow for those. Never put untrusted FFmpeg expressions, shell commands, or filter graphs in a manifest.

A draft is not suitable for publication until timing, framing, audio, captions and the final path are visually/listening-reviewed. The renderer writes to a new destination and refuses to overwrite by default. Ask before replacing an existing render.

## Troubleshooting

- `ffmpeg`/`ffprobe` missing: install using trusted Ubuntu packages or official builds; do not fake the metadata result.
- Media path rejected: put the media within the project, or use an explicitly approved root path and update the project tooling's allowlist deliberately. Do not weaken path validation by default.
- MCP server does not launch: check `.mcp.json`, executable path, Python environment, dependency install and Claude Code's `/mcp` error output. Test the server in its own terminal only if the runtime supports MCP stdio protocol inspection.
- Render fails: preserve logs, check input decodability/output free space/available codec, and retry only with a documented compatible option. Don't silently lower quality.
- Kdenlive cannot open or relink a project: protect a copy, verify editor version and paths, and follow the Kdenlive manual's project backup guidance.
