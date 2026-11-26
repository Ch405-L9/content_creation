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
- grantrun_finecut_v008 — previous candidate (old opening)
- **grantrun_v009** — current candidate: Mustang intro + v008 from 8.583 s. Rebuild: edit/tools/build_intro_v2.py, then normalize_loudness
| 2026-11-25 | New intro (Mustang) | Met Gala slow-mo intro redo: matte black Mustang Dark Horse + red M hood; Gordon black/grey outfit (user sheet), Trixie red/black (user: keep outfit; face from user's Trixie sheet) | User direction | Pro plan needed for more AI video |
| 2026-11-25 | CapCut | 5 keyframes (Nano Banana 2, 768x1376) in assets/originals/capcut_gen; car clip via Seedance 2.0 Mini (free trial, 720p); other clips blocked by "Upgrade" paywall → FFmpeg push-in/flash motion on stills | No purchases made | User: upgrade or keep stills-motion |
| 2026-11-25 | Preview | review/mustang_intro_preview_v1.mp4 (11.0 s: pendant → Gordon → Trixie → Mustang → both) | For direction approval before splicing into v008 | — |
| 2026-11-25 | Logo | Hood M must be the real Mach 5 M (user-supplied ref: assets/graphics/mach5_logo_ref/); AI image models kept approximating → local composite via edit/tools/hood_logo.py (inpaint old chevron, perspective-warp logo, paint shading) | Exact logo, repeatable | Apply to shot 5 after Trixie fix; car video clip still has old chevron |
| 2026-11-25 | Trixie likeness | Ref = user's sheet (assets/graphics/character_refs/trixie_sheet_official.png): koi/yin-yang back piece, NO neck tattoo, blunt bob + bangs. trixie_shot3_v3 fixes tattoos/hair; face still drifts | — | User: accept v3 or another pass (face-only ref / Character Swap) |
| 2026-11-25 | Trixie | trixie_shot3_v3 accepted ("close enough") | User | — |
| 2026-11-25 | Shot 5 | both_mustang_shot5_v6_plainhood (Trixie = v3 likeness, Gordon outfit restored, plain hood) + Mach 5 logo composite (bold strokes, ahead of the vent) | — | — |
| 2026-11-25 | Shot 4 | Mach 5 logo composite v3 (re-grained inpaint); Seedance car clip retired (old chevron) → still-motion | — | Re-animate if CapCut is upgraded |
| 2026-11-25 | v009 | Mustang Met Gala intro (206 frames) replaces v008 0–8.583 s (old shots 1–6 incl. tach); name cards moved onto new Gordon/Trixie shots; rest of v008 unchanged. 40.000 s, -14.0 LUFS, sync ≤15 ms | Built by edit/tools/build_intro_v2.py | Intro→chase car swap (Mustang→white C8); loop seam now chase→pendant |
| 2026-11-25 | Logo fix | User: car "M" incorrect. Perspective-sheared M read as a squat ribbon → composite now upright to camera, true tall proportions (car_shot4 v5, both_shot5 v3) | Readability over literal hood perspective | White-Vette chase shots still carry the AI chevron (needs per-frame tracking) |
| 2026-11-25 | 5 s clips | review/clips_5s: 01_pendant_v1, 02_gordon_v1, 03_trixie_v1, 04_mustang_v2, 05_gordon_trixie_v3 — 5.000 s, 1080x1920@24, tag on, ~-13..-16 LUFS | edit/tools/build_5s_clips.py | — |
| 2026-11-25 | v010 | Reel rebuilt with corrected logos (review/grantrun_v010.mp4, -14.0 LUFS) | edit/tools/build_intro_v3.py | — |
