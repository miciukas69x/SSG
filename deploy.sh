#!/usr/bin/env bash
set -euo pipefail


SSG_DIR="$HOME/Documents/SSG_personal_site/SSG"
SITE_DIR="$HOME/dev/miciukas69x.github.io"
DOMAIN="michailinas.com"

echo "-> Building…"
"$SSG_DIR/build.sh"

echo "-> Checking site repo…"
test -d "$SITE_DIR/.git" || { echo "Site repo not found at $SITE_DIR"; exit 1; }

# Keep existing CNAME (or set it if missing)
CNAME_CONTENT="$DOMAIN"
if [ -f "$SITE_DIR/CNAME" ]; then
  CNAME_CONTENT="$(cat "$SITE_DIR/CNAME")"
fi

echo "-> Cleaning site repo (leaves .git)…"
cd "$SITE_DIR"
git rm -r . >/dev/null 2>&1 || true     # remove tracked files
git clean -fdx                           # remove untracked/ignored junk

echo "-> Copying new build…"
# copy *contents* of docs into repo root
cp -a "$SSG_DIR/docs/." "$SITE_DIR/"

# restore CNAME (GitHub custom domain)
echo "$CNAME_CONTENT" > "$SITE_DIR/CNAME"

echo "-> Committing & pushing…"
git add .
git commit -m "publish: $(date -u +'%Y-%m-%d %H:%M UTC')" || true
git push origin main

echo "✓ Deployed. Check https://$DOMAIN"
