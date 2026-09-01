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

# Reading order, which is also the nav order in mkdocs.yml. Series carry no
# ordinal in their name: the order lives here and in the nav, so a new series
# does not mean renumbering prose that nothing validates.
GUIDES = [
    ("Start here", "guides/start-here"),
    ("Website on Edgible", "guides/website-on-edgible"),
    ("n8n on Edgible", "guides/n8n-on-edgible"),
    ("OpenClaw on Edgible", "guides/openclaw-on-edgible"),
    ("LLM on Edgible", "guides/llm-on-edgible"),
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
                    # Chapter hooks are one sentence, but a page can open with a
                    # full paragraph. One sentence is enough for an index entry.
                    # Splitting only before a capital keeps 127.0.0.1 intact.
                    text = re.split(r"\.\s+(?=[A-Z])", text)[0]
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
    out.append("## Overview")
    out.append("")
    index = REPO / "README.md"
    out.append(
        f"- [{heading(index)}]({url_for('index.md')}): what Edgible does, "
        "what the guides cover, and where to start"
    )
    cap = REPO / "capabilities.md"
    out.append(f"- [{heading(cap)}]({url_for('capabilities.md')}): {hook(cap)}")
    glossary = REPO / "glossary.md"
    out.append(f"- [{heading(glossary)}]({url_for('glossary.md')}): {hook(glossary)}")
    ai = REPO / "working-with-ai.md"
    out.append(f"- [{heading(ai)}]({url_for('working-with-ai.md')}): {hook(ai)}")
    evaluators = REPO / "appendix" / "for-evaluators.md"
    out.append(
        f"- [{heading(evaluators)}]({url_for('appendix/for-evaluators.md')}): "
        f"{hook(evaluators)}"
    )
    out.append("")

    for title, rel in GUIDES:
        directory = REPO / rel
        out.append(f"## {title}")
        out.append("")
        readme = directory / "README.md"
        if readme.exists():
            summary = hook(readme) or "chapter list and reading order"
            out.append(f"- [{heading(readme)}]({url_for(rel + '/README.md')}): {summary}")
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
    sources = [
        REPO / "README.md",
        REPO / "capabilities.md",
        REPO / "glossary.md",
        REPO / "working-with-ai.md",
        REPO / "appendix" / "for-evaluators.md",
    ]
    for _, rel in GUIDES:
        directory = REPO / rel
        readme = directory / "README.md"
        if readme.exists():
            sources.append(readme)
        sources.extend(chapter_files(directory))

    for path in sources:
        rel = path.relative_to(REPO).as_posix()
        # The canonical URL rather than the repo path, so a section quoted out
        # of this file can still be traced back to the page it came from.
        out.append(f"<!-- source: {url_for(rel)} -->")
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
