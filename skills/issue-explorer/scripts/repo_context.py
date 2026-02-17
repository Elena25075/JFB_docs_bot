#!/usr/bin/env python3
"""
Print a quick, read-only repository context snapshot as Markdown.

Intended use:
  python3 skills/issue-explorer/scripts/repo_context.py
  python3 skills/issue-explorer/scripts/repo_context.py --repo path/to/repo
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path


def _read_text(path: Path, max_bytes: int = 512_000) -> str:
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        return ""
    if len(data) > max_bytes:
        data = data[:max_bytes]
    # Best-effort UTF-8; fall back to latin-1 to avoid crashes on odd files.
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1", errors="replace")


def _walk_limited(root: Path, max_depth: int, ignore_dirs: set[str]) -> tuple[Counter, Counter]:
    """
    Return (ext_counts, top_level_counts).
      ext_counts: file-extension histogram (normalized, with "" for no extension)
      top_level_counts: counts of immediate children (dirs/files)
    """
    ext_counts: Counter[str] = Counter()
    top_level_counts: Counter[str] = Counter()

    try:
        for child in root.iterdir():
            if child.name in ignore_dirs:
                continue
            top_level_counts["dirs" if child.is_dir() else "files"] += 1
    except FileNotFoundError:
        return ext_counts, top_level_counts

    root_parts_len = len(root.parts)
    for dirpath, dirnames, filenames in os.walk(root):
        cur = Path(dirpath)
        depth = len(cur.parts) - root_parts_len
        if depth >= max_depth:
            dirnames[:] = []
            continue

        # In-place prune ignored dirs.
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]

        for fn in filenames:
            p = cur / fn
            ext = p.suffix.lower()
            ext_counts[ext] += 1

    return ext_counts, top_level_counts


def _parse_pyproject(pyproject_path: Path) -> dict:
    result: dict = {}
    if not pyproject_path.exists():
        return result

    try:
        import tomllib  # py3.11+
    except Exception:
        return {"error": "tomllib unavailable (need Python 3.11+)"}

    try:
        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)
    except Exception as e:
        return {"error": f"failed to parse pyproject.toml: {e}"}

    # PEP 621
    project = data.get("project") or {}
    if isinstance(project, dict):
        deps = project.get("dependencies") or []
        scripts = project.get("scripts") or {}
        if deps:
            result["project.dependencies"] = deps
        if scripts:
            result["project.scripts"] = scripts
        opt_deps = project.get("optional-dependencies") or {}
        if opt_deps:
            result["project.optional-dependencies"] = opt_deps

    # Poetry (common in Python repos)
    tool = data.get("tool") or {}
    poetry = (tool.get("poetry") or {}) if isinstance(tool, dict) else {}
    if isinstance(poetry, dict):
        pdeps = poetry.get("dependencies") or {}
        if isinstance(pdeps, dict):
            # Drop python itself; keep the rest.
            pdeps = {k: v for k, v in pdeps.items() if k.lower() != "python"}
            if pdeps:
                result["tool.poetry.dependencies"] = pdeps
        pscripts = poetry.get("scripts") or {}
        if pscripts:
            result["tool.poetry.scripts"] = pscripts
        groups = poetry.get("group") or {}
        if isinstance(groups, dict):
            out_groups = {}
            for gname, gval in groups.items():
                if not isinstance(gval, dict):
                    continue
                gdeps = gval.get("dependencies") or {}
                if isinstance(gdeps, dict) and gdeps:
                    out_groups[gname] = gdeps
            if out_groups:
                result["tool.poetry.group"] = out_groups

    return result


def _parse_requirements_txt(path: Path) -> list[str]:
    if not path.exists():
        return []
    deps: list[str] = []
    for raw in _read_text(path).splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        # Keep include directives but mark them.
        deps.append(line)
    return deps


def _parse_package_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(_read_text(path))
    except Exception as e:
        return {"error": f"failed to parse package.json: {e}"}

    out: dict = {}
    for key in ("name", "type", "main"):
        if key in data:
            out[key] = data[key]
    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        if key in data and isinstance(data[key], dict) and data[key]:
            out[key] = data[key]
    if "scripts" in data and isinstance(data["scripts"], dict) and data["scripts"]:
        # Keep scripts as a hint for entrypoints and dev workflow.
        out["scripts"] = data["scripts"]
    return out


def _candidate_entrypoints(root: Path) -> list[str]:
    candidates = [
        "main.py",
        "app.py",
        "server.py",
        "__main__.py",
        "wsgi.py",
        "asgi.py",
        "manage.py",
        "index.js",
        "server.js",
        "app.js",
        "index.ts",
        "server.ts",
        "app.ts",
    ]
    hits: list[str] = []

    # Look in a few common places.
    roots = [root, root / "src", root / "app"]
    for base in roots:
        for rel in candidates:
            p = base / rel
            if p.exists() and p.is_file():
                hits.append(str(p.relative_to(root)))
    return sorted(set(hits))


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", help="Repository root (default: .)")
    ap.add_argument("--max-depth", type=int, default=4, help="Max directory walk depth (default: 4)")
    args = ap.parse_args(argv)

    root = Path(args.repo).resolve()
    ignore_dirs = {".git", ".venv", "venv", "__pycache__", "node_modules", ".mypy_cache", ".pytest_cache"}

    ext_counts, top_counts = _walk_limited(root, max_depth=args.max_depth, ignore_dirs=ignore_dirs)

    pyproject = _parse_pyproject(root / "pyproject.toml")
    reqs = []
    for name in ("requirements.txt", "requirements-dev.txt", "requirements-dev.in", "requirements.in"):
        p = root / name
        if p.exists():
            reqs.append((name, _parse_requirements_txt(p)))

    pkg = _parse_package_json(root / "package.json")
    entrypoints = _candidate_entrypoints(root)

    top_exts = []
    for ext, count in ext_counts.most_common(12):
        label = ext if ext else "(none)"
        top_exts.append(f"`{label}`={count}")

    print("# Repo Context Snapshot")
    print()
    print(f"- Root: `{root}`")
    print(f"- Top-level: {top_counts.get('dirs', 0)} dirs, {top_counts.get('files', 0)} files (excluding ignored dirs)")
    print(f"- File types (top 12): {', '.join(top_exts) or '(none)'}")
    print()

    if entrypoints:
        print("## Candidate Entrypoints")
        print()
        for p in entrypoints:
            print(f"- `{p}`")
        print()

    if pyproject:
        print("## pyproject.toml (parsed)")
        print()
        print("```json")
        print(json.dumps(pyproject, indent=2, sort_keys=True))
        print("```")
        print()

    if reqs:
        print("## requirements*.txt")
        print()
        for name, items in reqs:
            print(f"### `{name}`")
            print()
            if not items:
                print("- (empty)")
            else:
                for dep in items[:200]:
                    print(f"- `{dep}`")
                if len(items) > 200:
                    print(f"- (… {len(items) - 200} more)")
            print()

    if pkg:
        print("## package.json (parsed)")
        print()
        print("```json")
        print(json.dumps(pkg, indent=2, sort_keys=True))
        print("```")
        print()

    if not any([pyproject, reqs, pkg, entrypoints]):
        print("## Notes")
        print()
        print("- No common dependency/entrypoint files detected at the repo root.")
        print("- If this repo is empty or uses a non-standard layout, provide README/deps files or point to the correct subdirectory.")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
