#!/usr/bin/env bash
set -euo pipefail

UPSTREAM_URL="https://github.com/FirestormViewer/phoenix-firestorm.git"
UPSTREAM_BRANCH="Firestorm_7.2.4"
UPSTREAM_PIN="10bd3c9f930c76e1427ddd4ecece6cdf36b4406d"
IMPORT_BRANCH="feature/firestorm-source-import"

fatal() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || fatal "Not in a Git checkout"
cd "$(git rev-parse --show-toplevel)"
[[ -z "$(git status --porcelain)" ]] || fatal "Working tree is not clean; commit/stash changes first"
[[ "$(git branch --show-current)" == "main" ]] || fatal "Run from the main branch of a fresh local clone"
[[ -f LICENSE && -f ROADMAP.md ]] || fatal "TrixieStorm foundation files missing"
[[ "$(git remote get-url origin)" == *"opengenesislink/trixiestormviewer"* ]] || fatal "Wrong origin repository"
if git show-ref --verify --quiet "refs/heads/$IMPORT_BRANCH"; then
  fatal "Import branch already exists. Inspect it before retrying."
fi

if git remote get-url firestorm >/dev/null 2>&1; then
  [[ "$(git remote get-url firestorm)" == "$UPSTREAM_URL" ]] || fatal "Unexpected remote URL for firestorm"
else
  git remote add firestorm "$UPSTREAM_URL"
fi

printf 'Fetching official release branch (can be large)...\n'
git fetch --no-tags firestorm "refs/heads/$UPSTREAM_BRANCH:refs/remotes/firestorm/$UPSTREAM_BRANCH"
ACTUAL="$(git rev-parse "refs/remotes/firestorm/$UPSTREAM_BRANCH^{commit}")"
[[ "$ACTUAL" == "$UPSTREAM_PIN" ]] || fatal "Upstream branch changed. Expected $UPSTREAM_PIN, found $ACTUAL. Review before importing."

git switch -c "$IMPORT_BRANCH"
printf 'Merging pinned Firestorm Git history into %s...\n' "$IMPORT_BRANCH"
if git merge --allow-unrelated-histories --no-commit --no-ff "$UPSTREAM_PIN"; then
  printf 'Merge staged without conflicts. Review: git diff --cached --stat\n'
  printf 'When satisfied: git commit -m "import: Firestorm 7.2.4 source baseline"\n'
else
  printf '\nMerge requires manual review: git status\n'
  printf 'Resolve README/.gitignore/LICENSE or other conflicts without discarding required upstream notices.\n'
  printf 'Finish: git add <resolved files>; git commit\n'
  printf 'Abort:  git merge --abort\n'
  exit 2
fi
printf 'Do not push or merge until build and license audit pass.\n'
