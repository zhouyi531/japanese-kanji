# japanese-kanji — deployment notes

Deployed from: `/home/austinzhou/code/japanese-kanji`
Date: 2026-09-08

## Runtime (pinned)

- Runtime bin: `/home/linuxbrew/.linuxbrew/bin`
- Interpreter: `/home/linuxbrew/.linuxbrew/bin/python3`
- Verify: `/home/linuxbrew/.linuxbrew/bin/python3 -c "import http.server"`
- Install: no dependencies; Python standard library only

## Service

- Listen address: `0.0.0.0:18473`
- Local URL: `http://127.0.0.1:18473`
- LAN URL: `http://192.168.1.21:18473`
- Health: `http://127.0.0.1:18473/health.json`
- Entrypoint: `/home/linuxbrew/.linuxbrew/bin/python3 /home/austinzhou/code/japanese-kanji/server.py --bind 0.0.0.0 --port 18473`
- Review store: `/home/austinzhou/code/japanese-kanji/data/mistakes.json` (git-ignored runtime state)

## Run it

```bash
./run.sh
./run.sh -f
./run.sh stop
./run.sh restart
./run.sh status
./run.sh logs
./run.sh health
./run.sh review list
./run.sh ui
```

The optional quick-try UI listens on `127.0.0.1:19473`.

## Service Hub

Registered as `japanese-kanji`, with `lifecycle.start` set to `./run.sh -f` via its absolute path.

```bash
curl -sS -X POST http://localhost:1234/services \
  -H 'Content-Type: application/json' -d @service.json
curl -sS http://localhost:1234/services/japanese-kanji
```
