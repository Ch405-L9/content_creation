# Decision log

| Date (UTC) | Phase | Choice/approval | Rationale or impact | Open item |
|---|---|---|---|---|

## Revision history
Record the name/path of each meaningful revision, what changed, and which previously approved version remains recoverable.

| 2026-11-25 | Intake / media | Copied 26 quarter-final clips, 11 ZR1X sound clips, 52 stills into assets (originals untouched, sha256 logged) | Main pool = AI renders; inspiration/caranddriver/IG screenshots/commercial songs kept as reference only | SFX provenance |
| 2026-11-25 | Treatment (draft) | Shot list v001 + 3 storyboard sheets (review/storyboards_v002) | 20 shots / 40.0 s / 24 fps; cold open → cards → run → drop → secret → loop | Gate A/C approval; IP trade dress; music; AI label |
| 2026-11-25 | Gate A/C | Open non-commercial fan tribute; cast approved (red M cap = Gordon, pink = Trixie); YUCK_clips usable | User decision | — |
| 2026-11-25 | Defaults | No commercial music baked in; on-screen tribute/AI/fiction tag + not-affiliated line | Recommended defaults, user did not object | — |
| 2026-11-25 | Gate E | Rough cut **v002** chosen (review/grantrun_roughcut_v002.mp4) | User: "all are good, choose"; v002 = v001 timing + text-layout fixes | Fine cut next |
| 2026-11-25 | Fine cut | No dialogue captions (user: "audio and visuals, professional level"); title cards kept; Nimbus Sans Narrow Bold, shadow, fades | User direction | — |
| 2026-11-25 | Sound | Synth trailer design (assets/audio/sfx_synth: boom, sub-drop, whoosh, riser, heartbeat, tape-stop, drone) + ZR1X engine clips; cue sheet edit/finish_v008/cue_sheet.json | No usable SFX library locally; synth = no licensing risk | More real car foley (user to source) |
| 2026-11-25 | QC fixes | Renderer AAC-per-segment drift (~0.67 s by end) fixed (PCM segments); shots snapped to frames; single-pass a/v mix dropped last 0.5 s → separate picture/mix + mux | Lip-sync and seamless loop | — |
| 2026-11-25 | Gate F (pending) | **review/grantrun_finecut_v008.mp4** — 40.000 s, 1080x1920@24, -14.0 LUFS, -2.35 dBTP, sync ≤ 13 ms | Candidate for picture lock | User review |

## Revision history
- grantrun_roughcut_v001/v002 — hard-cut rough cuts with captions (v002 approved)
- grantrun_finecut_v003 — first grade/mix (superseded: renderer A/V drift)
- grantrun_finecut_v005/v006/v007 — superseded (tail-silence bug); kept for comparison
- **grantrun_finecut_v008** — current candidate. Rebuild: render edit/timeline_grantrun_v004.json → edit/tools/finish.py → normalize_loudness
