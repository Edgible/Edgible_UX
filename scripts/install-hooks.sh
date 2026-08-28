#!/usr/bin/env bash
# Install git hooks that rebuild ./site after a commit or a pull.
#
# nginx serves ./site from a read-only bind mount, so a rebuild is picked up
# immediately. There is no container to restart.
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
./scripts/build.sh >/tmp/edgible-guides-build.log 2>&1 \\
    && echo "guides: site rebuilt" \\
    || echo "guides: BUILD FAILED, see /tmp/edgible-guides-build.log" >&2
EOF
    chmod +x "$HOOKS/$hook"
done

echo "Installed post-commit, post-merge and post-checkout hooks in $HOOKS"
echo "Build log: /tmp/edgible-guides-build.log"
