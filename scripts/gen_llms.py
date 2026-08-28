#!/usr/bin/env python3
"""Generate llms.txt and llms-full.txt from the canonical guide markdown.

llms.txt is an index for coding agents and MCP servers. It links to the raw
.md files rather than the HTML, because that is what an agent wants to read.
llms-full.txt is every chapter concatenated, for one-shot ingestion.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SITE = "https://guides.edgible.com"

REPO = Path(__file__).resolve().parent.parent

GUIDES = [
    ("1. n8n on Edgible", "guides/n8n-on-edgible"),
    ("2. OpenClaw on Edgible", "guides/openclaw-on-edgible"),
    ("3. LLM on Edgible", "guides/llm-on-edgible"),
]


def heading(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def hook(path: Path) -> str:
    """The bold one-liner under the title, stripped of markup."""
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            for candidate in lines[i + 1 : i + 5]:
                candidate = candidate.strip()
                if candidate:
                    text = re.sub(r"[*_`]", "", candidate)
                    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
                    return text.rstrip(".")
            break
    return ""


def url_for(rel: str) -> str:
    return f"{SITE}/{rel}"


def chapter_files(directory: Path) -> list[Path]:
    return sorted(p for p in directory.glob("*.md") if p.name != "README.md")


def build_index() -> str:
    out: list[str] = []
    out.append("# Edgible Guides")
    out.append("")
    out.append(
        "> Hands-on guides for publishing a self-hosted service on a public HTTPS "
        "hostname with Edgible, using an outbound connection on TCP 443 and no "
        "port-forward. Every chapter is one job with one smoke test. Links below "
        "are raw markdown."
    )
    out.append("")
    out.append("## Start here")
    out.append("")
    out.append(f"- [Start here]({url_for('index.md')}): reading order for the three guides")
    cap = REPO / "capabilities.md"
    out.append(f"- [{heading(cap)}]({url_for('capabilities.md')}): {hook(cap)}")
    out.append("")

    for title, rel in GUIDES:
        directory = REPO / rel
        out.append(f"## {title}")
        out.append("")
        readme = directory / "README.md"
        if readme.exists():
            out.append(f"- [{heading(readme)}]({url_for(rel + '/README.md')}): chapter list and reading order")
        for chapter in chapter_files(directory):
            link = url_for(f"{rel}/{chapter.name}")
            summary = hook(chapter)
            line = f"- [{heading(chapter)}]({link})"
            if summary:
                line += f": {summary}"
            out.append(line)
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def build_full() -> str:
    out: list[str] = ["# Edgible Guides, full text", ""]
    sources = [REPO / "README.md", REPO / "capabilities.md"]
    for _, rel in GUIDES:
        directory = REPO / rel
        readme = directory / "README.md"
        if readme.exists():
            sources.append(readme)
        sources.extend(chapter_files(directory))

    for path in sources:
        rel = path.relative_to(REPO).as_posix()
        out.append(f"<!-- source: {rel} -->")
        out.append("")
        out.append(path.read_text(encoding="utf-8").rstrip())
        out.append("")
        out.append("---")
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: gen_llms.py <output-dir>", file=sys.stderr)
        return 2
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "llms.txt").write_text(build_index(), encoding="utf-8")
    (dest / "llms-full.txt").write_text(build_full(), encoding="utf-8")
    print(f"wrote {dest/'llms.txt'} and {dest/'llms-full.txt'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
