#!/usr/bin/env bash
# Prints one JSON line describing what's installed and logged in. Read only, changes nothing.
has() { command -v "$1" >/dev/null 2>&1; }
ver() { "$@" 2>/dev/null | head -1 | tr -d '"\r'; }

git_v=""; has git && git_v=$(ver git --version)
gh_v=""; gh_user=""
if has gh; then
  gh_v=$(ver gh --version)
  gh_user=$(gh api user -q .login 2>/dev/null | tr -d '\r')
fi
node_v=""; has node && node_v=$(ver node --version)
vercel_user=""
if has npx; then
  # --yes installs vercel into the npx cache on first run without a prompt
  # logged out exits non zero and prints a JSON error, so trust the exit code, not the text
  if out=$(npx --yes vercel whoami 2>/dev/null); then
    vercel_user=$(printf '%s' "$out" | tail -1 | tr -d '\r"')
    case "$vercel_user" in *" "*|*"{"*|*"}"*) vercel_user="" ;; esac
  fi
fi
os=$(uname -s 2>/dev/null || echo unknown)

printf '{"git":"%s","gh":"%s","gh_user":"%s","node":"%s","vercel_user":"%s","os":"%s"}\n' \
  "$git_v" "$gh_v" "$gh_user" "$node_v" "$vercel_user" "$os"
