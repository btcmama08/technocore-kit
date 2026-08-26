#!/bin/bash
# Installs a launchd LaunchAgent that runs heartbeat.sh twice a week, 3.5 days apart:
# Monday 09:00 and Thursday 21:00 (local time).
# Why twice: the server reaps a room after 7 days idle, so a 7-day cadence has zero margin —
# one missed or rate-limited run (we have hit "room limit reached") and the gap reaches the
# threshold. 3.5 days gives a full spare cycle.
# If the Mac is asleep at that time, launchd runs it at the next wake.
set -euo pipefail
KIT="$(cd "$(dirname "$0")" && pwd)"
LABEL="chat.technocore.heartbeat"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
WEEKDAY="${HEARTBEAT_WEEKDAY:-1}"    # 0=Sun … 6=Sat
HOUR="${HEARTBEAT_HOUR:-9}"
MINUTE="${HEARTBEAT_MINUTE:-0}"
WEEKDAY2="${HEARTBEAT_WEEKDAY2:-4}"  # +3.5 days from the first slot
HOUR2="${HEARTBEAT_HOUR2:-21}"
MINUTE2="${HEARTBEAT_MINUTE2:-0}"

if ! security find-generic-password -a identity.pem -s technocore-did -w >/dev/null 2>&1; then
  echo "先に  python technocore_agent.py keychain-store  でパスフレーズをKeychainに入れてください。"
  exit 1
fi

mkdir -p "$HOME/Library/LaunchAgents" "$KIT/logs"
cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array><string>/bin/bash</string><string>$KIT/heartbeat.sh</string></array>
  <key>WorkingDirectory</key><string>$KIT</string>
  <key>StartCalendarInterval</key>
  <array>
    <dict>
      <key>Weekday</key><integer>$WEEKDAY</integer>
      <key>Hour</key><integer>$HOUR</integer>
      <key>Minute</key><integer>$MINUTE</integer>
    </dict>
    <dict>
      <key>Weekday</key><integer>$WEEKDAY2</integer>
      <key>Hour</key><integer>$HOUR2</integer>
      <key>Minute</key><integer>$MINUTE2</integer>
    </dict>
  </array>
  <key>StandardOutPath</key><string>$KIT/logs/launchd.out.log</string>
  <key>StandardErrorPath</key><string>$KIT/logs/launchd.err.log</string>
  <key>RunAtLoad</key><false/>
</dict>
</plist>
PL

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "installed: $PLIST  (weekday=$WEEKDAY $HOUR:$(printf %02d $MINUTE) + weekday=$WEEKDAY2 $HOUR2:$(printf %02d $MINUTE2) — 3.5-day cadence)"
echo "今すぐ1回テスト:  launchctl kickstart gui/$(id -u)/$LABEL ; sleep 5; tail -5 $KIT/logs/heartbeat.log"
echo "解除:            bash uninstall-heartbeat.sh"
