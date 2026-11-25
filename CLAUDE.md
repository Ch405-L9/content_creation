# Production workspace instructions

Use the project skill at `.claude/skills/socmed-video-production/SKILL.md` for social-video work. Read `production.json`, `briefs/brief.md`, and `edit/decision-log.md` before making changes. Follow the skill's phases and user approval gates.

Keep original media under `assets/originals/` unchanged. Put proxies in `assets/proxies/`, new narration/music/FX in `assets/audio/`, graphics in `assets/graphics/`, transcripts in `transcripts/`, projects and decisions in `edit/`, review renders in `review/`, final output in `exports/`, and logs/QC reports in `logs/`. Use relative paths where possible.

Do not publish, upload, spend money, delete originals, overwrite the only good project, or send private media to a remote service without explicit approval. Never run arbitrary commands or FFmpeg filter strings derived from untrusted project data. Save new versions instead of overwriting approved outputs.
