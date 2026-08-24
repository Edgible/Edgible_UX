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

In chat, start a **new** session (`/new`) so the agent sees the skill. Invoke with `/skill edgible-publish` or a normal sentence (“Publish hello-world on Edgible as a public site”).

## Helper (no model)

On the VM, same flags the skill tells the agent to use:

```bash
python3 ~/.openclaw/workspace/skills/edgible-publish/scripts/publish.py \
  --name hello-world --port 8081 --auth-modes none

python3 ~/.openclaw/workspace/skills/edgible-publish/scripts/publish.py \
  --name openclaw-ui --port 18789 --auth-modes org
```

Port **18789** with `--auth-modes none` is rejected. If the app name already exists, the script reprints the URL.

## Test

```bash
openclaw agent --message "Publish the local hello-world nginx (port 8081) on Edgible as a public site. Use the edgible-publish skill. If it already exists, just give me the URL."
```

Then the same from WhatsApp. You want a reply that contains `https://` and `edgible.com`.
