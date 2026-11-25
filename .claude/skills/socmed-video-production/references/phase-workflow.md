# Phase-by-phase production workflow

Use this as a gated operating procedure, not a rigid bureaucratic checklist. Do mechanical work without interrupting the user. Ask a small number of high-value questions at each creative gate. Record assumptions and approvals in `briefs/brief.md` and `edit/decision-log.md`.

For each phase report: **what was examined**, **what changed**, **what remains uncertain**, **the recommendation and trade-off**, and **the next choice**. Offer at most three concrete paths plus “something else.” If the user granted end-to-end autonomy, choose safe defaults for reversible matters and proceed; retain gates for consequential decisions.

## 0. Intake and intent

**Discover.** Identify intended viewer, one primary outcome, platform and placement, length or limit, aspect ratio, language, tone, source material, CTA, deadline, brand constraints, permitted music/stock, appearance/voice permissions, and whether AI generation is allowed. Ask what success means (e.g. explain, entertain, drive an action) rather than promising reach or performance.

**Recommend.** If the user has not selected a channel, ask where it will publish. If duration is flexible, recommend the shortest version that preserves the story and offer a more complete version. If brief is incomplete but the project is low-risk, write down assumptions before drafting.

**Gate A — one creative direction.** Present a one-sentence promise, intended emotion, audience, likely length, CTA, and one or two tonal directions. Ask the user to choose or approve the best-fit direction before committing to extensive assembly. For an explicitly autonomous job, proceed with the best-supported direction and log it.

**Accept when.** Required output and constraints are understood; rights and permitted use of assets are either evidenced or flagged; unknown facts are not presented as facts.

## 1. Workspace and media safety

**Inspect.** Confirm the workspace root and expected folders; read current project manifest and decisions; inventory candidate media; probe streams, duration, frame rate, dimensions, rotation, sample rate, channels, codec and timestamps where supported. Generate stable hashes only when useful. Check for missing files, duplicate names, unsupported codecs, variable frame rate, corrupt streams, silence/clipping, and low-resolution or portrait/landscape mismatches.

**Protect.** Keep originals untouched. Make proxies or working copies in designated locations. Never move media to “organize” it without authorization. Keep private raw assets local unless the user explicitly authorizes external AI processing; disclose a proposed external service before sending media to it.

**Recommend.** Present the best source/shot candidates with a reason and any technical risk. Suggest proxy workflow when decode is slow; transcode only to a new file and preserve source/hash. Flag missing releases/music licenses as publish blockers, not assumptions.

**Gate B — material risks only.** Ask about unclear rights, missing/ambiguous source, private data, or problematic codecs before using them. Routine inventory does not need approval.

**Accept when.** Inventory is saved, every selected file has a stable path, source protection is explicit, and required red flags are raised.

## 2. Creative treatment / storyboard

**Build.** Create an outline with a hook, context, development/proof, payoff, and CTA/end beat. Every beat should do a job. Plan visuals, on-screen text, audio, approximate seconds, and source candidates. Identify how the first seconds honestly establish relevance without bait-and-switch.

**Options to offer.** (A) clear/explanatory: faster comprehension, less atmosphere; (B) story/emotion-led: stronger feeling, more setup; (C) energetic/rapid: quicker rhythm, less room for nuance. Tailor to the brief, not generic platform myths. Show a short sample of opening copy and a rough runtime for each credible choice.

**Recommend.** Choose one primary narrative angle and give a reason based on source strength, audience and desired outcome. If footage cannot support the requested claim or visual, say so and propose a truthful alternative.

**Gate C — approve angle.** Obtain direction on message/tonality before finalizing script or generating material. A user-approved objective does not automatically approve factual assertions, brand representation, or synthetically generated likeness/audio.

**Accept when.** The outline has a coherent causal/emotional sequence, each beat is supportable by source material, and the ending delivers the promised value/action.

## 3. Selects, transcript, paper edit

**Prepare.** Transcribe only when needed. Mark transcription confidence and verify names/numbers/claims against the audio. Build a selects list with source filename, source in/out timecode, exact quote or visual description, usefulness, confidence, and rights/status. Create a paper edit/beat sheet before heavy timeline work.

