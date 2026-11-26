# Social Media Video Production Workspace

A Claude Code skill and Ubuntu project scaffold for phase-by-phase, AI-led social video production. It combines a free/open-source desktop editor with deterministic local command-line tools, keeps source media safe, and uses explicit user checkpoints for creative choices.

**New here? Start with [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)** — copy-paste prompts for making a video with Claude.

## Quick start

On the Ubuntu computer where the workspace should live, clone this repository to the requested path and initialize only missing project files:

```bash
git clone https://github.com/Ch405-L9/content_creation.git /home/t0n34781/Projects/socmed_content_creation
cd /home/t0n34781/Projects/socmed_content_creation
python3 scripts/bootstrap_workspace.py
```

If a directory already exists, inspect it and back it up rather than cloning over it. The bootstrapper preserves existing files; it never copies or overwrites source media. Setup details are in [docs/ubuntu-workspace.md](docs/ubuntu-workspace.md).

## Recommended editor and automation

Use **Kdenlive** for visual timeline editing/review. Use **FFmpeg/FFprobe** for reproducible local metadata checks, proxies, constrained draft renders and export validation. Optional **OpenTimelineIO** can represent editorial decisions when a tested adapter is available; it is not a media container or universal Kdenlive project converter. The included optional local MCP server exposes a small allowlisted set of local project/media tools—not a Kdenlive API. See [the tooling decision](.claude/skills/socmed-video-production/references/tooling-and-editor.md), [MCP/CLI instructions](.claude/skills/socmed-video-production/references/mcp-and-cli.md), and [technical sources](docs/technical-decisions.md).

## Claude Code

The skill is at `.claude/skills/socmed-video-production/SKILL.md`. Open Claude Code in the repository/workspace and invoke `/socmed-video-production`. It moves through intake, media safety, treatment, selects, rough cut, fine cut, captions/accessibility, sound/color, platform versions, and QC/handoff. At meaningful gates it offers a recommendation plus alternatives; “take the wheel” lets it proceed on reversible low-risk work, not publish, delete originals, spend money, or expose private media.

## Existing repository material

This repository includes example MP4s, a cinematography PDF and images, production transcripts, and an earlier video-editing JSON. Treat all as references/source candidates only after checking provenance, licensing and relevance. The legacy pipeline values are not a native project for Kdenlive or an executable recipe. Review [repo migration guidance](.claude/skills/socmed-video-production/references/repo-assets-and-migration.md).

## Safety and scope

No media is uploaded by the local scripts. External transcription, media generation, publishing, and sharing are separate decisions requiring explicit user authorization. Project files and originals are preserved; generated drafts and exports go to separate folders. Platform technical specs change, so confirm current official guidance for a real delivery.
