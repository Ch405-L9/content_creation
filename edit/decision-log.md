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
| 2026-11-26 | Phone zoom shot | User: tighter handheld phone shot from the interior angle, lower, quick zoom tight on his face, standard → dutch, shaky, blurry until focus. New low-angle LHD keyframe chase_C3_lowangle_v1.png (first try rejected: camera faced him = RHD) → Seedance push-in (chase_C3_phone_zoom_seedance_v1, 0.9–4.9 s @1.6x) → edit/tools/phone_cam.py (keyframed digital zoom, roll 0→-17°, hand shake + road vibration, AF hunt blur peak at the zoom, exposure nudge, grain; spec edit/phone_specs/c3_phone_zoom_v1.json) → review/cutscene/phone_zoom_v1.mp4 (2.5 s, -14 LUFS) | — | Not yet placed in a sequence |
| 2026-11-26 | Hood M style | User: M about the size/layout of the AI M on the tracking shot (wide, low, forward on the hood), darker deeper red, matte flat, with a high-gloss red pinstripe AROUND the M (user sketch file arrived blank/transparent). hood_logo_video.py: --box (fit AI-M footprint), --outline gap/width ring, gloss shading + specular, hood pinstripes glossy. Matte fill (92,8,14), gloss (228,24,34). Applied to fly-by (chase_A_..._mach5_v2) AND tracking shot (chase_B_..._plateblur_mach5; detection window moved off the headlight DRL) | User | — |
| 2026-11-26 | Outputs | review/cutscene/exit_chase_v5.mp4, full_with_interior_v3.mp4 | Supersede v4 / v2 | — |
| 2026-11-26 | Club hand routine | User: Speed doing the exact hand movements of ~/Desktop/speed_create_now-HIGH-prio-01.mp4 (relaxed like the ref), Trixie lovingly at his side → eye-roll "wanna-be thug" to cam; party-goers; low handheld phone, pan/push-in to close (not extreme); stay true to char sheets; NO audio, NO text, 9:16 2K, ≤ ref length (8.27 s). Keyframe club_hands_key_v1.png (refs: gordon_walk_shot2, trixie_shot3_v3, both_shot5) → Seedance 2.0 8 s 720p with the ref clip (cropped, silent, 704x1108) as choreography-only reference (88 credits). 4K/1080p need a CapCut upgrade — not purchased; upscaled locally. edit/tools/finish_2k_silent.sh: delogo CapCut AI badge, 1440x2560, sharpen, no audio, no text → exports/club_hands_speed_trixie_2k_v1.mp4 (8.0 s) + review/..._share.mp4 | Choreography matches beat-for-beat | Trixie gives a side-eye + smirk rather than a full eye roll |
| 2026-11-26 | Car + door shot | User (on Video 1 / car_shot4_seedance_v1): fix the hood M as requested, car exactly per the authoritative sheet, Speed walks to the driver side in the last ~2 s and opens the door just before the cut; keep dramatic slow-mo angles, 4 angles (3 new) in the first 4 s, no angle repeated, no shot over 1 s; total 5 s; same res/dimensions/quality. New keyframe club_car_exact_key_v1 (refs S01_B_edit1_APPROVED + VIEW02_side_driver, nose left / driver side to camera) → true Mach 5 M composited (matte deep red + gloss outline, front of hood; hood_logo_video.py --place) → assets/proxies/club_car_exact_key_v1_mach5.png → ONE Seedance 2.0 multi-shot generation (5 cuts; refs: keyframe, gordon_ref, side view; 85 credits). Seedance kept the composited M in shot 1 and a matching M in the overhead shot. Re-timed every shot to exactly 24 frames (minterpolate slow-mo on shots 2/3/5), delogo CapCut badge, 720x1280 @24, 120 frames, audio bed = Video 1 club ambience → review/car_door_multishot_v3.mp4 | v1/v2 superseded (frame-count/cut drift) | Door only just begins to open at the cut |

