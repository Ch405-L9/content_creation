---
name: socmed-video-production
description: Plan, edit, generate, review, and export social-media videos from source footage using a phase-gated AI-led workflow, FFmpeg, Kdenlive, and optional local MCP tools. Use for short-form video creation, editing, repurposing, captions, platform variants, and production-workspace setup.
---

# Social video production

Drive the project; do not merely describe editing advice. Take initiative on reversible analysis and draft work, preserve originals, explain important trade-offs, and keep the user in control at meaningful creative gates and before publishing or destructive actions.

## Start here

1. Resolve the project root. Use the current directory if it contains `production.json`; otherwise look for the requested project path. If no production workspace exists, run `python3 scripts/bootstrap_workspace.py --target [path]` from the repository root or ask the user to clone the repository first. Never assume the cloud computer can write to the user's Ubuntu home directory.
2. Read `production.json`, any existing brief, prior approved decisions, and the repository README. Do not reset a project that already has assets or edits.
3. Establish the requested outcome, audience, platform(s), duration, aspect ratio, resolution, frame rate, tone, CTA, language, deadline, source rights, and autonomy level. Reuse known choices. Ask only for missing decisions that would materially change the edit. Offer a small recommended default plus 2–3 meaningful alternatives; state the consequence of each. If the user says “take the wheel,” proceed with reversible work using declared assumptions and pause only at the gates below.
4. Read `references/phase-workflow.md` for the full phase sequence and gate behavior. Read `references/creative-and-technical-standards.md` for editorial reasoning, platform-safe composition, accessibility, audio, color, and delivery checks. Read `references/tooling-and-editor.md` before changing editor/project/automation setup. Read `references/repo-assets-and-migration.md` when reusing the supplied repo resources or translating the legacy pipeline JSON.
5. Use the local MCP tools, if configured, for media inventory/probing, timeline validation, draft render, and export QA. Otherwise call the repository scripts with explicit paths. See `references/mcp-and-cli.md`. Never invent an MCP API for Kdenlive: treat Kdenlive as the visual review/editor and its MLT project/render ecosystem as the bridge.

## First principles

- **Story before effects.** Identify the one useful viewer outcome and the central promise. Use the opening to earn attention honestly, then make each beat advance, clarify, prove, or emotionally develop that promise.
- **The viewer's experience is the spec.** Optimize for comprehension, emotional intent, legibility, pacing, and sound on the actual device—not fashionable transitions or maximum effect count.
- **Frame-accurate, source-safe, reversible.** Preserve camera originals; track edits as source references plus in/out points; keep project files, decisions, proxies, renders, and logs separate; version before substantial changes; use non-destructive effects and re-renderable recipes.
- **Evidence over certainty.** Inspect media and rights. Do not infer a person's identity, consent, product claims, dialogue, ownership, or platform performance from filenames. Mark uncertain facts and ask when they matter.
- **Optimize for editability and delivery risk.** Prefer open, documented interchange and standard media tools. Pin output profile, codec, frame rate, color assumptions, and subtitles in project metadata. Validate actual rendered files, not merely command success.
- **Human approval is creative direction.** After each meaningful gate, show concrete choices with a recommendation and why. Do not make the user micromanage deterministic tasks; do not silently lock in major tone, meaning, brand, legal, or publication choices.

## Operating protocol

- Before a phase, say what you will inspect/do and what decision (if any) is needed. After it, summarize completed work, assumptions, issues, and the next gate.
- Offer decisions in plain language, normally: **Recommended**, **Alternative**, **Alternative**. Add an “other” option. State duration/platform impact when relevant.
- For “take the wheel,” pick the safest coherent option for low-risk choices, document it in the brief/decision log, and keep moving. Stop if source ambiguity, licensing/privacy, factual claims, likeness/voice synthesis, sensitive topics, or a major creative branch could cause meaningful harm or wasted work.
- An approval of one phase does not authorize publishing, spending, deleting originals, replacing the only project file, or sharing private media externally. Require explicit approval before those actions.
- Use AI-generated imagery/audio only when requested or approved and label synthetic elements where appropriate. Never fabricate testimonials, news, endorsements, evidence, or a person's voice/likeness without informed authorization.
- Never overwrite a source file. Save drafts/revisions with clear names and keep the last known good version. Avoid broad shell deletion or commands with unbounded path/glob behavior.
- For every recommendation, identify the observed issue, its likely audience effect, the proposed fix, and any trade-off. Separate must-fix errors from subjective polish.
- Treat CLI commands and files as untrusted input. Use argument arrays/subprocesses, not shell-interpolated media filenames. Run only tools and paths required for this project.

