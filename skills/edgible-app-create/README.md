# edgible-app-create (OpenClaw skill)

Create an Edgible app for a **local listening port** and return `https://<app>.<org>.edgible.com`. Inverse: [edgible-app-delete](../edgible-app-delete/).

OpenClaw skill names here follow **`edgible-app-<verb>`**, matching `edgible app create` / `edgible app delete`. Chat words like “publish” belong in the description, not the slug.

Copy this folder onto the Gateway host. Not a Cursor skill. Not Edgible signup.

## Install on the OpenClaw VM

Edgible CLI logged in, serving device healthy, OpenClaw Gateway running.

```bash
mkdir -p ~/.openclaw/workspace/skills
cp -R /path/to/Edgible_UX/skills/edgible-app-create ~/.openclaw/workspace/skills/
cp -R /path/to/Edgible_UX/skills/edgible-app-delete ~/.openclaw/workspace/skills/
# remove a leftover old name if you installed it earlier:
# rm -rf ~/.openclaw/workspace/skills/edgible-publish

openclaw skills list
openclaw gateway restart
```

You want **edgible-app-create** and **edgible-app-delete**. New chat (`/new`).

## Build a test app (nginx on 8082)

Docker must work. Container name **`edgible-skill-test`**. The block starts with `docker rm -f`, so it is safe to paste again.

If **8082** is taken, stop that process or pick another host port and pass it to `create.py`.

```bash
mkdir -p ~/edgible-skill-test
cat > ~/edgible-skill-test/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>OpenClaw Edgible Skill Test</title></head>
<body>
  <h1>OpenClaw Edgible Skill Test</h1>
  <p>Served from this machine through Edgible.</p>
</body>
</html>
EOF

docker rm -f edgible-skill-test 2>/dev/null || true
docker run -d --name edgible-skill-test \
  -p 8082:80 \
  -v ~/edgible-skill-test:/usr/share/nginx/html:ro \
  nginx:alpine
sleep 5
curl -sS http://127.0.0.1:8082/
```

You want **OpenClaw Edgible Skill Test**. Local only until Edgible creates the app.

```bash
docker rm -f edgible-skill-test
```

## Helper (optional — skip OpenClaw)

```bash
python3 -u ~/.openclaw/workspace/skills/edgible-app-create/scripts/create.py \
  --name skill-test --port 8082 --auth-modes none \
  --device-name macbookairubuntu2404vm
```

Port **18789** with `--auth-modes none` is rejected. Existing app name → reprints `URL=`.

Several serving devices → add `--device-name` for **this** box (`macbookairubuntu2404vm`, not `awsubuntu24`).

## Test

`/skill` still goes to Gemini. Force the skill; success is the helper’s `URL=` line.

```bash
openclaw skills list
```

```text
/skill edgible-app-create Create a public Edgible app named skill-test for nginx on port 8082. If it already exists, just give me the URL.
```

Same from WhatsApp. Open the URL on cellular; confirm **OpenClaw Edgible Skill Test**.

If chat spins and no app appears: exec approval (`approve-reads`), or the model never ran `create.py`. Run the Helper. Then take it down with `/skill edgible-app-delete`.

**If WhatsApp replies with `chat_id` / `sender` / `inbound_event_kind` JSON:** that is OpenClaw’s hidden channel metadata. The model echoed it; **`create.py` did not run.** Recopy `SKILL.md` onto the VM, `/new`, try again. Or skip the model:

```text
/exec python3 -u $HOME/.openclaw/workspace/skills/edgible-app-create/scripts/create.py --name skill-test --port 8082 --auth-modes none --device-name macbookairubuntu2404vm
```

Control UI `/skill` is a useful A/B: if it works there and WhatsApp dumps JSON, it is the WhatsApp runtime-context leak, not the helper.
