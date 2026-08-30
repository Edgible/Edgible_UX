#!/usr/bin/env python3
"""Stamp each page with the date its markdown last changed.

The date comes from git rather than a field an author maintains, because a
hand-kept date goes stale exactly when it matters. Two modes, because the
rendered page and the raw markdown are read by different audiences:

  meta    prepends YAML front matter to the staged copies, which MkDocs exposes
          as page.meta for overrides/main.html to render. It also carries the
          page's hook across as its description, which becomes the meta
          description and the line under the title on the social card. Without
          it every page would share the site description, cut mid-sentence.
  header  prepends the canonical URL and the date to the .md files served
          alongside the HTML. Once a reader pastes a chapter into a chat, the
          URL is the only thing that lets the assistant cite it, or the reader
          work out later which version they followed. It leads rather than
          trails because a long chapter is often pasted truncated.

Paths are relative to the repo root in both trees, so the tree being stamped
maps onto the file whose history is being read. Untracked files are skipped
rather than guessed at.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

from gen_llms import hook

REPO = Path(__file__).resolve().parent.parent
SITE = "https://guides.edgible.com"


def last_changed(rel: str) -> str | None:
    """The committer date, as YYYY-MM-DD, of the last commit touching rel."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", rel],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def display(iso: str) -> str:
    return date.fromisoformat(iso).strftime("%-d %B %Y")


def source_for(path: Path, root: Path) -> str:
    rel = path.relative_to(root).as_posix()
    # MkDocs needs the home page as index.md; its history lives in README.md.
    return "README.md" if rel == "index.md" else rel


def stamp(path: Path, iso: str, root: Path, mode: str) -> None:
    text = path.read_text(encoding="utf-8")
    if mode == "meta":
        lines = [f"updated: {iso}", f"updated_display: {display(iso)}"]
        summary = hook(path)
        if summary:
            # hook() drops the full stop, which suits a list entry in llms.txt
            # but not a sentence under a card title.
            summary += "."
            # json.dumps gives a double-quoted scalar YAML accepts, so a hook
            # containing a colon or a quote cannot break the front matter.
            lines.append(f"description: {json.dumps(summary)}")
        front = "---\n" + "\n".join(lines) + "\n---\n\n"
        path.write_text(front + text, encoding="utf-8")
    else:
        url = f"{SITE}/{path.relative_to(root).as_posix()}"
        header = f"Source: {url}\nLast updated: {iso}\n\n"
        path.write_text(header + text, encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in {"meta", "header"}:
        print("usage: add_dates.py <meta|header> <tree>", file=sys.stderr)
        return 2

    mode, root = sys.argv[1], Path(sys.argv[2])
    stamped = 0
    for path in sorted(root.rglob("*.md")):
        iso = last_changed(source_for(path, root))
        if iso:
            stamp(path, iso, root, mode)
            stamped += 1

    if stamped == 0:
        # No history reached the build, so every page would silently lose its
        # date. Worth failing rather than shipping pages that look undated.
        print(f"no git dates found for the markdown under {root}", file=sys.stderr)
        return 1

    print(f"dated {stamped} files under {root} ({mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
