#!/usr/bin/env python3
"""
Update `Overall Progress` in a markdown plan by scanning top-level step statuses.

Rules:
- Count only top-level task lines that start with:
  - "- [x] 🟩 **Step"
  - "- [ ] 🟨 **Step"
  - "- [ ] 🟥 **Step"
- Progress is computed as:
    (done_top_level_steps / total_top_level_steps) * 100
- The script updates the first line matching:
    **Overall Progress:** `N%`
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


# Match top-level step lines with explicit status emoji.
STEP_LINE_RE = re.compile(r"^- \[(?P<checked>[ xX])\] (?P<emoji>[🟩🟨🟥]) \*\*Step\b")

# Match the progress line at the top section.
PROGRESS_LINE_RE = re.compile(r"^\*\*Overall Progress:\*\* `\d+%`$")


def compute_progress(markdown_text: str) -> tuple[int, int, int]:
    """
    Return (progress_percent, done_steps, total_steps) from markdown content.
    """
    done = 0
    total = 0

    for line in markdown_text.splitlines():
        match = STEP_LINE_RE.match(line)
        if not match:
            continue
        total += 1
        emoji = match.group("emoji")
        checked = match.group("checked").lower() == "x"
        if emoji == "🟩" and checked:
            done += 1

    if total == 0:
        return 0, done, total

    percent = round((done / total) * 100)
    return percent, done, total


def update_progress_line(markdown_text: str, percent: int) -> tuple[str, bool]:
    """
    Replace the first progress line with the new percent.
    Return (updated_text, was_updated).
    """
    lines = markdown_text.splitlines()
    updated = False

    for index, line in enumerate(lines):
        if PROGRESS_LINE_RE.match(line):
            lines[index] = f"**Overall Progress:** `{percent}%`"
            updated = True
            break

    return "\n".join(lines) + ("\n" if markdown_text.endswith("\n") else ""), updated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to markdown plan file")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write updates in place (default: print summary only)",
    )
    args = parser.parse_args()

    plan_path = Path(args.file).resolve()
    content = plan_path.read_text(encoding="utf-8")

    percent, done, total = compute_progress(content)
    updated_content, had_progress_line = update_progress_line(content, percent)

    print(f"File: {plan_path}")
    print(f"Top-level steps done: {done}/{total}")
    print(f"Computed progress: {percent}%")

    if not had_progress_line:
        print("No progress line found. Expected: **Overall Progress:** `N%`")
        return 1

    if args.write:
        plan_path.write_text(updated_content, encoding="utf-8")
        print("Updated progress line in file.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

