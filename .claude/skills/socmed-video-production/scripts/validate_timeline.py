#!/usr/bin/env python3
"""Validate a sequential-cut timeline manifest without rendering it."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from timeline_utils import load_timeline

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('timeline', type=Path)
    args = ap.parse_args()
    data, errors, root = load_timeline(args.timeline.expanduser().resolve())
    duration = None
    if data:
        try:
            duration = sum(float(c['out_sec']) - float(c['in_sec']) for c in data['clips'])
        except (KeyError, TypeError, ValueError):
            pass
    result = {'valid': not errors, 'timeline': str(args.timeline.resolve()), 'project_root': str(root) if root else None, 'clip_count': len(data.get('clips', [])) if data else 0, 'duration_seconds': round(duration, 3) if duration is not None else None, 'errors': errors}
    print(json.dumps(result, indent=2))
    return 0 if not errors else 2

if __name__ == '__main__':
    raise SystemExit(main())
