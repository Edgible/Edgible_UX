# Telegram as the OpenClaw pocket client

**OpenClaw is the agent on a box you own. Telegram is a chat door to that agent. Edgible is a different door: a public `https://` URL.** Do not publish Telegram (or WhatsApp, Discord, Ollama) through Edgible. Do not port-forward 18789.

By the end of this chapter you DM **a bot you created** and OpenClaw on the VM replies. The Gateway still dials **out** to `api.telegram.org` on TCP 443. Your personal Telegram login is you; the BotFather **token** is the bot’s password, stored only on the VM.

This is the usual pocket client for OpenClawers. **Control UI** (chapter 1) is still the cleaner place for `/skill` and exec approvals. **WhatsApp** (chapter 1, step 14) is the bindable ACP client (`/acp spawn --bind here`). Telegram is official Bot API; WhatsApp is a linked device (Baileys).

**Prerequisites:** [Getting started](01-invite-through-edgible-on-vm.md) through a running Gateway and a model (at least step 9). Control UI through Edgible is optional here. `edgible` on PATH is only needed if you will use the [openclaw-edgible](https://github.com/Edgible/openclaw-edgible) skill.

There is **no** `openclaw channels login telegram`. You paste a BotFather token into config.

---

## What you should have at the end

- A Telegram bot from [@BotFather](https://t.me/BotFather), and its token on the Gateway host (not in chat).
- `channels.telegram.enabled` true, `botToken` a literal `123:AAH…` string (not `$TELEGRAM_BOT_TOKEN`).
- `channels.telegram.apiRoot` **unset** (OpenClaw uses `https://api.telegram.org`).
- A DM to **your bot** (not BotFather) that gets an OpenClaw reply.
- Pairing approved if the Gateway asked.
- You can tell **Gateway `/whoami`** (instant sender id) from **`/skill edgible whoami`** (Edgible CLI, goes through the model).

---

## 1. Create the bot

On your phone or [web.telegram.org](https://web.telegram.org/), open **@BotFather** (Telegram’s official bot).

1. `/newbot` — pick a display name and a username ending in `bot`.
2. Copy the **HTTP API token** (`digits:AAH…`). Treat it like a password.
3. Later: `/mybots` → your bot → **API Token** if you lost it. **Revoke** if it leaked.

Logging into Telegram as yourself does **not** put this token anywhere. OpenClaw only sees it when you `config set` it on the VM.

DM **the bot you just created**. BotFather will not forward your `hello` to OpenClaw.

---

## 2. Store the token on the VM

SSH into the Ubuntu guest (the Gateway host). Do not paste the token into OpenClaw chat, WhatsApp, or this guide’s examples in a ticket.

```bash
openclaw config set channels.telegram.enabled true
openclaw config set channels.telegram.botToken 'PASTE_TOKEN_HERE'
```

**Do not set `apiRoot`.** If you run `openclaw config get channels.telegram.apiRoot` and see `Config path not found`, that is **correct**. The default is `https://api.telegram.org`. Setting `apiRoot` to the full `https://api.telegram.org/bot<TOKEN>` URL makes grammY double the `/bot…` path. Logs then show:

```text
telegram deleteMyCommands / setMyCommands failed: 404 Not Found
```

If you already set a bad `apiRoot`:

```bash
openclaw doctor --fix
openclaw config unset channels.telegram.apiRoot
```

`apiRoot` is only for a **self-hosted** Bot API server (file-size limits, blocked regions). Everyone else leaves it unset.

Check the token is real (do not paste the value into chat):

```bash
openclaw config get channels.telegram.botToken
```

Empty, missing, or `$TELEGRAM_BOT_TOKEN` means OpenClaw never got the secret. A `123:AAH…` shape is what you want.

```bash
openclaw gateway restart
openclaw channels status --probe
```

You want Telegram enabled, configured, a bot username, token from config.

---

## 3. Pairing and first `hello`

Default DM policy is **pairing**. Send `hello` to **your bot**. On the VM:

```bash
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

Send `hello` again. You want a reply from OpenClaw (Gemini, or Ollama if Gemini returned 429 — see step 5).

If there is no reply: token, `apiRoot`, pairing, or the Gateway not running. `openclaw doctor` and `channels status --probe` first. There is still no Edgible hop on this path.

### Verify

- [ ] You DMed **your** bot, not BotFather.
- [ ] `channels status --probe` shows Telegram working.
- [ ] `hello` gets a reply (identity ritual counts).
- [ ] You did not publish a Telegram port through Edgible.

---

## 4. Gateway commands vs the Edgible skill

Telegram slash commands that OpenClaw handles **in the Gateway** (no model) must be a **standalone** message:

| You send | What it is |
| --- | --- |
| `/whoami` or `/id` | **Your Telegram sender id** (`telegram:123…`). Instant. |
| `/status` | Runtime + **selected** model; **Fallback** line if this session answered on Ollama. |
| `/model status` | Endpoints / picker detail. |
| `/stop` | Abort a stuck agent turn. |
| `/skill edgible whoami` | **Edgible CLI** `edgible whoami`. Full agent turn (slow). |

If `/whoami` spins, a previous `/skill` turn is probably still queued (`/stop` then `/id` alone), or Telegram treated the slash as chat and the model loaded the Edgible skill because the description mentions `whoami`. A real `/whoami` is a short identity line in a second or two.

**Your numeric user id** is the number in `/whoami`. Use that for allowlists (`id:123456789`), not `@username`. If the command never comes back: [@userinfobot](https://t.me/userinfobot) `/start`, or `openclaw pairing list telegram`.

---

## 5. Which model, and 429s

Gemini free tier **429** is quota, not a broken Telegram install. If `agents.defaults.model.fallbacks` includes e.g. `ollama/gpt-oss:20b`, OpenClaw **fails over on that same turn** — you do not resend for fallback to start. The next message starts on Gemini again.

Failover does **not** run if you pinned a model in Control UI or `/model …` (strict). Leave the picker on **Default**.

In a **DM**, a switch can show:

```text
↪️ Model Fallback: ollama/gpt-oss:20b (selected google/…; rate_limit)
```

Groups suppress that notice; `/status` still has the state.

A 20B local model on an 8 GB VM is slow. That is why `/skill` feels the same in Control UI and Telegram: same Gateway, same model. `edgible whoami` on the VM is milliseconds.

```bash
openclaw config get agents.defaults.model
```

You want `primary` = Flash and `fallbacks` including `ollama/…` if you set that in chapter 1.

---

## 6. Logs do not echo your Telegram text

Default `openclaw logs --follow` is **info**. Inbound message bodies are not printed (privacy). A successful `/whoami` can be almost silent. Follow logs on the **VM**, not the Mac.

```bash
openclaw channels logs --channel telegram
openclaw channels status --probe
```

To see raw updates while debugging, raise file logs then put them back:

```bash
openclaw config set logging.level debug
openclaw gateway restart
openclaw logs --follow
```

Then:

```bash
openclaw config set logging.level info
openclaw gateway restart
```

If debug still shows nothing when you send a DM, the Gateway is not receiving Telegram (wrong host, another poller, stale update offset). `openclaw gateway status` and `ls ~/.openclaw/state/telegram/`.

---

## 7. Install the Edgible skill (optional)

The skill is **[Edgible/openclaw-edgible](https://github.com/Edgible/openclaw-edgible)**, not this UX repo. One skill named **`edgible`**.

```bash
openclaw skills install git:Edgible/openclaw-edgible --force
openclaw skills list
openclaw gateway restart
```

You want **edgible**. Then `/new`. Remove old folders `edgible-app-create` / `edgible-app-list` / `edgible-app-delete` if they are still under `~/.openclaw/workspace/skills/`.

`openclaw skills update --all` refreshes **ClawHub** installs only. Git installs need `install … --force` again.

Helpers live in the **skill** directory (`{baseDir}/scripts/delete.py`), not `~/.openclaw/workspace/scripts/`. If logs say `ENOENT` on `workspace/scripts/delete.py`, the model expanded `{baseDir}` wrong.

`/skill edgible whoami` and `/skill edgible doctor` are CLI pass-through (`edgible` + those args). English “list my apps” / “publish this port” / “take down that URL” use the Python helpers. Test `/skill` in **Control UI** first if Telegram is noisy.

Create helper flags: `--name`, `--port`, `--auth-modes` (`none` \| `org` \| `api-key`), optional `--device-name` / `--device-id`. Never `--auth-modes none` on port **18789**.

---

## 8. Optional: stop WhatsApp

Same OpenClaw agent; WhatsApp is a channel. Pause:

```bash
openclaw config set channels.whatsapp.enabled false
openclaw gateway restart
```

Unlink the phone session:

```bash
openclaw channels logout --channel whatsapp
```

Telegram is unchanged.

---

## 9. Optional: host bash (`!` / `/bash`)

Off by default. It is a **host shell from chat**, not the Edgible skill.

```bash
openclaw config set commands.bash true
openclaw config set tools.elevated.enabled true
openclaw config set tools.bash.enabled true
openclaw config set tools.elevated.allowFrom.webchat '["*"]' --strict-json
openclaw config set tools.elevated.allowFrom.telegram '["id:YOUR_TELEGRAM_USER_ID"]' --strict-json
openclaw gateway restart
```

Standalone message: `! edgible whoami` or `/bash edgible whoami`. Limit Telegram to **your** `id:`. Do not enable this in a group.

---

## Verify

- [ ] `hello` to **your bot** gets an OpenClaw reply.
- [ ] `/id` (standalone) returns `telegram:` + a number, quickly.
- [ ] `/status` shows the selected model (and Fallback if Ollama answered).
- [ ] `apiRoot` is unset. Token is a literal BotFather string.
- [ ] No Telegram port on Edgible. Gateway still loopback. openclaw-ui still **org** if you published it in chapter 1.
- [ ] (Optional) `openclaw skills list` shows **edgible**; `/skill edgible --version` in Control UI prints the CLI version in the **bubble**.

---

## Why this pattern

Telegram does not replace Edgible. Bookmarkable Control UI and Hello World still go through `https://<app>.<org>.edgible.com`. The bot is how you talk to the same Gateway from a phone without opening that URL. The token never belongs in Edgible, and the Edgible skill never logs into Telegram.
