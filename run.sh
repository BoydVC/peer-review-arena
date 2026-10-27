#!/usr/bin/env bash
# Start (or restart) Peer Review Arena on 127.0.0.1:4333
set -euo pipefail
cd "$(dirname "$0")"
python3 build_seeds.py
pkill -f "peer-review-arena/server.py" 2>/dev/null || true
sleep 0.3
setsid nohup python3 "$PWD/server.py" > /tmp/peer-review-arena-server.log 2>&1 < /dev/null &
sleep 0.7
code=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:4333/api/health || echo "000")
echo "Peer Review Arena -> http://127.0.0.1:4333/ (health HTTP ${code})"
