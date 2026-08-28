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

# Staged as README.md, not index.md: MkDocs treats README.md as a directory
# index, and keeping the name means links written for GitHub still resolve.
cp README.md "$STAGE/README.md"
cp capabilities.md "$STAGE/capabilities.md"
cp -R guides "$STAGE/guides"
cp static/robots.txt "$STAGE/robots.txt"
cp -R static/stylesheets "$STAGE/stylesheets"

python3 scripts/gen_llms.py "$STAGE"

mkdocs build --strict

# Serve the raw markdown next to the rendered HTML.
cp README.md "$OUT/README.md"
cp README.md "$OUT/index.md"
cp capabilities.md "$OUT/capabilities.md"
while IFS= read -r file; do
  mkdir -p "$OUT/$(dirname "$file")"
  cp "$file" "$OUT/$file"
done < <(find guides -name '*.md')

echo
echo "Built $OUT"
echo "Preview:  python3 -m http.server -d $OUT 8000"
echo "Publish:  docker compose up -d --build   # then edgible app create"
