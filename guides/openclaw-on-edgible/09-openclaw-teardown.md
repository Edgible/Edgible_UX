# 9. Tear down OpenClaw

**Remove OpenClaw and its hostname without breaking the other guides on this VM.**

## 9.0 Why

This guest is probably shared: it may still be serving [n8n on Edgible](../n8n-on-edgible/README.md) and [LLM on Edgible](../llm-on-edgible/README.md). Uninstalling the serving agent, deleting every app and dropping Hello World would break guides you have not finished. The default here is OpenClaw only: Telegram / WhatsApp, `openclaw-ui`, the Gateway, and optionally `~/.openclaw`. Do not switch the Control UI hostname to `None` on the way out to check something. Delete the app instead.

**Where you run this:** `openclaw` and `edgible` on the **Ubuntu guest**; Automations in **Control UI**; BotFather in the **Telegram app**; the final check in a **phone browser on cellular**.

## 9.1 The job

You disable the chat clients, delete the `openclaw-ui` app, stop the Gateway, and optionally wipe OpenClaw’s config. Cellular `openclaw-ui` should fail. `hello-world` (and n8n / ollama apps) still load if you left them.

**Done when**

- `edgible app list` has no `openclaw-ui`.
- `ss -ltnp | grep 18789` is empty; nothing listens on `18789`.
- Phone `openclaw-ui` URL does not chat (cert gone or connection fails).
- Telegram bot does not reply (disabled / token revoked). WhatsApp unlinked if you had it.
- n8n / `n8n-hooks` / `ollama` still listed if you had created them.
- `hello-world` still loads unless you chose 9.7.
- Port `18789` is not forwarded.

**Need first:** You finished enough of this series that OpenClaw exists (at least [chapter 1](01-openclaw-on-the-box.md)). Skip steps for things you never installed.

**Not this chapter:** deleting the Ubuntu VM, `edgible auth logout` (keeps the CLI off this box), or publishing anything new.

## 9.2 Stop jobs and chat clients (Ubuntu VM)

ACP sessions and site crons keep running until you stop them.

```bash
# Control UI or CLI: close Cursor ACP sessions if any
# openclaw /acp close   (from a chat that still works)
```

In Control UI → **Automations**, delete hourly Hello World / On this day jobs ([chapter 3](03-openclaw-changes-edgible-site.md) / [chapter 7](07-cursor-agent.md)).

Telegram ([chapter 5](05-telegram-pocket-client.md)), on the Gateway host:

```bash
openclaw config set channels.telegram.enabled false
openclaw config unset channels.telegram.botToken
openclaw gateway restart
```

In Telegram: **@BotFather** → your bot → **API Token** → **Revoke** if you will not use that bot again.

WhatsApp ([chapter 6](06-whatsapp-pocket-client.md)):

```bash
openclaw channels logout --channel whatsapp
openclaw gateway restart
```

## 9.3 Delete the Control UI app

Closes `https://openclaw-ui.<org>.edgible.com`. Gateway can still be up on loopback until 9.4.

```bash
edgible app list
edgible app delete --name openclaw-ui
edgible app list
```

**Smoke test.** You want `openclaw-ui` gone. `hello-world` (and n8n / ollama) still there.

Never `None` on `18789` on the way out. Delete the app; do not “make it public then remove it.”

## 9.4 Stop the Gateway

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

## 9.5 Optional: skill and config wipe

Remove the `edgible` skill ([chapter 4](04-edgible-openclaw-skill.md)):

```bash
openclaw skills list
openclaw skills uninstall edgible
```

If `uninstall` is missing, stop the Gateway first, then delete the `edgible` folder under `~/.openclaw` (skills / workspace). Do not delete the whole `~/.openclaw` unless you mean 9.6.

## 9.6 Optional: full OpenClaw wipe

This removes keys in `~/.openclaw/.env` (Gemini, DeepSeek, …) from this VM. Revoke those keys in the provider consoles if they leaked or you are done with them.

```bash
rm -rf ~/.openclaw
```

The `openclaw` binary may still be on PATH (installer / nvm). Remove it only if you will not reinstall: follow OpenClaw’s uninstall docs for this install, or delete the npm/nvm copy you used in [chapter 1](01-openclaw-on-the-box.md).

## 9.7 Optional: Hello World too

Only if you also want the shared public page gone. Skip this if n8n or LLM-on-Edgible still uses this VM.

```bash
edgible app delete --name hello-world
docker stop hello-world && docker rm hello-world
```

Leave `~/hello-world` on disk unless you want that HTML gone too. Do not `edgible agent uninstall` here. That serving agent is still what [n8n on Edgible](../n8n-on-edgible/README.md) (until [n8n teardown](../n8n-on-edgible/06-n8n-teardown.md)) and [LLM on Edgible](../llm-on-edgible/README.md) publish through.

### Verify

- [ ] `edgible app list` has no `openclaw-ui`.
- [ ] `ss -ltnp | grep 18789` is empty; nothing listens on `18789`.
- [ ] Phone `openclaw-ui` URL does not chat (cert gone or connection fails).
- [ ] Telegram bot does not reply (disabled / token revoked). WhatsApp unlinked if you had it.
- [ ] n8n / `n8n-hooks` / `ollama` still listed if you had created them.
- [ ] `hello-world` still loads unless you chose 9.7.
- [ ] Port `18789` is not forwarded.

---

## Next

Series index: [README](README.md). Workflows: [n8n on Edgible](../n8n-on-edgible/README.md). Published model: [LLM on Edgible](../llm-on-edgible/README.md).
