# CapCut AI pipeline — what we learned (The Grant Run)

Distilled from sessions 2026-11-25/26 (49 prompts, ~20 Seedance clips). Full prompts with GOOD/BAD tags:
`docs/prompt_log_2026-11-26.md`. Decisions and file lineage: `edit/decision-log.md`.

## 1. The loop that works (use this every time)

1. **Lock references first.** Car = `edit/car_sheet_m/MUSTANG_DH_M_CAR_SHEET_v2.png` (approved). Speed = black & grey polo +
   matching cap with the official M. Trixie = full character sheet, red & black outfit for the whole series.
   Only use stills/videos/refs that are on the CapCut board "Music Video Stills".
2. **Keyframe first (Design Studio, Nano Banana 2, 14 cr).** One image per request. Upload the board background + car
   refs; say "Location: EXACTLY image 1 … Car: THIS EXACT car from images 2 and 3 …", camera position, direction of travel.
3. **Fix logos locally, not with AI.** The hood M is composited on the keyframe with `edit/tools/hood_m_still.py`
   (exact traced board M, `--vent` slat cut, `--texture` keeps rain beads, matte deep red 142,30,38). Old graphics are
   removed with `edit/tools/clean_red_graphics.py`.
4. **Animate (Video Studio, Seedance 2.0, 720p 9:16 5 s, 85 cr)** with the keyframe as the ONLY image (first-frame mode).
   Describe shots with second ranges and "HARD CUT". State the direction of travel relative to the camera.
5. **Finish locally:** trim/retime to exact frame counts, `delogo=x=12:y=12:w=48:h=38` removes the "Ai" badge, no music,
   no captions. Clips ≤ 5 s; anything longer is split evenly.
6. **Review → log → commit.** Deliverables in `review/…`, originals in `assets/originals/capcut_gen/` (never overwritten).

## 2. Prompt patterns

| Works | Fails |
|---|---|
| One still per request, model named | 5 stills in one request (failed twice) |
| "Edit image N only … ONE change only" | Regenerating to fix identity (faces drift) |
| "Keep EXACTLY the same camera direction and layout as this reference" | "same scene but much LOWER" (camera flipped, RHD look) |
| Explicit LHD geometry: "driver in LEFT seat, RIGHT hand on the console shifter" | Generic "hand on the gear lever" (arms from passenger side) |
| Timed multi-shot: "Shot 1 (0-1.25s) … Shot 2 (1.25-2.5s): HARD CUT …" (cuts land ±0.4 s) | Asking for a camera ARC (ignored — it pushes in instead) |
| "races toward the low camera" / rear chase cam for pull-aways | "pulls away ahead" from a FRONT-facing first frame → car faces camera while shrinking = reads REVERSING |
| "emergency lights", "cinematic high-speed" | "over 100 mph" + police chase wording → CapCut "security error" (credits refunded) |
| First frame only (one image) | First frame + extra reference image → refused in first-frame mode |
| Keyframe built for the exact subject (emblem close-up) | Reference-only video (no first frame) → starts on grey studio, wrong subject |
| Location from a board backdrop image (exact ATL overpass) | Text-only "Atlanta skyline" → generic city |
| Logos composited locally (exact) | Any AI logo edit on a busy frame (outline / wrong M every time) |

## 3. Logo / M rules (car sheet v2)
- Shape = board M traced (`assets/graphics/board_refs/board_M_poly.npy`, w/h 0.83). NOT the old pngegg M (0.59).
- Size = user mock: spans the hood from the windshield-base corners to the hood front edge; the carbon vent slats cut through it.
- Finish = deep red MATTE (approved), no stripes, no "5", no other graphics. Fender: factory Dark Horse emblem only.
- In low front-3/4 views a flat decal looks squashed — that is correct perspective; straight-front/top views read best.
- Video fixes: track the OLD logo's measured position/size (similarity) — affine ECC on smoky club footage drifts/shears.

## 4. CapCut quirks (and the fix)
| Quirk | Fix |
|---|---|
| Progress stuck at 99% / card never finishes in the open page | Wait ~3–4 min total, then reload with force (generation keeps running server-side). Credits dropping = it rendered. |
| Chat says "Failed: Generate videos" but credits were charged | The card usually exists — reload and check the canvas. |
| "The network connection was lost" in Design Studio chat | Reload + New chat + re-upload. Lost result still costs 14 cr. |
| Upload button opens a native file dialog | Patch `HTMLInputElement.prototype.click` to capture the input, then use the file_upload tool on it. |
| Clicking the canvas selects cards / marquee into the prompt | Reload before typing; never click the canvas body before a prompt. |
| Canvas "Download" of a grouped board image → blank transparent PNG | Fetch the board's resource URL in-page and save ONE blob per call (multiple in one call are blocked). |
| Big board → WebGL context loss (images vanish) | Reload the board; nothing is lost. Do generation work in a separate small canvas. |
| Chat download comes down as .jpg not .png | Check `ls -t ~/Downloads` for any extension before assuming it failed. |
| 1080p/4K need a paid upgrade | Never purchase; generate 720p and upscale locally if needed. |
| Video reference must be 640×640 … 834×1112 | Pre-crop/scale; or describe the reference shots in text with timings (worked better). |

## 5. Costs
Seedance 2.0 5 s 720p = 85 credits; **Seedance 2.0 Mini 5 s 720p = 15 credits** (piece 6 quality was fine — try Mini first). Nano Banana image = 14 credits. A 4.6 s escape piece = 14 + 85 ≈ 100.

## 6. Open items (as of 2026-11-26)
- Last chase (Vette ref → Mustang), 6 × 4.6 s: piece 1 done (`review/escape/escape_01_overpass_approach_v1.mp4`); pieces 2–6 next.
- Video 7 redo (side-tracking pull-away) rejected — redo as a rear chase-cam pull-away.
- Video 12 overhead shot (≈1.9–2.5 s) still has CapCut's own M.
- Backdrops A–E, cut scenes, remaining M redos — see the board and `edit/decision-log.md`.

## 7. Video-reference edits (Yuck → Mustang, 2026-11-27)
- Seedance 2.0 Mini accepts a VIDEO reference (scale/crop to 640x1112 for 9:16) + image refs; keeps faces, lip timing, camera.
  Cost 10 cr per 5 s (15 shown with extra refs, actually charged 10). Re-mux the ORIGINAL audio afterwards.
- Character sheets with FACES as refs → failed (likely face-swap filter). Use headless outfit crops
  (edit/yuck_mustang/refs/speed_outfit_body.jpg, speed_cap.jpg, trixie_outfit_body.jpg) — works.
- Text-only outfit change gives a generic block M on the cap; the speed_cap image ref gives the correct M.
- Seedance adds a sports-brand chest logo to "polo" → ask for "plain fabric with no print on the chest".
- ~1 in 2 ref-edits fail at random ("Failed" in chat, card later "Couldn't load content", credits refunded) → just resend.
- "Failed" in chat can be false: check the canvas card (00:05 = rendered). Only ONE generation at a time per project
  (send button greys out while one runs). Reload can show "Update project?" → Update keeps cards.
- Click the card LABEL to select → toolbar Download; selection adds a chip to the prompt (reload to clear, never Ctrl+A).
