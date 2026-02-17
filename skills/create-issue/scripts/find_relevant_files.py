#!/usr/bin/env python3
"""
Find up to 3 likely relevant files for an issue description using ripgrep hits.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "into",
    "when",
    "what",
    "where",
    "have",
    "has",
    "had",
    "are",
    "was",
    "were",
    "not",
    "but",
    "can",
    "could",
    "should",
    "would",
    "need",
    "needs",
    "issue",
    "bug",
    "feature",
    "improvement",
}


def build_pattern(text: str) -> str:
    tokens = re.findall(r"[a-zA-Z0-9_/-]+", text.lower())
    filtered = []
    seen = set()
    for tok in tokens:
        if len(tok) < 3 or tok in STOPWORDS:
            continue
        if tok in seen:
            continue
        filtered.append(tok)
        seen.add(tok)
        if len(filtered) >= 10:
            break
    if not filtered:
        filtered = tokens[:5]
    escaped = [re.escape(t) for t in filtered]
    return "|".join(escaped)


def run_rg(pattern: str, root: Path) -> Counter[str]:
    cmd = [
        "rg",
        "-n",
        "-S",
        "--hidden",
        "--glob",
        "!.git",
        "--glob",
        "!node_modules",
        "--glob",
        "!venv",
        "--glob",
        "!.venv",
        "--glob",
        "!__pycache__",
        pattern,
        str(root),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode not in (0, 1):
        raise RuntimeError(proc.stderr.strip() or "rg failed")

    counts: Counter[str] = Counter()
    for line in proc.stdout.splitlines():
        parts = line.split(":", 2)
        if len(parts) < 2:
            continue
        counts[parts[0]] += 1
    return counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True, help="Issue description or keywords")
    parser.add_argument("--root", default=".", help="Repository root (default: .)")
    parser.add_argument("--limit", type=int, default=3, help="Max files to return (default: 3, hard max: 3)")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    limit = max(1, min(args.limit, 3))
    pattern = build_pattern(args.query)

    if not pattern:
        print("- (none found in current repo)")
        return 0

    try:
        counts = run_rg(pattern, root)
    except FileNotFoundError:
        print("ripgrep (`rg`) is required but not found.", file=sys.stderr)
        return 1
    except RuntimeError as err:
        print(str(err), file=sys.stderr)
        return 1

    if not counts:
        print("- (none found in current repo)")
        return 0

    for file_path, hit_count in counts.most_common(limit):
        try:
            short = str(Path(file_path).resolve().relative_to(root))
        except ValueError:
            short = file_path
        print(f"- `{short}` ({hit_count} matches)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