**Editorial tests.** Keep the main point comprehensible without relying on an unverified voiceover. Remove repetitions that do not intentionally build meaning. Protect context around statements; do not join separate phrases into a misleading claim. Use visual cutaways for a reason (proof, orientation, emotion, contrast), not simply to hide every cut.

**Recommend.** Identify one strongest opening and one backup, plus cuts that save time without losing meaning. Report transcript uncertainties as ranges/timecodes.

**Gate D — factual meaning.** Obtain review for changed claims, sensitive quotes, names, medical/financial/legal material, client promises, or edits that could alter speaker intent. If only mechanical rhythm is affected, continue in draft status.

**Accept when.** Selects are traceable to original timecodes, transcript uncertainty is visible, and story still makes sense without unexplained leaps.

## 4. Rough cut

**Assemble.** Make the simplest coherent assembly. Prioritize message order, emotional arc, intelligibility, and total duration. Use hard cuts unless another transition communicates time, space, or feeling. Establish sequence/profile early. Maintain timing in frames or exact rational timebase; do not add a new frame-rate conversion accidentally.

**Preview.** Render a watermarked or clearly labeled low-res draft when appropriate. Use a low-resolution profile and a short section test before a full export. Never mistake temp footage or generated visuals for final approved content.

**Recommend.** Call out the highest-impact one to three improvements only. For each, state issue → audience effect → proposed change → trade-off. Example: “The context lands at 0:08, so some viewers may leave before the promise is clear. Moving this sourced payoff to 0:02 improves clarity but reveals the reveal earlier.”

**Gate E — story and runtime.** Show or link the rough cut and request approve / targeted revisions / alternate direction. If “take the wheel” is active, proceed with a saved revision and keep the last review render.

**Accept when.** Message is understandable, no unsupported story jump is present, duration is plausible, and the user has had a chance to redirect the narrative.

## 5. Fine cut and picture

**Refine.** Tighten starts/ends; remove dead air unless meaningful; preserve breaths/emphasis where they support performance. Check continuity, eyelines, action direction, geography, rhythm and motivated B-roll. Reframe for subject position and intended eye line, not centered face as an invariant. If source is landscape but deliverable is vertical, choose among (A) crop/follow subject, (B) blurred/graphic background with full image, or (C) designed split-screen; explain visible-content and design consequences.

**Polish selectively.** Add titles, graphics, transitions or effects only when they clarify hierarchy or emotion. Keep legal/brand details readable and avoid unsupported claims. Use licensed fonts/assets; do not assume a bundled font is available on Ubuntu.

**Recommend.** Identify crop safety, pacing, mismatched exposure/color, distracting movement, or effects that reduce legibility. Prefer correcting source mismatch to applying a global heavy look.

**Gate F — picture lock.** Request approval before expensive finishing or platform-version multiplication. If user asks fully automated, record the approved base cut and continue; keep a versioned project.

**Accept when.** Framing supports the story, cuts are motivated, titles are safe/readable, and no obvious flash/black frame/repeated frame or accidental transition appears.

## 6. Captions and accessibility

**Create.** Generate captions from actual speech, correct them against source audio, preserve SRT or WebVTT, and burn them only when requested or required. Use line breaks that preserve phrase units; avoid covering faces, UI controls or critical visuals. Keep reasonable contrast, size and screen dwell time. Check accents, names, punctuation, speaker labels and sound cues. Do not rely on color alone.

**Options.** Offer (A) clean accessibility captions (less motion, highest reading comfort), (B) restrained emphasis (highlight a few meaningful words), (C) kinetic word-by-word style (higher energy but greater distraction and word-reading burden). Show a still/frame or a short preview when styling has consequences.

**Recommend.** Prefer accuracy and mobile legibility over animated captions. Mention whether text is burned in, sidecar, or both; editable sidecars improve reuse/accessibility but platforms handle them differently.

**Gate G — text and identity.** Confirm any styled claims, names, sensitive terms and brand treatment. User approval of audio does not equal approval of mistranscribed captions.

**Accept when.** Captions match speech, timing is legible, text stays inside safe areas, and a sidecar exists when practical.

