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

## Build a test app (nginx on 8081)

On the VM. Docker must already work (same as the getting-started chapter). This is a **new** page and container, not the Hello World app.

If something is already on **8081** (the chapter’s `hello-world` nginx), stop it first (`docker stop hello-world`) or map a free host port and pass that port to `publish.py`.

```bash
mkdir -p ~/edgible-skill-test
cp ~/.openclaw/workspace/skills/edgible-publish/templates/index.html ~/edgible-skill-test/index.html
# if you have not copied the skill yet:
# cp /path/to/Edgible_UX/skills/edgible-publish/templates/index.html ~/edgible-skill-test/index.html

docker rm -f edgible-skill-test 2>/dev/null || true
docker run -d --name edgible-skill-test \
  -p 8081:80 \
  -v ~/edgible-skill-test:/usr/share/nginx/html:ro \
  nginx:alpine

curl -sS http://127.0.0.1:8081/
```

You want HTML that contains **OpenClaw Edgible Skill Test**. That is local only — the phone cannot see `:8081` until Edgible publishes it.

## Helper (no model)

On the VM, same flags the skill tells the agent to use:

```bash
python3 ~/.openclaw/workspace/skills/edgible-publish/scripts/publish.py \
  --name skill-test --port 8081 --auth-modes none

python3 ~/.openclaw/workspace/skills/edgible-publish/scripts/publish.py \
  --name openclaw-ui --port 18789 --auth-modes org
```

Port **18789** with `--auth-modes none` is rejected. If the app name already exists, the script reprints the URL.

## Test

```bash
openclaw agent --message "Publish the local nginx on port 8081 as an Edgible public site named skill-test. Use the edgible-publish skill. The page title is OpenClaw Edgible Skill Test. If skill-test already exists, just give me the URL."
```

Then the same from WhatsApp. You want a reply that contains `https://` and `edgible.com`. Open that URL on a phone (cellular) and confirm **OpenClaw Edgible Skill Test**.