## Phase map

Execute in order; combine adjacent mechanical phases only when no creative decision is hidden. The full procedure, choices, gates, and acceptance criteria are in `references/phase-workflow.md`.

1. **Intake & intent** — clarify deliverable, audience, message, platform, rights, constraints, and autonomy.
2. **Workspace & asset safety** — initialize/verify folders, inventory and probe assets, preserve originals, flag missing/corrupt/unlicensed items.
3. **Creative treatment** — propose hook, promise, story beats, emotional arc, CTA, visual/audio style, and success criteria.
4. **Selects & script** — transcribe if needed, identify strongest moments, construct a beat sheet or paper edit with source timecodes; do not fabricate quotations.
5. **Rough cut** — assemble story beats, choose format, establish pacing and readable framing; render a review proxy.
6. **Fine cut & picture** — tighten comprehension/continuity, B-roll, reframing, transitions, visual hierarchy, and motion graphics.
7. **Captions & accessibility** — correct transcript, caption timing/line breaks, contrast and safe placement; preserve an editable caption file when possible.
8. **Sound & color** — clean dialogue, balance music/effects, loudness-check, correct shots, then apply restrained look.
9. **Platform versions** — create separately framed/timed/captioned deliverables from a shared approved master; never stretch aspect ratios blindly.
10. **QC, delivery & learning** — probe and play the actual exports, check all requirements and risks, provide files and concise change log; publishing stays a separate explicit step.

## Execution details

- Confirm `ffmpeg` and `ffprobe` with `command -v`; inspect versions and available encoders/filters before choosing a codec/effect. Use Kdenlive for human review and complex hands-on finishing; automate deterministic operations via the bundled scripts/FFmpeg. Never claim Kdenlive has a native REST API or official MCP unless you verify such an interface in primary documentation.
- Start with source media metadata and a sample playback/checksum. Never move or rewrite camera originals. Copy/reference them into `assets/originals` only when storage policy allows.
- Keep edit decisions in the workspace's JSON/CSV/OTIO files rather than only in a prompt. A draft must be repeatable from source paths, source in/out, timeline order, profile, captions, and explicitly selected effects.
- Use a low-resolution proxy or short representative section to test a pipeline before a full-resolution render. Confirm storage, expected runtime, and destination space before large jobs.
- Do not hard-code one loudness target, caption style, frame rate, font, or bitrate for every platform. Select appropriate delivery requirements, document assumptions, and perform a final platform-specific check.
- Review exports with `ffprobe` and by visual playback (and audio listening where available). A successful process exit is not proof of sync, crop, caption accuracy, intelligibility, rights, or quality.

## Deliver

Provide the final export path(s), project/edit-decision files, caption/transcript files as applicable, profile and codec details, a short QC report, assumptions/known limits, and prioritized improvement suggestions. Make a clear distinction between **must fix before publish**, **recommended**, and **optional polish**. Do not publish or upload unless explicitly requested and separately approved.

## Resource map

- `references/phase-workflow.md` — detailed phases, decision points, and acceptance checks.
- `references/creative-and-technical-standards.md` — first-principles editorial, accessibility, sound, image, and export standards.
- `references/tooling-and-editor.md` — Ubuntu setup and Kdenlive/FFmpeg/MLT/OTIO division of labor.
- `references/mcp-and-cli.md` — optional MCP setup and safe CLI examples.
- `references/repo-assets-and-migration.md` — how to use this repository's existing media/transcripts and fix its legacy pipeline configuration.
- `../../../../docs/ubuntu-workspace.md` — workspace creation, structure, backup, and handoff.
