# Technical decisions and sources

Research checked on 2026-11-25. The official Kdenlive download page showed release 26.08.3 at that check; recheck release-specific behavior and platform delivery rules before a future production.

## Kdenlive and MLT

Kdenlive's official manual describes `.kdenlive` files as XML based on MLT, says project files reference most external media, and notes MLT can render the project while ignoring Kdenlive-specific editing data. It also warns that project file versions evolve and newer files may not open in older versions. Therefore the project file remains the human-editable source of truth when Kdenlive is used; automation uses tested MLT/FFmpeg operations and preserves versioned copies. Kdenlive documents terminal rendering of generated `.mlt` scripts with `melt`.

Sources: [Kdenlive project file details](https://docs.kdenlive.org/en/project_and_asset_management/file_management/project_files.html), [Kdenlive rendering](https://docs.kdenlive.org/en/exporting/render.html), [Kdenlive official downloads](https://kdenlive.org/download/), [Kdenlive KDE application listing](https://apps.kde.org/kdenlive/).

## Claude Code skills and MCP

Claude Code documents skills as a `SKILL.md` with YAML frontmatter and Markdown, project skill location `.claude/skills/`, and supporting files loaded as needed. Its docs distinguish Claude Code-specific frontmatter from fields available to other Agent Skills consumers. Project-scoped MCP servers can run local stdio processes; trust and configuration should be reviewed rather than silently enabled.

Sources: [Claude Code skills](https://code.claude.com/docs/en/skills), [Claude Code MCP](https://code.claude.com/docs/en/mcp).

## OpenTimelineIO and FFmpeg

OpenTimelineIO describes itself as an API/interchange format for editorial cut information and says timeline media is referenced externally rather than embedded. Adapter availability is tool/format-specific, so the project uses OTIO only when a verified adapter matches the installed workflow. FFmpeg and FFprobe are the command-line processing and machine-readable inspection layer; their current docs are linked below.

Sources: [OpenTimelineIO overview](https://opentimelineio.readthedocs.io/en/latest/), [OpenTimelineIO adapters](https://opentimelineio.readthedocs.io/en/latest/tutorials/adapters.html), [FFmpeg documentation](https://www.ffmpeg.org/documentation.html), [FFprobe documentation](https://ffmpeg.org/ffprobe.html), [FFmpeg filters](https://ffmpeg.org/ffmpeg-filters.html).

## License and media rights

Kdenlive is free/open-source software; verify license notices in its official downloads/source package. The GitHub repository currently has no declared repository license in its public API metadata. This is not proof that bundled videos, images, transcripts or documents are freely reusable. Confirm each asset's provenance and permission before public reuse.
