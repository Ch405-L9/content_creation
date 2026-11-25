# Creative and technical standards

Use these as review questions rather than one-size-fits-all numerical rules. The requested platform, project manifest, current official delivery guidance, source properties and creative intent take precedence over generic presets.

## Story and editorial judgment

- Write the central promise in one sentence. If the edit contains multiple promises, choose a primary and demote the rest to supporting proof or remove them.
- The opening must make a truthful promise quickly. A hook is a clear question, vivid moment, useful outcome, or emotional tension—not a claim the video fails to satisfy.
- Shape beats as setup → development/evidence → payoff → optional CTA. Not every video needs a CTA. Avoid delaying essential context just to optimize an assumed algorithm.
- Check whether the viewer can understand the subject, stakes, and sequence without private context. Preserve caveats and uncertainty in health, finance, law, safety, political and product-claim content.
- Judge cuts by intent, performance, continuity and comprehension. A cut may be motivated by action, eyeline, audio, contrast, reveal or rhythm. A transition is not a substitute for story logic.
- Use B-roll to establish setting, prove a point, reveal a detail, bridge time or make an emotion visible. Do not use illustrative footage in a way that misrepresents what happened.
- Think in shot sizes and visual hierarchy: distinguish subject, supporting detail and negative space for text. Match foreground/background contrast and avoid placing essential content beneath common interface overlays.
- Preserve authentic pauses and reactions when they carry meaning. Remove dead time when it dilutes intent, not merely to meet an arbitrary cut frequency.

## Platform framing and graphics

- Confirm aspect ratio, dimensions, frame rate, orientation/rotation metadata, color space and maximum duration for each delivery. Verify current official rules for time-sensitive platform limits rather than relying on memory.
- Scale/crop by subject and action. Inspect the first, middle and last frame of every crop; account for hand/face motion and captions. Do not stretch pixels to fill the frame.
- Create a reusable safe-area overlay per target device/placement, not a single universal percentage. Keep essential text away from edges and UI overlays.
- Use typography with sufficient size, contrast and line length at phone size. Restrict font families and emphasis styles. Verify font availability and license on Ubuntu; substitute only with an explicitly noted, compatible font.
- Motion should reinforce hierarchy. Use restrained transitions and text animation; avoid flashing/strobing, rapid zooms, fine patterns or effects likely to trigger discomfort or compression artifacts.
- Do not place unlicensed logos, assets, fonts, templates or music into delivery. Keep attribution/license notes with third-party materials.

## Captions and accessibility

- Preserve a corrected text transcript and preferably a sidecar subtitle file (SRT/WebVTT) even if a burned-in version is also produced.
- Correct automatic transcription against audio. Mark uncertain words, speaker names and numbers for review; do not conceal uncertainty with polished-looking text.
- Break captions at linguistic phrase boundaries and maintain readable screen dwell time. Avoid single-word shattering except for intentional, minimal emphasis and at the user's direction.
- Ensure captions do not obscure faces, demonstrations, labels, safety information or UI. Test in the actual aspect ratio at realistic mobile scale.
- Use strong contrast and outline/background treatment where the moving image demands it. Color cannot be the only signal. Describe meaningful non-speech audio when required by the brief/accessibility target.
- Respect language, dialect, punctuation, speaker identity, and user-supplied style. Never normalize dialect or alter a speaker's meaning merely for style.

## Dialogue, music and effects

- Dialogue intelligibility is usually the first priority when speech carries the message. Listen for clipping, distortion, room noise, HVAC, traffic, plosives, sibilance, edits, phase problems and sync drift.
- Set clip gain/fades before dynamics processing. Apply noise reduction, EQ and compression conservatively; compare bypassed and processed audio at matched loudness.
- Keep music supportive. Side-chain/automation ducking should be smooth and phrase-aware. Avoid masking consonants or lowering critical ambient cues. Add SFX only when they clarify or motivate an edit.
- Measure loudness and true peak if delivery requirements specify them. Targets vary by platform, format and jurisdiction; keep measurement method, integrated loudness, loudness range, true peak and standard in the QC report when measured.
- Record music/SFX source and license/attribution. Do not infer that a popular or repository-embedded song is licensed for commercial social use.

## Color, encoding and visual integrity

- Determine source color primaries, transfer, matrix/range and orientation before conversions. Preserve or intentionally transform color tags. Avoid double-transforms between editor, filter chain and encoder.
- Correct exposure, white balance and shot matching before applying a style. Inspect skin tones, highlights, deep shadows and color clipping on representative scenes.
- Do not add film grain, chromatic aberration, LUTs, artificial blur or aggressive sharpening by default. Compression and small screens may make them objectionable.
- Use FFprobe to verify actual file streams and metadata. File extension alone does not prove container, codec, frame rate or subtitle format.
- Do not label a low-resolution draft “final.” Store final master and delivery copies separately. Record export recipe, tool versions and manifest/profile hash where repeatability matters.

## Review priority rubric

1. **Blocker:** factual/rights/privacy problem, missing/corrupt media, wrong format, absent required audio/captions, broken export, misleading edit, or unreadable essential text.
2. **High impact:** weak story clarity/hook/payoff, dialogue unintelligibility, poor framing, sync problem, abrupt ending, or inconsistent crop.
3. **Polish:** color matching, subtle animation, SFX, tighter but non-essential timing, or optional variant.

Explain recommendations as observed issue → likely impact → proposed change → trade-off. Do not present subjective taste as objective failure.
