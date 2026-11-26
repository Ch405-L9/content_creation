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
| 2026-11-25 | Exit-chase cutscene | Prompt pack edit/prompts/cutscene_exit_chase_v1.md: Shot A fly-by (1.3 s), Shot B tracking orbit + pull-away (3.0 s) replicating source choreography with Mustang + rainy GSP highway BG; Shot C interior manual shift (1.5 s, separate prompt). Refs in assets/graphics/scene_refs | Choreography from third-party clip used as reference only | CapCut keyframe gen failed twice ("network connection lost") — possibly content filter; manual-vs-SC authenticity; left- vs right-hand shift |
| 2026-11-26 | Cutscene video gen | Seedance 2.0 (720p, 9:16, 5 s) image-to-video on the 4 keyframes: chase_A_flyby, chase_B_tracking, chase_C1_footwell, chase_C2_shifter `_seedance_v1.mp4` in assets/originals/capcut_gen (85 credits each; 1 B attempt failed with "security error", credits refunded, retried with "emergency lights" wording) | — | — |
| 2026-11-26 | Cutscene edit | edit/tools/build_cutscene.py: A 2.20–3.90 s @1.3x (31 f), B 0.20–5.00 s @1.6x (72 f), C1 0.00–0.66 s (16 f, avoids glitch frame at 0.67 s), C2 2.25–3.25 s @1.2x (20 f). Night-rain grade (lifted in v2), 1.65x upscale + crop (drops corner AI badge; our AI-GENERATED tag stays on). Sound: Seedance rain/road bed + zr1x pass-by / cockpit / high-rpm + synth far siren (assets/audio/sfx_synth/siren_wail_far_6s.wav) | — | — |
| 2026-11-26 | Plate | Generated rear plate showed semi-readable fake characters → tracked blur (edit/tools/blur_track.py) → assets/proxies/chase_B_tracking_seedance_v1_plateblur.mp4 | Avoid matching a real plate | — |
| 2026-11-26 | Cutscene outputs | review/cutscene/exit_chase_v3.mp4 (4.29 s, A+B), interior_shift_v1.mp4 (1.50 s, C1+C2), full_with_interior_v1.mp4 (5.79 s, A→C1→C2→B); all -14.0 LUFS, 1080x1920@24 | exit_chase v1 (too dark) and v2 (plate visible) superseded | Hood M in A is the AI version (brief, motion-blurred); C2 arms enter from frame right (RHD-ish geometry); not yet spliced into the reel |
| 2026-11-26 | User review | Vid 6 shifter: wrong geometry (arms from passenger side / driver "sideways"); Vid 4: reads as reversing near the end; Vid 2 hood M wrong — make it slightly bigger like the Vette's, matte deep red; retry Video 3 | User | — |
| 2026-11-26 | Hood M (fly-by) | edit/tools/hood_logo_video.py: per-frame AI-M detection (frames 50–63) → quadratic path (linear extrapolation beyond), inpaint, true Mach 5 M flat on the hood (w/h 0.95, 0.82 far-edge taper, width ≈ AI M width, bold strokes), matte deep red (132,14,22), pinstripes recoloured, motion blur from tracked velocity → assets/proxies/chase_A_flyby_seedance_v1_mach5.mp4 | Exact logo | Video 1 (Met Gala car Seedance clip) still has the AI chevron; not used in any output (intro uses the still-motion composite) |
| 2026-11-26 | Tracking | Video 4 source 3.45–4.0 s slides back up the car (reads as reversing) then jumps ahead → cut out; B = 0.20–3.45 s @1.6x (48 f) + hard cut to pull-away 4.02–5.04 s (24 f). "Video 3" had never rendered (refused/refunded attempt); new take Video 7 (chase_B_tracking_seedance_v2) rejected: car faces camera while receding (drives backwards) + AI M | — | — |
| 2026-11-26 | Shifter | New keyframe chase_C2_shifter_v2.png (LHD: driver left seat, left hand on wheel, right hand on console shifter) → Seedance v2 (Video 8); C2 = 0.50–1.33 s | — | — |
| 2026-11-26 | Cutscene outputs | review/cutscene/exit_chase_v4.mp4 (4.29 s), interior_shift_v2.mp4 (1.50 s), full_with_interior_v2.mp4 (5.79 s); -14 LUFS | Supersede exit_chase_v3, interior_shift_v1, full_with_interior_v1 | — |
