# 7. WhatsApp linked device for OpenClaw

**WhatsApp as a linked device — and the client that can bind Cursor.**

## 7.1 The job

You link the Gateway as another WhatsApp device (same idea as WhatsApp Web). Incoming DMs hit OpenClaw on the VM. Gemini stays the dispatcher until you **bind** Cursor; then this thread *is* the Cursor session until `/acp close`. Control UI cannot `--bind here`. Skip if you have no WhatsApp — [6. Telegram pocket client for OpenClaw](06-telegram-pocket-client.md) is everyday pocket chat without linking a device.

A dedicated second number is cleaner. **Self-chat** on your personal number works (`allowFrom` includes you, `selfChatMode` on). WhatsApp has **no bot badge** — set `messages.responsePrefix` so replies start with `[OpenClaw]`.

**Done when**

- `openclaw channels status --probe` shows WhatsApp linked.
- WhatsApp `hello` gets a reply that starts with **`[OpenClaw]`**.
- Optional: `/acp spawn cursor --bind here …` succeeds (no webchat bind error); public On this day retitles without `/acp steer`.

**Need first:** [2. OpenClaw on the VM (loopback Gateway)](02-openclaw-on-the-box.md). For ACP bind, [8. Cursor Agent from OpenClaw on the Edgible site](08-cursor-agent.md) through doctor. For the retitle demo, the designed page from [4](04-openclaw-changes-edgible-site.md) or [8](08-cursor-agent.md).

**Not this chapter:** publishing WhatsApp through Edgible, port-forwarding, or **None** on openclaw-ui.

## 7.2 Plugin + QR login

On the **VM desktop** terminal (you must **see** the QR; it expires in about a minute). Gateway running:

```bash
openclaw plugins install clawhub:@openclaw/whatsapp
openclaw gateway restart
openclaw channels login --channel whatsapp
```

If install already happened, `channels login` is enough. Phone: **WhatsApp → Settings → Linked devices → Link a device** → scan the terminal QR. You want a linked session, not “can’t link new devices” (remove a stale Web session, or wait if WhatsApp is throttling).

```bash
openclaw channels status --probe
```

WhatsApp should show connected / linked.

Do **not** paste session creds into chat or Hello World.

## 7.3 Who may DM

Default is **pairing** (unknown senders wait). Put **your** E.164 in `allowFrom` (example shape only — use your number):

```bash
openclaw config set channels.whatsapp.dmPolicy pairing
openclaw config set channels.whatsapp.allowFrom '["+61XXXXXXXXX"]' --strict-json
openclaw config set channels.whatsapp.selfChatMode true
openclaw config set channels.whatsapp.groupPolicy allowlist
openclaw config set messages.responsePrefix "[OpenClaw] "
openclaw gateway restart
```

## 7.4 First WhatsApp `hello`

From the phone, message **yourself** (or a second phone messaging the linked account). If OpenClaw asks to pair:

```bash
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <CODE>
```

That is the same *idea* as `devices approve` for the Control UI — it is **not** the WhatsApp QR. Send `hello`. You want a reply in WhatsApp that **starts with `[OpenClaw]`** (Gemini/gpt-oss behind it). Edgible is unused for this hop.

A bare “Hey Stefano! How can I help you today?” is still the Gateway — it just has no product label. WhatsApp shows it as **your** linked session. Self-chat is *supposed* to default to `[openclaw]` / `[{identity.name}]` when `responsePrefix` is unset; that does not always fire. The explicit prefix from 7.3 is the check.

## 7.5 Bind Cursor — retitle sections (no steer)

If you set `permissionMode` back to `approve-reads` in [chapter 8](08-cursor-agent.md), headless Cursor cannot write HTML. For this pass:

```bash
openclaw config set plugins.entries.acpx.config.permissionMode approve-all
openclaw gateway restart
```

In the **same** WhatsApp chat (not Control UI):

```text
/acp spawn cursor --bind here --thread off --cwd /home/YOURUSER/hello-world
```

You want a spawn **without** `Conversation bindings are unavailable for webchat`. Then a **normal** message — not `/acp steer`:

```text
Rename the three section headings to: Who this is. Why we remember them. One odd fact.
Keep the body copy, CSS, and the Australia/Adelaide next-rotation footer.
Update the Python updater so the next hourly run uses those headings too.
Do not docker exec. Do not touch ~/.openclaw or Edgible.
```

Wait for Cursor to finish in WhatsApp. `/acp close` when done. Then set `permissionMode` back to `approve-reads` ([chapter 8](08-cursor-agent.md)).

Leave WhatsApp, hard-refresh `https://hello-world.YOUR-ORG.edgible.com` (cellular). You want the **new titles**, same person, same footer.

### Verify

- [ ] `openclaw channels status --probe` shows WhatsApp linked.
- [ ] WhatsApp `hello` gets a reply that starts with **`[OpenClaw]`** (pairing approved if asked).
- [ ] `/acp spawn cursor --bind here …` succeeds in WhatsApp (no webchat bind error).
- [ ] Public On this day page shows **Who this is / Why we remember them / One odd fact** after a hard-refresh.
- [ ] You did not use `/acp steer` for this change.
- [ ] `permissionMode` is **approve-reads** again. openclaw-ui is still **org**. Port **18789** is still not forwarded.

---

## Next

[8. Cursor Agent from OpenClaw on the Edgible site](08-cursor-agent.md) if you have not done ACP yet. Series: [README](README.md).

