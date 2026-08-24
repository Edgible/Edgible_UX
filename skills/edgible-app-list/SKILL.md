---
name: edgible-app-list
description: List Edgible apps. Default is this OpenClaw machine (the serving device you are on), not the whole org. Use when the user asks what is published, which URLs, or apps on this box. Pass --all only if they want every device in the org.
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

# Edgible app list

Shows Edgible applications. **Default: only this box** — the serving device colocated with OpenClaw (same machine as the Gateway). That is what “what apps do I have?” means in WhatsApp/Control UI when the org also has AWS or another mini-PC.

`--all` is the whole organisation (every serving device). Use only if they said all devices / the whole org.

## When to use

- “What Edgible apps are on this machine?”
- “List my URLs / what’s published?”
- “Show all apps in the org” → `--all`

## How to run

If they already said this box vs whole org, **do not ask again**. First tool call is `exec`.

This OpenClaw box (several serving devices in the org — pass the guest you are on):

```bash
python3 -u "$HOME/.openclaw/workspace/skills/edgible-app-list/scripts/list.py" --device-name macbookairubuntu2404vm
```

Whole org:

```bash
python3 -u "$HOME/.openclaw/workspace/skills/edgible-app-list/scripts/list.py" --all
```

If that path is missing, try `{baseDir}/scripts/list.py`. If the helper asks for `--device-name`, retry with this machine, not AWS.

**Required chat reply:** after `exec`, paste `SCOPE=`, `COUNT=`, and each `NAME=… URL=…` line into the bubble. Do not stop on the tool card. Do not dump WhatsApp `chat_id` JSON.

## Hard rules

- Default is **this device**, not `--all`.
- Do not delete or create apps in this skill.
- Do not paste tokens.
- If exec needs approval, say so.

## Not this skill

**edgible-app-create**, **edgible-app-delete**.