## 2026-11-26 — Mustang authoritative car sheet v1 (board "Music Video Stills")
- User direction: Vette is reference for the hood 'M' ONLY. Drop all custom pinstripes/colours; the black 2026 Mustang Dark Horse
  from the board car sheet + ONE gloss red 'M' on the front of the hood (Vette red, smaller than the Vette's), no 5, no other graphics.
- Board car sheet images matched by signature to local files: S01_B_edit1_APPROVED (+ its mirror), VIEW02/VIEW03 side views.
- Board M traced from the board render (880x1024) -> assets/graphics/board_refs/board_M_logo_outline.txt / board_M_poly.npy /
  board_M_logo_traced.png (wider than the old pngegg M: w/h 0.83 vs 0.59). The board M is now the only M source.
- Red hood/roof pinstripes removed by inpainting; M painted flat on the hood plane with edit/tools/hood_m_still.py
  (centre 340,432; across 116,14; down -96,66 on the 1671x941 front 3/4). Passenger 3/4 = mirror with the pony badge un-mirrored.
- Outputs: edit/car_sheet_m/SHEET_01..04 (+ front / top-down views generated next, M re-composited exactly).
- Standing rules from the user: Speed = black & grey polo + matching cap with the official M, the NEW Mustang. Trixie = full
  character sheet, red & black outfit for the entire series. Use only stills/videos/refs on the CapCut board.
- v2 (user-approved look, "Thats what I wanted"): LARGE deep red matte M spanning the hood from the windshield-base corners to the
  hood front edge, the carbon vent slats cutting through it (user mock edit/car_sheet_m/user_M_size_mock.png).
  Front 3/4 = CapCut/Nano Banana edit made by the user (assets/originals/capcut_gen/carsheet_front34_bigM_matte_user_v1.png);
  passenger 3/4 = mirror with pony un-mirrored; straight front = hood_m_still.py composite (--vent slat cut, matte, colour 142,30,38).
  Top-down view dropped (CapCut chat would not apply the edit). Sheet: edit/car_sheet_m/MUSTANG_DH_M_CAR_SHEET_v2.png.
  This sheet is now THE authoritative car reference; all M shots (incl. every chase shot / Video 13) get redone to match it.
- 2026-11-26 Redo #1 (Video 13, rain chase): CapCut image edit gave a wrong outline 'M' -> rejected. Keyframe made locally instead:
  stripes inpainted + regrained, exact M composited (hood_m_still.py --texture 0.9 keeps rain beads; vent slat cut).
  Seedance 2.0 first-frame only (it accepts one image when first-frame is used), 5 s 720p 9:16, 85 credits.
  -> review/redo_M/01_video13_chase_M_v1.mp4 (badge removed, generated rain audio kept, no music/text).
- 4-shot speed version of Video 13 (front charge / wheel side / drone overhead / rear under gantry), one Seedance multi-shot gen, 85 cr -> review/redo_M/02_video13_4shot_speed_v1.mp4. Video 14 (Video 7 redo) REJECTED: car faces camera while receding (reads as reversing).
- Video 12 fix (user: "just the first 1.233 s"): frames 1-30 (shot 1) only. Old small M + vent/roof pinstripes removed
  (clean_red_graphics.py, --grain 0.25), exact board M fitted to the hood on frame 1 (affine from cowl corners / vent / front edge,
  edit/video12_M/f0_CAD.npy) and moved with the old M's measured path + size (similarity; ECC affine drifted/sheared).
  Frames 31-121 untouched, original audio. -> review/redo_M/03_video12_Mfix_first1233ms_v1.mp4 (badge removed).
- Pony emblem close-up: keyframe via Nano Banana (low, high-gloss chrome pony, club garage), Seedance first-frame slow push 5 s (Video 17), used 3.0-5.0 s -> review/redo_M/04_pony_emblem_slowmo_2s_v1.mp4. Video 16 rejected (wheel/fender, studio start). Research: no Ford 'SE' package found; Dark Horse has factory Dark Horse fender emblems (black/gray); Dark Horse SC only an interior SC IP badge.

## 2026-11-26 — Last chase ("Cops Lose! Speed Wins"): Vette reference -> Mustang, 6 x 4.6 s (27.6 s split evenly)
- Reference: ~/Desktop/speed_create_now-HIGH-prio-00.mp4, picture cropped 590x420+314+106 -> assets/proxies/refs/vette_escape_ref_cropped.mp4
  cuts 1.9 / 6.97 / 8.9 / 16.73 / 23.83 s. Pieces: 0-4.6, 4.6-9.2, 9.2-13.8, 13.8-18.4, 18.4-23.0, 23.0-27.6.
- ATL backgrounds pulled from the board (in-page fetch, letterbox cropped): assets/graphics/board_refs/board_bg_atl_overpass_interstate.png,
  board_bg_D_atl_skyline_highway.png.
- Piece 1: Nano Banana keyframe (Mustang rear 3/4 under the board's ATL overpass) -> Seedance first-frame, 2 shots (85 cr).
  Re-timed to the reference: shot 1 46 f + shot 2 64 f = 4.58 s -> review/escape/escape_01_overpass_approach_v1.mp4.

## 2026-11-26 — Escape chase pieces 3, 4, 6 (storyboard-first)
- User asked for pieces 3, 4 and 6 only, with a per-second storyboard approved before any credits were spent.
  Storyboards: `review/escape/storyboard_piece3_v1.jpg`, `storyboard_piece4_v1.jpg`, `storyboard_piece6_v1.jpg` → `storyboard_piece6_v2.jpg`
  (user: shots 2–4 good; replace the shifter ending with the Mustang rocketing past the still, low, handheld cam). 3 and 4 approved as is.
- Piece 3 location: user pointed to `~/Desktop/scene-by-scene/` → `shot02_still_v3.jpg` (gas station, front at pump), copied to
  `assets/graphics/board_refs/gas_station/`.
- Piece 3 keyframe: Nano Banana edit "Edit image 1 only … ONE change only: replace the white car with THIS EXACT car from image 2 …
  hood plain" → `assets/originals/capcut_gen/escape_p3_gas_key_v1.png` (GOOD, plain hood as asked).
  An accidental click on a CapCut suggestion chip ("Increase wetness of pavement") started a 2nd edit; stopped, but 14 cr were still charged.
- M composited locally: `hood_m_still.py --center 790 1300 --across 420 0 --down 0 152 --color 142 30 38 --gloss 0.05
  --shade-max 1.08 --texture 0.5` → `edit/escape_p3/key_M_v2.png` (v1 with across 600 was too wide vs the car sheet).
- Piece 3 video: Seedance first-frame only, 3 timed shots → `escape_p3_seedance_v1.mp4` (Video 19). Cuts landed at 2.375 s and 3.85 s.
  Frames 5–114 kept (110 f = 4.583 s), delogo → `review/escape/escape_03_gas_station_highway_v1.mp4`.
- Piece 4 keyframe: board BG D (ATL skyline highway) + car refs, rear chase cam → `escape_p4_key_v1.png` (GOOD).
- Piece 4 video: Seedance first-frame only (escape_p4_key), 3 timed shots → `escape_p4_seedance_v1.mp4` (Video 20); cuts ≈1.7 s and 2.875 s.
  Frames 0–109 (4.583 s), delogo → `review/escape/escape_04_rear_chase_side_v1.mp4`.
- Piece 6 keyframe: board overpass BG + car refs, rear three-quarter wide, driving away under the overpass →
  `escape_p6_key_v1.png` (GOOD) → upload copy `capcut_inputs/escape_p6_key.jpg`. Video NOT generated: 49 credits left,
  Seedance needs 85. Prompt ready (storyboard_piece6_v2): 0–0.8 s drive-away; HARD CUT low static curb cam, headlights approach
  and flood the lens; same handheld low cam, no cut, the Mustang rockets past right beside the lens; ends on shrinking tail lights.
- Note: in Design Studio only 2 of 3 uploaded chips showed (front34_bigM_APPROVED seemed to drop); results still matched the car.

## 2026-11-26 (later) — Escape piece 6 done with Seedance 2.0 Mini
- 75 credits available (< 85 for Seedance 2.0); user said "use seedance if credits an issue" → Seedance 2.0 Mini, 15 cr (75 → 60).
- Original: `assets/originals/capcut_gen/escape_p6_seedance_mini_v1.mp4` (Video 21, 121 frames). Storyboard v2 beats all landed:
  drive-away under overpass → HARD CUT (1.25 s) low curb cam, headlights approach → same cam, Mustang rockets past, spray, shake,
  tail lights shrink.
- Deliverable: `review/escape/escape_06_overpass_flyby_v1.mp4` = frames 11–120 (110 @24, 4.583 s), cut now at 0.79 s (storyboard 0.8),
  delogo 12/12/48/38, no audio.
- Known issue: during the approach (~3.0–3.3 s in the deliverable) the hood M is a smaller red M band near the windshield, not the
  car-sheet big M. Visible ~0.4 s with blur. Fix option if rejected: tracked local M composite on those frames.

## 2026-11-26 (night) — "Next shot" from 5 user reference clips (exports/the_*.mp4)
- Refs: build_up 1.17 s, speed 1.88 s, shift_down 1.47 s, victory 1.15 s, calm 0.70 s = 6.33 s (TikTok screen caps,
  letterboxed 1080x788 @ y=664 in 1080x1920; handle + "Following" removed with delogo). Clean refs: assets/proxies/refs/next_shot/.
- Storyboard: review/storyboard_next_shot_v1.jpg. User: "Two shots for the FULL time" → split on the ref's own cut at 3.03 s.
- Pixel-exact video edit (upload ref video to Gemini Omni) BLOCKED: "uploaded video … isn't available in your region".
  Fallback: per-setup first frame taken from the ref, Vette → car-sheet Mustang via Nano Banana 2.1 (AI Studio, badgch PRO,
  no API key = plan quota), then animated with the ref's camera move described, retimed to the ref's exact frame counts @30.
  Keys + clips: assets/originals/aistudio_gen/next_shot/. Flash still shows the big matte M with vent slats.
- Build-up + speed: Gemini Omni 1.2 Flash 3 s (then Omni daily limit hit). Shift-down + victory: CapCut Seedance 2.0 Mini 16:9
  (15 cr each, 60 → 30). Calm: CapCut refused twice ("security restriction", credits returned) → LOCAL placeholder from the
  calm keyframe (drift + grade), regenerate when Omni resets.
- Retime: edit/next_shot/retime.sh (pts scale + atempo, exact frames). Luma matched per part to the ref segment (lutyuv).
  CapCut "Ai" badge delogo x=14 y=12 w=36 h=36 on 1280x720. Output in the ref's letterbox: 1080x608 picture at y=754.
- Deliverables: review/next_shot/next_shot_A_buildup_speed_v1.mp4 (91 f) and next_shot_B_shiftdown_victory_calm_v1.mp4 (99 f),
  30 fps, car sounds only (model audio, loudnorm -14), no music/captions.
- Incident: Ctrl+A/Delete in CapCut while the prompt wasn't focused deleted canvas cards; undone immediately (Undo). Never use Ctrl+A there.

## 2026-11-27 — Next shot v2 (camera-language prompts, Arena first)
- Pushed 25 commits (user go). Method: docs/chase_camera_language.md (rig → plain camera wording, speed cues, one move per shot).
- Arena video battles (2/day cap): build-up → A kept (B added cuts, 10 s). Speed → user: "B is WAAAAAAYY better";
  B had a red M on the DOOR → Arena Edit on B; edit result A removed it (plain sides), edit result B left a red stripe (rejected).
  Door M appears at ~1.5 s in the original, so the whole edited clip is used (not original 0–2 s + edit).
- Omni 1.2 Flash (16:9, 720p, 4 s): shift-down v2 OK; victory v2 REJECTED (prompt said "tripod" → tripod rendered); victory v3 OK;
  calm v2 OK (replaces the local placeholder).
- Build: edit/next_shot/build_v2.sh → review/next_shot/next_shot_A_buildup_speed_v2.mp4 (91 f),
  next_shot_B_shiftdown_victory_calm_v2.mp4 (99 f). Luma k: 0.874, 0.735, 0.871, 0.888, 1.131. Sources in
  assets/originals/arena_gen/next_shot/ and assets/originals/aistudio_gen/next_shot/ (omni_*_v2/v3).

## 2026-11-27 — Yuck clips → Mustang interior, night (CapCut)
- Found: assets/originals/quarterfinals/YUCK_clips/S1–S8 (+ Desktop copy). S7 = lips macro, no car. All have lip-synced lyrics.
- User: "use capcut". Method: Seedance 2.0 Mini, clip as video reference (scaled 640x1112), prompt = keep everything,
  change only cockpit → 2026 Mustang Dark Horse + late night; red seat accents kept. Cost 10 cr per 5 s.
- S1 0–5 s done: assets/originals/capcut_gen/yuck/S1_0-5_mustang_night_seedmini_v1.mp4 → delogo, 1080x1920, ORIGINAL audio
  re-muxed → review/yuck_mustang/S1_night_selfie_0-5_mustang_v1.mp4. Performance/lip timing preserved. Awaiting review.
- S1 5–10 s done (Video 29, 10 cr; balance 210 after the 200 welcome bonus): review/yuck_mustang/S1_night_selfie_5-10_mustang_v1.mp4.
  Refs for S2–S6, S8 (0–5, 5–10) prepped in edit/yuck_mustang/refs/.
- User (2026-11-27): Speed in black/grey outfit + black M cap, Trixie red&black with the red jacket OFF, per the authoritative sheets; redo S1.
  Face-sheet refs failed (filter) → headless outfit crops work (refs/speed_outfit_body, speed_cap, trixie_outfit_body).
  S1 0–5 v3 (Video 35) + S1 5–10 v2 (Video 34) DONE: review/yuck_mustang/S1_night_selfie_{0-5_mustang_v3,5-10_mustang_v2}.mp4.
  (0–5 v2 = Video 31 had a sports-brand chest logo; superseded.) (A "30 credits" reading was a UI glitch; balance 160 before S2.)
- S2 0–5 s DONE (Video 36): CapCut left a white ring + dark disc where the "5" roundel was → local OpenCV inpaint
  (edit/yuck_mustang/remove_door_ring.py, lower 20% band, large bright/dark components only) → review/yuck_mustang/S2_window_hero_0-5_mustang_v1.mp4.
- S2 5–10 s (Video 37): no roundel visible; paint came out light silver-grey instead of matte black → flagged to user
  (regen 10 cr if wanted). review/yuck_mustang/S2_window_hero_5-10_mustang_v1.mp4.
- S3 0–5 s (Video 38): roundel ("24") removed locally (remove_door_ring.py now has a 2nd pass for leftover digits);
  paint again warm grey metallic despite "deep MATTE BLACK, not silver/grey" → asked user before spending more.
  review/yuck_mustang/S3_arm_out_window_0-5_mustang_v1.mp4.
- S3 5–10 s (Video 39): paint finally BLACK with the wording "painted flat jet black, dark as the night sky" → new template.
  Local paint-darken attempt (edit/yuck_mustang/darken_paint.py) looked blotchy — not used. Re-roll S2 5–10 / S3 0–5 with new wording.
- S4 0–5 (Video 40): night OK, hood black + red M but M reads like the old chevron outline; cap brim brownish → flagged.
- S4 both halves: Video 41 kept the white Mach-5 hood; hood is static in frame → edit/yuck_mustang/hood_fix_static.py builds a
  matte-black hood plate + board M (hood_m_still.py, matte 142,30,38, driver-seat view) and composites it on all frames of
  both halves → review/yuck_mustang/S4_his_mirror_mouth_{0-5,5-10}_mustang_v2.mp4. Cap brim in mirror still light (flag).
- S5 0–5 (Video 42): night + new cluster; Corvette flags stayed on the hub → edit/yuck_mustang/wheel_badge_plate.py (inpaint + chrome pony from emblem_key_v1) static plate. review/yuck_mustang/S5_her_mirror_mouth_0-5_mustang_v1.mp4
- S5 5–10 (Video 43) + 0–5 redone: hub inpaint area widened (no flags remnant). review/yuck_mustang/S5_her_mirror_mouth_{0-5,5-10}_mustang_v1.mp4
- S6 0–5 (Video 44) DONE clean: review/yuck_mustang/S6_her_in_front_0-5_mustang_v1.mp4
