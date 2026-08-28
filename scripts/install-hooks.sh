#!/usr/bin/env bash
# Install git hooks that rebuild the guides after a commit or a pull.
#
# The hook always runs scripts/build.sh, which is the strict link check. If the
# container is already running it also rebuilds and restarts the image, so what
# is published matches the commit.
set -euo pipefail

cd "$(dirname "$0")/.."
REPO="$PWD"
HOOKS="$(git rev-parse --git-path hooks)"

mkdir -p "$HOOKS"

for hook in post-commit post-merge post-checkout; do
    cat > "$HOOKS/$hook" <<EOF
#!/usr/bin/env bash
# Installed by scripts/install-hooks.sh
set -euo pipefail
cd "$REPO"
if [ -x .venv/bin/mkdocs ]; then
    PATH="$REPO/.venv/bin:\$PATH"
fi
export PATH
LOG=/tmp/edgible-guides-build.log

if ! ./scripts/build.sh >"\$LOG" 2>&1; then
    echo "guides: BUILD FAILED, see \$LOG" >&2
    exit 0
fi
echo "guides: site rebuilt"

if command -v docker >/dev/null 2>&1 && [ -n "\$(docker compose ps -q guides 2>/dev/null)" ]; then
    if docker compose up -d --build >>"\$LOG" 2>&1; then
        echo "guides: container updated"
    else
        echo "guides: container update FAILED, see \$LOG" >&2
    fi
fi
EOF
    chmod +x "$HOOKS/$hook"
done

echo "Installed post-commit, post-merge and post-checkout hooks in $HOOKS"
echo "Build log: /tmp/edgible-guides-build.log"
