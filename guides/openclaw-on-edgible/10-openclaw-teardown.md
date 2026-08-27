# 10. Tear down OpenClaw

**Stop the agent and its Edgible door. Leave n8n, Ollama, and the serving agent unless you say otherwise.**

This VM may still be [1. n8n on Edgible](../n8n-on-edgible/README.md) and [3. LLM on Edgible](../llm-on-edgible/README.md). Default teardown is **OpenClaw only**: Telegram / WhatsApp, **openclaw-ui**, Gateway, optional `~/.openclaw`. Do **not** delete **n8n**, **n8n-hooks**, or **ollama**. Do **not** uninstall the Edgible serving agent. **hello-world** stays up unless you opt in at the end.

## 10.1 The job

You close chat doors, delete the **openclaw-ui** app, stop the Gateway, and optionally wipe OpenClaw’s config. Cellular **openclaw-ui** should fail. **hello-world** (and n8n / ollama apps) still load if you left them.

**Done when**

- `edgible app list` has **no** **openclaw-ui**.
- `ss -ltnp | grep 18789` is empty.
- Phone **openclaw-ui** URL does not chat (cert gone or connection fails).
- **n8n** / **n8n-hooks** / **ollama** still listed if you had created them.
- Port **18789** is still not forwarded.

**Need first:** You finished enough of this series that OpenClaw exists (at least [chapter 2](02-openclaw-on-the-box.md)). Skip steps for things you never installed.

**Not this chapter:** deleting the Ubuntu VM, `edgible auth logout` (keeps the CLI off this box), or publishing anything new.

## 10.2 Stop jobs and chat doors (Ubuntu VM)

ACP sessions and site crons keep running until you stop them.

```bash
# Control UI or CLI: close Cursor ACP sessions if any
# openclaw /acp close   (from a chat that still works)
```

In Control UI → **Automations**, delete hourly Hello World / On this day jobs ([chapter 4](04-openclaw-changes-edgible-site.md) / [chapter 8](08-cursor-agent.md)).

Telegram ([chapter 6](06-telegram-pocket-client.md)) — Gateway host:

```bash
openclaw config set channels.telegram.enabled false
openclaw config unset channels.telegram.botToken
openclaw gateway restart
```

In Telegram: **@BotFather** → your bot → **API Token** → **Revoke** if you will not use that bot again.

WhatsApp ([chapter 7](07-whatsapp-pocket-client.md)):

```bash
openclaw channels logout --channel whatsapp
openclaw gateway restart
```

## 10.3 Delete the Control UI app

Closes `https://openclaw-ui.<org>.edgible.com`. Gateway can still be up on loopback until 10.4.

```bash
edgible app list
edgible app delete --name openclaw-ui
edgible app list
```

You want **openclaw-ui** gone. **hello-world** (and n8n / ollama) still there.

Never **None** on **18789** on the way out — delete the app; do not “make it public then remove it.”

## 10.4 Stop the Gateway

```bash
openclaw gateway stop
openclaw gateway uninstall
ss -ltnp | grep 18789
```

Empty `ss` is success. If `uninstall` is unknown, `openclaw gateway stop` is enough; then `systemctl --user list-units | grep -i openclaw` and disable whatever is left.

Optional: turn off linger if you enabled it only for this Gateway:

```bash
sudo loginctl disable-linger "$USER"
```

## 10.5 Optional — skill and config wipe

Remove the **edgible** skill ([chapter 5](05-edgible-openclaw-skill.md)):

```bash
openclaw skills list
openclaw skills uninstall edgible
```

If `uninstall` is missing, stop the Gateway first, then delete the **edgible** folder under `~/.openclaw` (skills / workspace). Do not delete the whole `~/.openclaw` unless you mean 10.6.

## 10.6 Optional — full OpenClaw wipe

This removes keys in `~/.openclaw/.env` (Gemini, DeepSeek, …) from **this VM**. Revoke those keys in the provider consoles if they leaked or you are done with them.

```bash
rm -rf ~/.openclaw
```

The `openclaw` binary may still be on PATH (installer / nvm). Remove it only if you will not reinstall: follow OpenClaw’s uninstall docs for this install, or delete the npm/nvm copy you used in [chapter 2](02-openclaw-on-the-box.md).

## 10.7 Optional — Hello World too

Only if you also want the shared public page gone. **Skip** if n8n or LLM-on-Edgible still uses this VM.

```bash
edgible app delete --name hello-world
docker stop hello-world && docker rm hello-world
```

Leave `~/hello-world` on disk unless you want that HTML gone too. Do **not** `edgible agent uninstall` here — that serving device is still [guide 1](../n8n-on-edgible/README.md) / [guide 3](../llm-on-edgible/README.md).

### Verify

- [ ] `edgible app list` has no **openclaw-ui**.
- [ ] Nothing listens on **18789**.
- [ ] Telegram bot does not reply (disabled / token revoked). WhatsApp unlinked if you had it.
- [ ] **n8n**, **n8n-hooks**, **ollama** unchanged if they existed.
- [ ] **hello-world** still loads unless you chose 10.7.
- [ ] Port **18789** is not forwarded.

---

## Next

Series index: [README](README.md). Workflows: [1. n8n on Edgible](../n8n-on-edgible/README.md). Published model: [3. LLM on Edgible](../llm-on-edgible/README.md).
