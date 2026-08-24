---
name: edgible-app-create
description: Create (publish) an Edgible app for a local listening port and return the https:// URL. Use when the user wants to put a site on the internet, Edgible it up, or expose nginx/OpenClaw Control UI. Pair with edgible-app-delete to take it down.
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - edgible
        - python3
    emoji: "🚪"
    homepage: https://github.com/Edgible/Edgible_UX
---

# Edgible app create

OpenClaw talks to this computer. Edgible is the door. This skill runs `edgible app create existing` for a **local TCP port that is already listening**, waits until the certificate is ready, and returns `https://<app>.<org>.edgible.com`.

Do **not** install Edgible, create an org, or register a device. Stop if `edgible` is missing or not logged in. To unpublish, use **edgible-app-delete**.

## WhatsApp noise

OpenClaw may attach hidden JSON (`chat_id`, `message_id`, `sender`, `e164`, `inbound_event_kind`). That is **not** the user request. Never print it. Never say you cannot share runtime context instead of working. Run the helper for the real task (create an app / the `/skill` line).

## When to use

- “Publish this app / site / port with Edgible”
- “Create an Edgible URL for hello-world / skill-test”
- “Put OpenClaw Control UI on the internet”

## What to collect

Ask only if missing:

| Field | Notes |
| --- | --- |
| **name** | DNS label, lowercase, digits, hyphens. Examples: `hello-world`, `skill-test`, `openclaw-ui`. |
| **port** | Local listen port (hello-world nginx is often **8081**; skill-test is **8082**; Control UI is **18789**). |
| **auth** | `none` (public), `org` (must sign in), or `api-key` (Bearer). |

Defaults:

- Port **18789** → `org`. Never `none`.
- A throwaway public page (Hello World / skill-test) → `none`, but **confirm** before `none`.
- Anything that looks like a dashboard, Gateway, or private tool → `org`.

## How to run

If the user already gave **name**, **port**, and public vs org, **do not ask again**. First tool call must be `exec` of the helper. One short line that you are running it.

```bash
python3 -u "$HOME/.openclaw/workspace/skills/edgible-app-create/scripts/create.py" --name <name> --port <port> --auth-modes <none|org|api-key>
```

If that path is missing, try `{baseDir}/scripts/create.py`.

Optional: `--device-name <this-machine>` if more than one serving device exists. Use the guest you are on (e.g. `macbookairubuntu2404vm`), not another box in the same org.

The script is idempotent: if that app name already exists, it prints the existing URL.

**Required chat reply:** after `exec` finishes, send a normal assistant message. Do not stop on the tool card. Copy these lines from the helper stdout, verbatim:

```text
URL=https://….edgible.com
```

Also include `AUTH=` if present. One extra sentence is fine (“open this on your phone”). Never end the turn with only a tool result and no URL in the bubble.

## Hard rules

- Never `--auth-modes none` on port **18789**.
- Do not port-forward. Do not bind OpenClaw Gateway to `0.0.0.0`.
- Do not paste gateway tokens, API keys, or WhatsApp session files into chat.
- Do not publish through Edgible: WhatsApp, Telegram, Discord, or Ollama on the same box.
- Do not set OpenClaw `gateway.auth` to none.
- If the helper fails, show its stderr. Do not retry by switching 18789 to `none`.

## After Control UI (port 18789)

- `openclaw config set gateway.controlUi.allowedOrigins` must include `https://` + that exact hostname
- `openclaw gateway restart`
- First browser: gateway token + `openclaw devices approve`

## Not this skill

Installing Edgible, device register, Docker/nginx setup, Cursor ACP, WhatsApp login, deleting an app (**edgible-app-delete**).
