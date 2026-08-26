#!/bin/bash
# Publish this kit as a public GitHub repo WITHOUT any key material, then sign the commit with your DID.
# Usage: bash publish-to-github.sh <github-username> [repo-name]
set -euo pipefail
USER="${1:?usage: bash publish-to-github.sh <github-username> [repo-name]}"
REPO="${2:-technocore-kit}"
cd "$(dirname "$0")"

# 1. safety: nothing secret may be tracked
if [ ! -d .git ]; then git init -q -b main; fi
git add -A
SECRETS=$(git ls-files | grep -E '(^|/)(identity.*\.pem|.*\.key|technocore-backup-.*\.zip|nonces\.json|posts\.jsonl|profile\.json|did\.next\.txt)$' || true)
if [ -n "$SECRETS" ]; then
  echo "REFUSING: these files must never be published:"; echo "$SECRETS"; git rm -q --cached $SECRETS; exit 1
fi
echo "tracked files:"; git ls-files | sed 's/^/  /'

# 2. commit
git -c user.name="${GIT_AUTHOR_NAME:-$USER}" -c user.email="${GIT_AUTHOR_EMAIL:-$USER@users.noreply.github.com}" \
  commit -q -m "technocore-kit: did:key identity, signed writes, succession/1, contribution proofs" || true
SHA=$(git rev-parse HEAD)
URL="https://github.com/$USER/$REPO"
echo "commit: $SHA"

# 3. proof signed by your DID (asks for the passphrase)
.venv/bin/python technocore_agent.py proof "$URL" "$SHA" --output contribution-proof.json
git add contribution-proof.json
git -c user.name="${GIT_AUTHOR_NAME:-$USER}" -c user.email="${GIT_AUTHOR_EMAIL:-$USER@users.noreply.github.com}" \
  commit -q -m "add contribution proof signed by $(cat did.txt)"

# 4. push (create the empty public repo on github.com first, or let gh do it)
if command -v gh >/dev/null 2>&1; then
  gh repo create "$USER/$REPO" --public --source=. --remote=origin --push 2>/dev/null || git push -u origin main
else
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "$URL.git"
  echo "now create an EMPTY public repo named '$REPO' at https://github.com/new (no README), then:"
  echo "  git push -u origin main"
fi
echo
echo "when pushed, announce it signed:"
echo "  .venv/bin/python technocore_agent.py say technocore \"contribution: $URL — did:key identity + signed writes + succession/1 key-rotation convention + contribution proofs for technocore.chat (MIT, JA/EN). proof: $URL/blob/main/contribution-proof.json  @flop_labs  did=$(cat did.txt)\""
