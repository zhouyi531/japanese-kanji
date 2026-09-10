#!/usr/bin/env bash
# Operational entrypoint for japanese-kanji — humans and Service Hub use this file.
set -euo pipefail

SERVICE_NAME="japanese-kanji"
PORT="18473"
HEALTH_PATH="/health.json"
RUNTIME_BIN="/home/linuxbrew/.linuxbrew/bin"
UI_PORT="19473"
PROCS=(service)

run_service() {
  cd "$ROOT"
  exec "$RUNTIME_BIN/python3" "$ROOT/server.py" --bind 0.0.0.0 --port "$PORT"
}

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_DIR="$ROOT/.run"
[ -n "$RUNTIME_BIN" ] && [ -d "$RUNTIME_BIN" ] && PATH="$RUNTIME_BIN:$PATH"
mkdir -p "$RUN_DIR"

if [ "${1:-}" = "_exec" ]; then "run_${2}"; exit $?; fi

HEALTH_URL="http://127.0.0.1:$PORT$HEALTH_PATH"
FOREGROUND=0

is_alive() { local pf="$RUN_DIR/$1.pid"; [ -f "$pf" ] && kill -0 "$(cat "$pf")" 2>/dev/null; }

spawn() {
  local name="$1" log="$RUN_DIR/$1.log"
  if is_alive "$name"; then
    echo "  $name already running (pid $(cat "$RUN_DIR/$name.pid"))"; return
  fi
  if [ "$FOREGROUND" -eq 1 ]; then
    bash "$ROOT/run.sh" _exec "$name" >"$log" 2>&1 &
  else
    setsid bash "$ROOT/run.sh" _exec "$name" >"$log" 2>&1 </dev/null &
  fi
  echo $! >"$RUN_DIR/$name.pid"
}

health_wait() {
  local i
  for i in $(seq 1 "${1:-45}"); do
    curl -fsS "$HEALTH_URL" >/dev/null 2>&1 && return 0
    sleep 1
  done
  return 1
}

cmd_start() {
  for p in "${PROCS[@]}"; do spawn "$p"; done
  if health_wait 45; then echo "  health OK: $HEALTH_URL"
  else echo "  WARN: not healthy yet — see ./run.sh logs" >&2; fi
  echo
  echo "$SERVICE_NAME started:"
  echo "  service   : http://127.0.0.1:$PORT"
  echo "  LAN       : http://192.168.1.21:$PORT"
  echo "  health    : $HEALTH_URL"
  echo "  quick-try : ./run.sh ui   → http://127.0.0.1:$UI_PORT"
  echo "  logs      : ./run.sh logs"
  for p in "${PROCS[@]}"; do is_alive "$p" && echo "  - $p (pid $(cat "$RUN_DIR/$p.pid"))"; done
  if [ "$FOREGROUND" -eq 1 ]; then
    trap 'cmd_stop; exit 0' TERM INT
    echo "  (foreground — supervising; SIGTERM/Ctrl-C stops all)"
    wait
  fi
}

cmd_stop() {
  local i p pf pid
  for ((i=${#PROCS[@]}-1; i>=0; i--)); do
    p="${PROCS[$i]}"; pf="$RUN_DIR/$p.pid"; [ -f "$pf" ] || continue
    pid="$(cat "$pf")"
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
      for _ in 1 2 3 4 5; do kill -0 "$pid" 2>/dev/null || break; sleep 1; done
      kill -9 "$pid" 2>/dev/null || true
      echo "  stopped $p (pid $pid)"
    fi
    rm -f "$pf"
  done
}

cmd_status() {
  for p in "${PROCS[@]}"; do
    if is_alive "$p"; then echo "  $p: running (pid $(cat "$RUN_DIR/$p.pid"))"
    else echo "  $p: stopped"; fi
  done
  if curl -fsS "$HEALTH_URL" >/dev/null 2>&1; then echo "  health: OK"; else echo "  health: DOWN"; fi
}

cmd_logs() { local p="${1:-${PROCS[0]}}"; tail -n "${LINES:-80}" -f "$RUN_DIR/$p.log"; }
cmd_review() { exec "$RUNTIME_BIN/python3" "$ROOT/scripts/review_store.py" "$@"; }
cmd_health() { curl -fsS "$HEALTH_URL" && echo || { echo "DOWN: $HEALTH_URL" >&2; exit 1; }; }
cmd_ui() {
  echo "quick-try UI → http://127.0.0.1:$UI_PORT  (proxy /api → http://127.0.0.1:$PORT)"
  exec "$RUNTIME_BIN/python3" "$ROOT/ui/serve.py" "$UI_PORT" "$PORT"
}

case "${1:-start}" in
  start) cmd_start ;;
  -f|--foreground) FOREGROUND=1; cmd_start ;;
  stop) cmd_stop ;;
  restart) cmd_stop; cmd_start ;;
  status) cmd_status ;;
  logs) cmd_logs "${2:-}" ;;
  health) cmd_health ;;
  review) shift; cmd_review "$@" ;;
  ui) cmd_ui ;;
  *) echo "usage: run.sh [start|-f|stop|restart|status|logs [name]|health|review [list|remove <id>|clear]|ui]" >&2; exit 2 ;;
esac
