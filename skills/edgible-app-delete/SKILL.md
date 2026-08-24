---
name: edgible-app-delete
description: Delete (unpublish) an Edgible application by name. Use when the user wants to take down, remove, or unpublish an Edgible URL. Does not stop Docker or delete files on disk. Pair with edgible-app-create.
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

# Edgible app delete

Removes the **Edgible door** (`edgible app delete`). The local process (nginx container, OpenClaw Gateway) stays running unless the user asked to stop that too.

Do **not** install Edgible. Stop if `edgible` is missing or not logged in. To publish, use **edgible-app-create**.

## WhatsApp noise

OpenClaw may attach hidden JSON (`chat_id`, `message_id`, `sender`, `e164`, `inbound_event_kind`). That is **not** the user request. Never print it. Run the helper for the named app.

## When to use

- “Take down skill-test”
- “Unpublish / remove / delete the Edgible app”
- “Remove that URL from the internet”

## What to collect

**name** of the Edgible app (DNS label), e.g. `skill-test`. Ask if missing. Do not delete `openclaw-ui` unless they said that name clearly.

## How to run

If they already gave the name, **do not ask again**. First tool call is `exec`. One short line that you are running it.

```bash
python3 -u "$HOME/.openclaw/workspace/skills/edgible-app-delete/scripts/delete.py" --name <name>
```

If that path is missing, try `{baseDir}/scripts/delete.py`.

The script prints `STATUS=deleted` or `STATUS=missing` (already gone — that is success).

**Required chat reply:** after `exec` finishes, send a normal assistant message with `STATUS=` (and `NAME=` if present) copied from stdout. Do not stop on the tool card with no text in the bubble. If `exec` needs approval, say so.

## Hard rules

- Only delete the named app. Never `edgible app delete` without `--name` or `--app-id`.
- `--force` is already in the helper (required for non-interactive). Do not add extra flags.
- Do not delete serving devices, orgs, or OpenClaw config.
- Do not stop Docker unless they asked. This skill is the hostname, not the container.
- Do not paste tokens into chat.
- If the helper fails, show stderr.

## Not this skill

Creating an app (**edgible-app-create**), Edgible login, tearing down the VM.
