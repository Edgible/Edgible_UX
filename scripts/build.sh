#!/usr/bin/env bash
# Build guides.edgible.com into ./site
#
# The markdown at the repo root stays canonical so the repo reads well on
# GitHub. This stages a copy into build/docs, runs MkDocs, then puts the .md
# sources back into the output so agents can fetch markdown from the same URLs
# the HTML lives at.
set -euo pipefail

cd "$(dirname "$0")/.."

STAGE="build/docs"
OUT="site"

rm -rf "$STAGE"
mkdir -p "$STAGE" "$OUT"

# Before staging, so the committed SVGs cannot drift from the spec they come
# from. Editing one by hand is pointless: the next build overwrites it.
python3 scripts/gen_diagrams.py

# Staged as README.md, not index.md: MkDocs treats README.md as a directory
# index, and keeping the name means links written for GitHub still resolve.
cp README.md "$STAGE/README.md"
cp capabilities.md "$STAGE/capabilities.md"
cp glossary.md "$STAGE/glossary.md"
cp working-with-ai.md "$STAGE/working-with-ai.md"
cp -R guides "$STAGE/guides"
cp static/robots.txt "$STAGE/robots.txt"
cp -R static/stylesheets "$STAGE/stylesheets"
cp -R static/javascripts "$STAGE/javascripts"
cp -R static/fonts "$STAGE/fonts"
cp -R static/images "$STAGE/images"

python3 scripts/gen_llms.py "$STAGE"

# After gen_llms, so the front matter is not mistaken for a page's hook.
python3 scripts/add_dates.py meta "$STAGE"

mkdocs build --strict

# Canonical URLs and image dimensions, which MkDocs cannot get right on its own.
python3 scripts/polish_html.py "$OUT"

# IndexNow proves ownership by asking for a file named after the key, holding the
# key. The key is public by design, so it lives in the repo; publishing it here
# rather than committing the served copy keeps the name and the contents from
# drifting apart.
INDEXNOW_KEY="$(tr -d '[:space:]' < static/indexnow.key)"
printf '%s' "$INDEXNOW_KEY" > "$OUT/$INDEXNOW_KEY.txt"

# Serve the raw markdown next to the rendered HTML.
cp README.md "$OUT/README.md"
cp README.md "$OUT/index.md"
cp capabilities.md "$OUT/capabilities.md"
cp glossary.md "$OUT/glossary.md"
cp working-with-ai.md "$OUT/working-with-ai.md"
while IFS= read -r file; do
  mkdir -p "$OUT/$(dirname "$file")"
  cp "$file" "$OUT/$file"
done < <(find guides -name '*.md')

python3 scripts/add_dates.py header "$OUT"

echo
echo "Built $OUT"
echo "Preview:  python3 -m http.server -d $OUT 8000"
echo "Publish:  docker compose up -d --build   # then edgible app create"
