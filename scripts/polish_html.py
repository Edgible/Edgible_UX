#!/usr/bin/env python3
"""Two fixes to the built HTML that MkDocs cannot make for us.

Canonical URLs. With `use_directory_urls: false` every page is a `.html` file,
including the home page, so MkDocs points the site's canonical at
`/index.html` while every link anyone writes points at `/`. Both answer, which
is two URLs for one page. The root is the one that gets linked, so it wins, and
CloudFront redirects `/index.html` to it.

Image attributes. A browser that does not know how big an image is has to lay
the page out twice, which is the jump you see as a photograph arrives. The sizes
are known here, so they go in, and everything below the first image is left to
load lazily.

Run after `mkdocs build`; edits `site/` in place.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.etree import ElementTree

SITE_URL = "https://guides.edgible.com/"
ROOT_CANONICAL = re.compile(re.escape(SITE_URL + "index.html"))


def resolve(src: str, out: Path, page: Path) -> Path:
    """Where a page's src attribute lands on disk."""
    clean = src.split("#")[0].split("?")[0]
    if clean.startswith("http"):
        return Path("/nonexistent")
    if clean.startswith("/"):
        return out / clean.lstrip("/")
    return (page.parent / clean).resolve()


def image_size(path: Path) -> tuple[int, int] | None:
    """Intrinsic size of an image the build produced, or None if unknown."""
    if not path.exists():
        return None
    if path.suffix == ".svg":
        view_box = ElementTree.parse(path).getroot().get("viewBox")
        if not view_box:
            return None
        _, _, w, h = view_box.split()
        return round(float(w)), round(float(h))
    from PIL import Image

    with Image.open(path) as im:
        return im.size


def fix_images(html: str, out: Path, page: Path) -> str:
    def repl(m: re.Match[str]) -> str:
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        if not src or "loading=" in tag or "data-md" in tag:
            return tag
        # The chrome's own images are small, already sized by the theme's CSS,
        # and the logo is wanted immediately, so leave them alone.
        if any(part in src.group(1) for part in ("edgible-logo", "edgible-symbol", "favicon")):
            return tag

        extra = ["decoding=\"async\""]
        if "width=" not in tag:
            size = image_size(resolve(src.group(1), out, page))
            if size:
                extra.insert(0, f'width="{size[0]}" height="{size[1]}"')
        # The hero is in the opening screen and is the largest thing on it, so it
        # is fetched at once. Everything else waits until it is scrolled to.
        hero = 'class="hero"' in tag
        extra.append('loading="eager" fetchpriority="high"' if hero else 'loading="lazy"')

        body = tag[:-1].rstrip().rstrip("/").rstrip()
        return f"{body} {' '.join(extra)}>"

    return re.sub(r"<img\b[^>]*>", repl, html)


def main() -> int:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
    pages = 0
    for page in out.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        fixed = ROOT_CANONICAL.sub(SITE_URL, html)
        fixed = fix_images(fixed, out, page)
        if fixed != html:
            page.write_text(fixed, encoding="utf-8")
            pages += 1

    sitemap = out / "sitemap.xml"
    if sitemap.exists():
        text = ROOT_CANONICAL.sub(SITE_URL, sitemap.read_text(encoding="utf-8"))
        sitemap.write_text(text, encoding="utf-8")
        # MkDocs writes a gzipped copy alongside it, which would otherwise still
        # advertise the URL we just stopped using.
        gz = out / "sitemap.xml.gz"
        if gz.exists():
            import gzip

            with gzip.GzipFile(gz, "wb", mtime=0) as fh:
                fh.write(text.encode("utf-8"))

    print(f"polished {pages} pages under {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
