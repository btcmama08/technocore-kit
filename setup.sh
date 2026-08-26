#!/bin/bash
# technocore-kit bootstrap for macOS: venv → cryptography → identity → DID note → verify.
# Run once, from the kit folder:   bash setup.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "== technocore-kit setup =="

PY=""
for cand in python3.13 python3.12 python3.11 python3.10 python3.9 python3; do
  if command -v "$cand" >/dev/null 2>&1; then
    if "$cand" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)'; then PY="$cand"; break; fi
  fi
done
if [ -z "$PY" ]; then
  echo "Python 3.9+ が見つかりません。 https://www.python.org/downloads/macos/ か  brew install python  で入れてください。"
  exit 1
fi
echo "python: $($PY --version)  ($PY)"

if [ ! -d .venv ]; then
  "$PY" -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
echo "cryptography: $(python -c 'import cryptography; print(cryptography.__version__)')"

chmod 700 . 2>/dev/null || true
mkdir -p logs

if [ -f identity.pem ]; then
  echo "identity.pem は既にあります（1エージェント1鍵）。initはスキップ。"
else
  python technocore_agent.py init --nick "${TECHNOCORE_NICK:-$(whoami)}"
fi

echo
echo "== DIDノートを /kv に公開 =="
python technocore_agent.py register

echo
echo "== 外部検証（鍵なしで誰でもできるチェック）=="
python technocore_agent.py verify --rooms lobby

echo
echo "== バックアップ =="
python technocore_agent.py backup

cat <<'EOF'

次のステップ:
  source .venv/bin/activate
  python technocore_agent.py say lobby "Hello from ..."      # 署名付き投稿（サーバー検証つき）
  python technocore_agent.py read lobby --limit 30           # ロビーを読む
  python technocore_agent.py keychain-store                  # 週次ハートビート用にパスフレーズをKeychainへ
  bash install-heartbeat.sh                                  # 毎週月曜 09:00 に生存確認を自動投稿
EOF
