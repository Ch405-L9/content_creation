# Ubuntu workspace setup

The intended production workspace is `/home/t0n34781/Projects/socmed_content_creation`. This repository was prepared in an isolated build environment; it cannot directly create files under that path on the user's Ubuntu computer. Clone or copy the repository onto that Ubuntu system, inspect the bootstrapper, and run it there:

```bash
git clone https://github.com/Ch405-L9/content_creation.git /home/t0n34781/Projects/socmed_content_creation
cd /home/t0n34781/Projects/socmed_content_creation
python3 scripts/bootstrap_workspace.py
```

If the directory already exists, do **not** clone over it. Run `git -C [existing-path] status` and back it up first. The bootstrapper is idempotent: it creates missing folders and copies missing template/skill files without replacing existing files. It does not download media, copy originals, install applications, or change permissions. If the target differs, pass `--target /absolute/path`. Inspect existing files before any migration.

## Layout

```text
socmed_content_creation/
├── .claude/skills/socmed-video-production/  # Claude Code skill and bounded local tools
├── assets/originals/                       # source media; preserve unchanged
├── assets/proxies/                         # generated low-resolution working copies
├── assets/audio/                           # approved narration, music, SFX
├── assets/graphics/                        # approved titles, logos, stills
├── briefs/                                 # intent, rights, decisions and constraints
├── transcripts/                            # source transcript and corrected captions
├── edit/                                   # Kdenlive project, timeline/EDL, decision log
├── review/                                  # clearly labeled draft renders
├── exports/                                 # approved final masters and delivery variants
├── archive/                                 # project snapshots/closed deliverables
└── logs/                                    # inventories, render logs, QC reports
```

Large source media should live in the project only if disk/backup policy allows it. Relative links or a separate source volume may be preferable. Back up project files and source media independently; a Kdenlive project references media rather than embedding most sources.

## Free/open-source editor and tooling

Recommended human editor: **Kdenlive**. Automated inspection/transcoding/rendering: **FFmpeg** and **FFprobe**. Install via the user's preferred trusted Ubuntu channel; see [tooling-and-editor.md](../.claude/skills/socmed-video-production/references/tooling-and-editor.md). Test installed versions and codecs before a production edit. Kdenlive's project file uses an MLT-based XML format and is human-editable in Kdenlive; do not blindly rewrite its XML or assume backwards compatibility.

## Claude Code

Open Claude Code from the workspace root. Invoke `/socmed-video-production` or describe the editing task. The project skill guides the AI through the phases and checkpoints. Optional MCP configuration is project-scoped and should be reviewed before it is trusted. Install its isolated dependencies only when needed. The MCP server does not expose Kdenlive's UI; it wraps a small set of local file/FFmpeg operations.

## Quick health checks

```bash
python3 --version
ffmpeg -version
ffprobe -version
kdenlive --version
python3 .claude/skills/socmed-video-production/scripts/media_inventory.py --root . --output logs/media_inventory.json
```

Missing editor commands are not a reason to modify the user's system automatically. Present installation choices and obtain approval before package installation or elevated commands.
