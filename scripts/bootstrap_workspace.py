#!/usr/bin/env python3
"""Create the social-video workspace without overwriting existing project files."""
from __future__ import annotations
import argparse
import shutil
import sys
from pathlib import Path

DEFAULT_TARGET = Path('/home/t0n34781/Projects/socmed_content_creation')
REPO = Path(__file__).resolve().parents[1]
SKILL_NAME = 'socmed-video-production'


def copy_missing(src: Path, dst: Path) -> tuple[int, int]:
    """Copy missing regular files only; never follow or overwrite target links."""
    copied = skipped = 0
    if src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists() or dst.is_symlink():
            return 0, 1
        shutil.copy2(src, dst)
        return 1, 0
    if not src.is_dir():
        return 0, 0
    for item in sorted(src.rglob('*')):
        if item.is_symlink():
            continue
        rel = item.relative_to(src)
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() or target.is_symlink():
                skipped += 1
            else:
                shutil.copy2(item, target)
                copied += 1
    return copied, skipped


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--target', type=Path, default=DEFAULT_TARGET, help=f'Workspace root (default: {DEFAULT_TARGET})')
    ap.add_argument('--repo', type=Path, default=REPO, help='Repository containing the workspace template and Claude skill')
    args = ap.parse_args()
    repo = args.repo.expanduser().resolve()
    target = args.target.expanduser().resolve()
    template = repo / 'workspace-template'
    skill_src = repo / '.claude' / 'skills' / SKILL_NAME
    if not template.is_dir() or not (skill_src / 'SKILL.md').is_file():
        print(f'ERROR: expected workspace-template and skill under {repo}', file=sys.stderr)
        return 2
    if target == Path('/') or target == Path.home():
        print(f'ERROR: refusing unsafe broad target {target}', file=sys.stderr)
        return 2
    target.mkdir(parents=True, exist_ok=True)
    copied = skipped = 0
    for src in sorted(template.rglob('*')):
        if src.is_symlink() or not src.is_file():
            continue
        n, s = copy_missing(src, target / src.relative_to(template))
        copied += n; skipped += s
    n, s = copy_missing(skill_src, target / '.claude' / 'skills' / SKILL_NAME)
    copied += n; skipped += s
    for rel in ('docs', 'schemas'):
        n, s = copy_missing(repo / rel, target / rel)
        copied += n; skipped += s
    for filename in ('skill-manifest.json', 'video-editing-pipeline-template.json'):
        n, s = copy_missing(repo / filename, target / filename)
        copied += n; skipped += s
    mcp_src = repo / '.mcp.json'
    if mcp_src.is_file():
        n, s = copy_missing(mcp_src, target / '.mcp.json')
        copied += n; skipped += s
    # Materialize empty-but-important workspace folders as well as template-backed ones.
    for rel in ('assets/originals', 'assets/proxies', 'assets/audio', 'assets/graphics', 'transcripts', 'review', 'exports', 'archive', 'logs'):
        (target / rel).mkdir(parents=True, exist_ok=True)
    print(f'Workspace ready: {target}')
    print(f'Files copied: {copied}; existing files preserved: {skipped}')
    print('Next: review production.json and briefs/brief.md, install/check FFmpeg and Kdenlive, then launch Claude Code in this directory.')
    print('No source media was copied, moved, uploaded, or overwritten.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