## 7. Sound and color

**Sound order.** Dialogue cleanup → edit fades → balance dialogue/music/effects → check loudness/true peaks in context → listen on speakers/headphones and, if possible, phone. De-ess/EQ/reduce noise carefully; aggressive processing can sound worse. Duck music only as needed. Keep important speech intelligible. Respect source and library licenses.

**Image order.** Verify rotation/aspect/color tags → correct white balance/exposure and shot-to-shot consistency → apply modest creative look → inspect skin/highlights/shadows and compression. Avoid assuming source footage is Rec.709 or applying global saturation/contrast blindly. Preserve correct color metadata and avoid illegal/unsupported settings for the target chain.

**Recommend.** Report audible clipping, hum, harsh sibilance, muddy dialog, poor balance, inconsistent shot color, and notable source quality limits. Do not describe numeric loudness as “broadcast-safe” unless measured and matching the selected delivery specification.

**Gate H — subjective finish.** Show a short before/after or controlled comparison if the look or mix changes emotional tone substantially. Otherwise document restrained choices and continue.

**Accept when.** Speech and music are balanced and free of obvious technical faults; visual shots are coherent; finish supports rather than obscures the content.

## 8. Platform versions and export

**Derive.** Start from one approved edit, but create intentional platform versions: crop/reposition independently; resize titles/captions for screen and UI occlusion; check exact duration/codec/frame rate/audio requirements for current destination; revise CTA only with approval. Use a project `platform_profiles.json` or explicit per-export settings and verify them against current official platform specs if hard requirements matter.

**Options.** Offer a main target and whether to create (A) one master only, (B) a vertical and horizontal pair, or (C) additional short/long variants. Explain added render/review effort. A “post everywhere” request does not mean identical center-crops are good versions.

**Recommend.** Export a high-quality master plus required delivery copy only where storage and workflow justify it. Use descriptive filenames and retain editability. Do not bake an unapproved CTA, music, or watermark.

**Gate I — delivery selection.** Confirm final dimensions, inclusion of subtitles/audio, brand treatment, filenames, and whether any external platform upload is wanted. Actual upload/publication is a separate explicit action with its own confirmation.

**Accept when.** Exports meet requested dimensions, rate, duration, codec/container, audio/subtitle behavior and naming; media is not clipped, stretched or accidentally silent.

## 9. QC, handoff and learning

**Machine checks.** Probe streams, expected duration/tolerance, dimensions, frame rate, codec, pixel format, color tags, audio presence/sample rate/layout, subtitle streams, file size and timestamps. Detect zero-byte files and unexpected stream counts. Compare intended and actual profile. Save report/log.

**Human checks.** Play the full export when possible; inspect the opening, every edit/transition, graphics/captions and ending; listen for sync/clicks/clipping/dropouts; verify factual copy, crop, skin/highlight detail, phone-scale legibility and proper final frame. Machine checks cannot determine whether a story is truthful or compelling.

**Report.** Sort findings into **must fix before publishing**, **recommended**, and **optional polish**. Include uncertainty, exact timecodes and steps to reproduce. Provide final files, Kdenlive project if created, EDL/OTIO when created, captions, settings, changelog, source rights notes and remaining approval needs.

**Accept when.** Machine QC passes or has documented exceptions; visual/audio review is complete or its limitation is declared; the project can be reopened; user knows no publication occurred absent explicit authorization.

## Revisions and recovery

- Record approved decisions in `edit/decision-log.md`; include date/time, stage, selected option, rationale, and unresolved items.
- Preserve baseline and previous approved versions before changing the story, profile, or graphics. Prefer `cut_v001`, `cut_v002` or short revision labels over replacing files.
- If the user requests a change after picture lock, identify downstream effects (captions, sound, versioning, QC) before executing. Make the smallest coherent rework.
- On render failure, keep logs and intermediate files in the project's work/log area; report the root cause and next best options. Never silently downgrade resolution, codec, or quality.
- If the request conflicts with safety, rights, factual support, or available sources, explain the blocker and propose a safe edit rather than attempting an unsupported workaround.
