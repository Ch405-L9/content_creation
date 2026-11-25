# Ubuntu editor and automation architecture

## Default recommendation: Kdenlive + FFmpeg/FFprobe

Use **Kdenlive** as the free/open-source Ubuntu nonlinear editor for timeline inspection, manual creative control, graphics/effects review and opening the native project. Automate deterministic media analysis and rendering with **FFmpeg/FFprobe**. Where an approved Kdenlive project is involved, preserve the `.kdenlive` file and use its MLT-based project/render ecosystem; do not treat its internal XML as a stable general-purpose editing API.

Why this pairing: Kdenlive project files are XML based on MLT; they reference media and describe timeline use, effects and project properties. Kdenlive's manual says MLT can render a Kdenlive project while ignoring Kdenlive-specific editing data; it also warns that format evolution can affect backwards compatibility. The manual documents generating MLT batch scripts and invoking `melt` from a terminal. These facts make this a practical, visible, editable handoff—but not a promise of an official REST API or MCP integration.

Install from a trusted official channel suited to the user's Ubuntu release: the Kdenlive download page lists Linux AppImage and Flatpak options. Ubuntu's repository package may be simplest, but version lag can matter. Prefer Flatpak/AppImage when the native package is materially older; check device/codec constraints and project version compatibility before switching installations. Never run an opaque third-party installer as root.

Example install choices (present rather than silently choosing):

- **Recommended for Ubuntu with Flatpak configured:** `flatpak install flathub org.kde.kdenlive` then `flatpak run org.kde.kdenlive`.
- **Ubuntu archive package:** `sudo apt update && sudo apt install kdenlive ffmpeg` (may not be the newest release).
- **AppImage:** download only from the official Kdenlive site, verify the published checksum/signature if offered, then mark executable and launch as the user (not root).

Check actual installed versions and installed codecs with `kdenlive --version`, `ffmpeg -version`, `ffprobe -version`, and (if installed) `melt -version`. Exact executable names can differ in sandboxed packages. Keep `ffmpeg`/`ffprobe` accessible in PATH to scripts.

## Division of labor

- **Kdenlive:** visual timeline review/editing, effects, titles, keyframes and a project a human can reopen. Open the project and confirm media relinking before further work.
- **FFmpeg/FFprobe:** deterministic transcodes/proxies, stream metadata, format conversions, simple assembly, audio filters, captions (when explicitly requested), and export checks. Use supported installed filters and codecs; write outputs to new paths.
- **MLT / `melt`:** render MLT/Kdenlive-compatible project scripts where available. A render does not guarantee an editable round trip. Keep a copy and test a small range first.
- **OpenTimelineIO (optional):** store editorial decisions in a Python API/interchange format when multiple tools benefit. OTIO carries editorial structure (clips, timing, tracks, transitions, markers and metadata) and references external media; it does not embed media. Adapter support depends on specific formats/tools. Do not assume direct Kdenlive `.kdenlive` round-tripping unless a verified adapter exists for the installed version.
- **Python/JSON/CSV:** manifests, decisions, inventory, safety checks and QC reports. Keep timing units, profile and referenced paths explicit.
- **MCP (optional):** expose a narrow local MCP service over approved project-safe scripts. MCP is the AI tool/API bridge; it is not a Kdenlive API. Prefer allowlisted operations and safe path checks over arbitrary shell execution.

## Editor selection and limits

If the user needs a different editor, compare actual current Linux builds, license, supported media, project compatibility, accessibility, proxy workflow and scripting options. Shotcut is another free/open-source option; do not claim its project format is interoperable with Kdenlive. Blender is useful for compositing/motion graphics but may be excessive for a conventional edit. Proprietary editors or cloud services are not default recommendations for a FOSS requirement.

## Project-file safeguards

- Kdenlive stores media as references; moving the project without updating its working directory can break paths. Keep assets stable and make a backup before project upgrades.
- Project file formats evolve and may not open in older Kdenlive versions. Record the editor version and preserve the original file when opening/upgrading a project.
- Avoid direct XML mutation unless a tested schema/version-specific tool is used. XML may contain Kdenlive-specific metadata in addition to MLT render instructions.
- If a project was created on another device, test a copy, confirm relative/absolute paths and plugins, and verify proxies and fonts. Do not overwrite the original to relink media.
- Before render, test a short range and verify output. For large jobs confirm available disk, power and expected run time.

## Compatibility note

This repository's project contains an old Premiere Pro-oriented JSON template. It is a creative/settings starting point only, not an executable Kdenlive, MLT, Premiere or universal engine project. Use the corrected file as a planning manifest and explicitly map its supported fields to the chosen editing/render tool. A setting with no tested implementation should remain a note—not silently pretend to render.
