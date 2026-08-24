# edgible-publish (OpenClaw skill)

Teach OpenClaw to **publish a local listening port** through Edgible and return a real `https://<app>.<org>.edgible.com` URL. Chat (WhatsApp, Control UI) is the hands; Edgible is the door.

This folder is the skill source. OpenClaw only loads it after you copy or symlink it onto the Gateway host.

## What it is not

- Not a Cursor skill (not `.cursor/skills`)
- Not Edgible signup, org create, or device register
- Not a tunnel for WhatsApp / Telegram / Discord

## Install on the OpenClaw VM

Edgible CLI already logged in, serving device healthy, OpenClaw Gateway running.

```bash
# from a clone of this repo on the VM, or scp the folder
mkdir -p ~/.openclaw/workspace/skills
cp -R /path/to/Edgible_UX/skills/edgible-publish ~/.openclaw/workspace/skills/
# or: ln -sfn /path/to/Edgible_UX/skills/edgible-publish ~/.openclaw/workspace/skills/edgible-publish

openclaw skills list
openclaw gateway restart
```

In chat, start a **new** session (`/new`) so the agent sees the skill. Invoke with `/skill edgible-publish` or a normal sentence (“Publish skill-test on Edgible as a public site”).

## Build a test app (nginx on 8082)

On the VM. Docker must already work (same as the getting-started chapter). This is a **new** page and container, not the Hello World app.

The container is always named **`edgible-skill-test`**. The block starts with `docker rm -f`, so you can paste it again after you change `index.html` or if the last run left a container behind.

If something else is already on **8082** (the chapter’s `hello-world` nginx), stop it first (`docker stop hello-world`) or map a free host port and pass that port to `publish.py`.

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

You want HTML that contains **OpenClaw Edgible Skill Test**. That is local only — the phone cannot see `:8082` until Edgible publishes it.

To throw the test container away (the HTML in `~/edgible-skill-test` stays):

```bash
docker rm -f edgible-skill-test
```

## Helper (optional — skip OpenClaw)

Only if you want to check Edgible **without** the agent. This is the same script the skill is supposed to run. It does **not** test whether OpenClaw loaded the skill — that is the next section.

On the VM:

```bash
python3 -u ~/.openclaw/workspace/skills/edgible-publish/scripts/publish.py \
  --name skill-test --port 8082 --auth-modes none \
  --device-name macbookairubuntu2404vm

python3 ~/.openclaw/workspace/skills/edgible-publish/scripts/publish.py \
  --name openclaw-ui --port 18789 --auth-modes org
```

Port **18789** with `--auth-modes none` is rejected. If the app name already exists, the script reprints the URL.

## Test

This is the skill check. English “please use Edgible” is not enough — Gemini can run `edgible` without loading **edgible-publish**. Force the skill, then look for the helper’s `URL=` line.

On the VM, confirm it is loaded:

```bash
openclaw skills list
```

You want **edgible-publish**. New chat (`/new` in Control UI or WhatsApp), then send **exactly** this (the `/skill` prefix is what selects it):

```text
/skill edgible-publish Publish the nginx on port 8082 as a public Edgible app named skill-test. If it already exists, just give me the URL.
```

Same line from WhatsApp. You want a reply that includes **`URL=https://`** … **`edgible.com`** (that string is printed by `scripts/publish.py`, not invented by the model). Open that URL on a phone (cellular) and confirm **OpenClaw Edgible Skill Test**.

If the reply has a URL but no `URL=` line, the model may have skipped the helper — run the optional Helper section, then try `/skill edgible-publish` again.

**If chat just spins and no app appears:** `/skill` still goes to Gemini. “Doing something” is usually the model thinking, not `publish.py`. Copy the updated `SKILL.md` onto the VM, `/new`, and check Control UI for an **exec approval** (common after `approve-reads`). Prove the helper without OpenClaw:

```bash
python3 -u ~/.openclaw/workspace/skills/edgible-publish/scripts/publish.py \
  --name skill-test --port 8082 --auth-modes none \
  --device-name macbookairubuntu2404vm
```

If the helper says **Several serving devices**, add `--device-name` for **this** box (on the getting-started VM that is `macbookairubuntu2404vm`, not `awsubuntu24`). Then retry. The script prints `edgible-publish: starting` immediately, then `URL=`. If that works and `/skill` still stays mute, the skill is loaded but **exec never ran**.
