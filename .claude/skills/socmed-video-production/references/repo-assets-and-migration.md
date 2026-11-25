# Repository assets and migration

This reference reflects the supplied `content_creation` repository. Preserve its existing originals and educational references; do not assume that the bundled video/image files are user-owned footage or approved for publication without checking rights and intended use.

## Existing material

- `Building_Cinematic_Frames.mp4` and `How_4K_Motion_Graphics_Impress.mp4`: use only as source examples after probing duration/codecs and confirming reuse permissions.
- `transcripts/`: editorial/production learning material about camera framing, shot sizes, camera movement, lighting, lenses, transitions, frame rate, subtitling, animation, and scene editing. These are references, not source footage or verified scripts for a new video. Transcripts can contain recognition errors; verify quotations against original sources when needed.
- `Technical Manual of Camera Rigs, Visual Framing, and Focus Modalities for Cinematic Production.pdf`, `Video_Editing_and_Cinematography_Blueprint.png`, `NotebookLM Mind Map.png`: reference resources. Inspect the original pages/images before relying on text extraction; do not treat recommendations as universal rules.
- `video-editing-pipeline-template.json`: a Premiere-oriented design template, not a runnable render specification. The original file had `""` where JSON Schema requires `"$schema"`, mislabeled a config as schema, hard-coded a 9:16 UHD default, and referenced proprietary effects/fonts/codecs that may not exist on Ubuntu. The repository version is repaired and reframed as an illustrative plan; keep tool capability checks and project-specific settings explicit.

## How to reuse repository knowledge

1. Ask which content/resource is in scope, or treat it as background only.
2. Check media metadata, provenance and licenses before any direct reuse or public distribution.
3. Use relevant transcripts as conceptual guidance (e.g. motivated cuts, eyelines, framing, transitions), not as law. Choose based on story, source shot and intended viewer.
4. Don't copy copyrighted educational footage, logos, illustrations, music or text into an export without permission. A public GitHub repo does not itself license the media; repository currently has no declared license metadata.
5. Preserve attributions/URLs and keep any allowed reference excerpt concise.

## Updating old template values

- Replace global `selected_mode` with a per-clip or per-sequence crop decision based on each target aspect and subject framing.
- Replace fixed resolution/fps with values chosen from actual source and target requirements; never assume 24 fps is right for every social video.
- Avoid importing Premiere-specific names such as “Ultra Key,” “Lumetri,” “SF Pro Display,” or blend-mode labels as though they were Kdenlive effects. Verify the installed editor version, effect names, fonts and licenses first.
- Treat loudness/peak values as targets only after selecting a delivery spec and measurement standard. Do not force music EQ at one frequency or add SFX triggers by default.
- Treat film grain/chromatic aberration/vignettes as optional creative choices. Compare before/after and disable when they degrade legibility or compression.
- For target bitrate, choose based on resolution, motion, encoder, quality requirement, file-size constraint and destination. Do not advertise a single fixed bitrate as universally optimal.
- Keep unknown features and unimplemented settings as advisory metadata. Declare the execution engine/profile and validate output instead of claiming every JSON value affects the render.
