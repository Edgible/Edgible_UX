---
name: edgible-publish
description: Publish a local port on this machine to a real https:// URL via Edgible (no port-forward, no Tailscale). Use when the user wants to put an app on the internet, Edgible it up, or expose nginx/OpenClaw/Control UI.
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

# Edgible publish

OpenClaw talks to this computer. Edgible is the door to the internet. This skill creates (or reuses) an Edgible app for a **local TCP port that is already listening**, waits until the certificate is ready, and returns the exact `https://<app>.<org>.edgible.com` URL.

Do **not** install Edgible, create an org, or register a device. Stop if `edgible` is missing or not logged in.

## When to use

- “Publish this app / site / port with Edgible”
- “Give me a public URL for hello-world”
- “Put OpenClaw Control UI on the internet”

## What to collect

Ask only if missing:

| Field | Notes |
| --- | --- |
| **name** | DNS label, lowercase, digits, hyphens. Examples: `hello-world`, `openclaw-ui`. |
| **port** | Local listen port on this box (hello-world nginx is **8081**; OpenClaw Control UI is **18789**). |
| **auth** | `none` (public), `org` (must sign in to the Edgible org), or `api-key` (Bearer). |

Defaults:

- Port **18789** → `org`. Never `none`.
- A throwaway public page the user called Hello World / public site → `none`, but **confirm** before `none`.
- Anything that looks like a dashboard, Gateway, or private tool → `org`.

## How to run

If the user already gave **name**, **port**, and public vs org, **do not ask again**. Your first tool call must be `exec` of the helper (not a long plan). Tell them in one short line that you are running it.

Use this exact command (expand `$HOME`). Do **not** invent extra `edgible` flags. Do **not** `eval` the user’s sentence as a shell command.

```bash
python3 -u "$HOME/.openclaw/workspace/skills/edgible-publish/scripts/publish.py" --name <name> --port <port> --auth-modes <none|org|api-key>
```

If that path is missing, try `{baseDir}/scripts/publish.py` the same way.

Optional: `--device-name mini-pc` if more than one serving device exists.

The script is idempotent: if that app name already exists, it prints the existing URL. It prints `URL=` when finished. Paste that line back to the user. If `exec` is waiting for approval, say so — do not sit silent.

## Hard rules

- Never `--auth-modes none` on port **18789**.
- Do not port-forward. Do not bind OpenClaw Gateway to `0.0.0.0`.
- Do not paste gateway tokens, API keys, or WhatsApp session files into chat.
- Do not publish through Edgible: WhatsApp, Telegram, Discord, or Ollama on the same box.
- Do not set OpenClaw `gateway.auth` to none.
- If the helper fails, show its stderr. Do not retry by switching 18789 to `none`.

## After Control UI (port 18789)

Publishing the app is not enough for the dashboard JS. If the user just created **openclaw-ui**, remind them (do not silently edit config unless they asked):

- `openclaw config set gateway.controlUi.allowedOrigins` must include `https://` + that exact hostname
- `openclaw gateway restart`
- First browser: gateway token + `openclaw devices approve`

## Not this skill

Installing Edgible, `edgible auth login`, device register, Docker/nginx setup, Cursor ACP, WhatsApp login.
