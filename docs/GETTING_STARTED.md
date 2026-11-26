# Getting started: making a video with Claude

A short, copy-paste guide. You bring footage and a goal; Claude runs the edit and stops at checkpoints for your approval.

---

## 0. Before each session (30 seconds)

1. Open a terminal in this folder and start Claude Code:
   ```bash
   cd ~/Projects/socmed_content_creation && claude
   ```
2. Type `/mcp` and confirm **socmed-video-production** is connected (9 tools).
3. Optional check — paste:
   > Run project_status and list_media. Tell me if anything is missing.

---

## 1. Add your footage

Copy (don't move) your clips into `assets/originals/`:

```bash
cp ~/Videos/my-shoot/*.mp4 assets/originals/
```

Music goes in `assets/audio/`, logos and images in `assets/graphics/`. Claude never edits or deletes anything in `assets/originals/`.

---

## 2. Start a project — copy one of these prompts

### Option A: Full brief (best results)

```text
/socmed-video-production

New video. Here's the brief:
- Project name:
- Footage: assets/originals/ (all files) — or list specific files
- Platform(s): TikTok / Reels / Shorts / YouTube / LinkedIn / X
- Length: e.g. 30–45 seconds
- Goal: what the viewer should know, feel or do by the end
- Audience: who this is for
- Tone: e.g. energetic, calm, funny, premium, educational
- Call to action: e.g. "Follow for part 2", "Link in bio", none
- Captions: burned-in / separate file / both
- Music: my file in assets/audio/ / none / suggest options
- Rights: footage and music are mine to publish — yes / no / unsure
- Mode: approve each step  OR  take the wheel (stop only at the main checkpoints)
```

### Option B: Quick start

```text
/socmed-video-production
Make a 30-second vertical Reel from the clips in assets/originals/.
Goal: <one sentence>. Audience: <who>. Take the wheel and stop at the main checkpoints.
```

Anything you leave out, Claude fills with a sensible default and writes it down in `briefs/brief.md` so you can change it later.

---

## 3. What happens next (and how to reply)

Claude works in stages. At each **checkpoint** it shows you what it did and gives a recommendation plus alternatives. Reply in plain words.

| Stage | What Claude does | Checkpoint — you decide |
|---|---|---|
| 1. Intake | Reads your brief, asks only what's missing | Approve the direction |
| 2. Footage check | Inspects every file, transcribes speech locally | Only if rights/quality problems turn up |
| 3. Treatment | Hook, story beats, ending, CTA | **Approve the angle** |
| 4. Selects & script | Picks best moments with timecodes | Approve quotes/claims if meaning could change |
| 5. Rough cut | Assembles the story, renders a draft to `review/` | **Approve story and length** |
| 6. Fine cut | Tightens pacing, reframing, B-roll | **Picture lock** |
| 7. Captions | Corrects transcript, styles captions | Check names and spelling |
| 8. Sound & color | Levels loudness, cleans audio, light grade | Only if the look/feel changes a lot |
| 9. Versions | Makes each platform's size/length | **Confirm the deliverables** |
| 10. QC & handoff | Checks the real files, writes a short report | Done — publishing is a separate step |

**Useful replies at any checkpoint:**

```text
Approved, continue.
Go with option 2.
Approved, but make the hook shorter and punchier.
Show me two alternative hooks before you continue.
Take the wheel from here until the rough cut.
Pause — explain the trade-off between options 1 and 3.
```

Watch drafts with any video player, or open them in **Kdenlive** for frame-by-frame review.

---

## 4. Revision prompts

```text
The middle drags — cut 5 seconds between 0:12 and 0:25.
Move the strongest line to the very start as the hook.
Keep the speaker centred when cropping to vertical — she's on the left in clip 3.
Captions: bigger, max 2 lines, keep them above the bottom 20% of the frame.
Music is too loud under the voice — duck it more.
Make a 15-second cutdown from the approved version.
Go back to rough cut v002 — I liked that pacing better.
```

Claude saves a new numbered version each time (`review/roughcut_v003.mp4`, …); earlier versions are kept.

---

## 5. One-off task prompts (no full project needed)

```text
Transcribe assets/originals/interview.mp4 and give me captions (SRT) for review.
Make a vertical 1080x1920 version of assets/originals/wide.mp4 — blur-pad, don't crop.
Normalize the loudness of review/final_v004.mp4 for Instagram.
Inventory everything in assets/originals/ and flag any problems.
Check exports/reel_final.mp4 against the vertical 1080x1920 profile.
Find the 3 strongest 15-second moments in this transcript for clips.
Write 3 caption + hashtag options for this video.
```

---

## 6. Where everything ends up

| Folder | Contents |
|---|---|
| `assets/originals/` | Your untouched source footage |
| `assets/proxies/` | Lightweight working copies |
| `transcripts/` | Draft and corrected captions (`.srt`, `.vtt`, `.json`) |
| `briefs/brief.md` | The brief and assumptions |
| `edit/` | Timeline, Kdenlive project, `decision-log.md` |
| `review/` | Draft renders for you to watch |
| `exports/` | Approved final files |
| `logs/` | Inventory and QC reports |

---

## 7. Ground rules Claude follows

- Never changes, moves or deletes your originals.
- Never overwrites an approved file — always saves a new version.
- Never uploads, publishes, spends money or sends your media to an online service without asking first. Transcription runs on this computer.
- Asks before using AI-generated faces, voices or footage, and labels them.
- Flags unclear rights (music, footage you didn't shoot, people who haven't agreed to appear).

---

## 8. If something goes wrong

| Problem | Fix |
|---|---|
| `/mcp` doesn't show the server | Restart Claude Code in this folder and approve the server |
| Transcription fails | `.venv/bin/python -m pip install -r .claude/skills/socmed-video-production/requirements-transcribe.txt` |
| "refusing to overwrite" | Expected — ask for a new version name, e.g. `_v004` |
| "path must stay inside the project root" | Copy the file into `assets/` first |
| Draft looks wrong / out of sync | Tell Claude what you see and the timecode; it keeps the previous version |

That's it — copy a prompt from section 2 and go.
