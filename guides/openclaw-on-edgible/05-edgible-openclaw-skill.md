# 5. OpenClaw skill for the Edgible CLI

**Teach the agent to run the hosting, not just talk about it.**

## 5.0 Why

Ask OpenClaw to publish a port or list your apps right now and you will get a confident, invented command. It has a shell on the box, but nothing has told it that `edgible` exists, what its subcommands are, or that it is already logged into your organisation. It guesses, and a guess that runs is worse than a refusal.

Two obvious fixes are worse. Turning on host bash gives chat an unrestricted shell in order to reach one CLI, which is far more access than the job needs. Reading output on the guest and pasting it into chat yourself removes the point of asking from a phone. A skill is the narrow version: a described, named command surface the model can call, running as the user that is already authenticated, with the guide’s safety rules (never `None` on the Control UI port) in the skill repo rather than in your memory.

Prove it in the shell first, Control UI second. If Telegram’s `/skill` fails three chapters from now, you will already know the binary, the login and the model turn work, so the remaining suspect is the channel.

```
you, in chat           Control UI (org door)  ·  Telegram DM  ·  WhatsApp
                                 │
Ubuntu guest           OpenClaw Gateway ──► edgible skill ──► edgible CLI (your org)
                                 │
                       the same box that serves your Edgible apps
```

**Where you run this:** the install and the shell check on the **Ubuntu guest**; the chat check in **Control UI**: local dashboard on a guest desktop, or the phone on cellular from [chapter 3](03-publish-openclaw-control-ui.md).

## 5.1 The job

You install the `edgible` skill from [openclaw-edgible](https://github.com/Edgible/openclaw-edgible) (not this UX repo). `/skill edgible <args>` means run `edgible <args>` on the Gateway host. Prove it twice: shell first (CLI is healthy), then Control UI (the model pastes stdout into the bubble). Shell-first means a later Telegram `/skill` failure is the channel or the model, not a missing binary.

The skill does not sign you up, create an org, or register a device. Telegram and WhatsApp are chat clients; they are not this skill.

**Done when**

- `openclaw skills list` shows `edgible` (not the old three `edgible-app-*` skills).
- VM: `edgible whoami` prints org/account.
- Control UI: `/skill edgible whoami` repeats that in the bubble (not only a tool card).
- Control UI: `/whoami` is OpenClaw identity, not the Edgible block.
- `/skill edgible doctor` is a doctor report, not an app list.

**Need first:** [2. OpenClaw on the VM (loopback Gateway)](02-openclaw-on-the-box.md) (Gateway running, `edgible auth login`). Control UI (local `openclaw dashboard` or [3. OpenClaw Control UI through Edgible](03-publish-openclaw-control-ui.md)) for the chat test.

**Not this chapter:** Edgible signup, publishing apps (that is English helpers after the smoke test), or Telegram `/skill` (prove Control UI first).

## 5.2 Install

On the Gateway host (the Ubuntu VM):

```bash
openclaw skills install git:Edgible/openclaw-edgible
openclaw skills list
openclaw gateway restart
```

You want a row named `edgible`. Then in Control UI send `/new` so the session loads the skill.

`--force` if you are refreshing a git install (`openclaw skills update --all` only updates ClawHub, not git):

```bash
openclaw skills install git:Edgible/openclaw-edgible --force
openclaw gateway restart
```

If you previously copied `edgible-app-create` / `edgible-app-list` / `edgible-app-delete` into `~/.openclaw/workspace/skills/`, remove those folders so OpenClaw is not choosing among four skills.

Copy-install (folder name must be `edgible`) is in the [skill README](https://github.com/Edgible/openclaw-edgible#install). Prefer `git:` so you can `--force` later.

The helpers live next to `SKILL.md` (`…/skills/edgible/scripts/`), not `~/.openclaw/workspace/scripts/`.

---

## 5.3 Shell: CLI is healthy

Same VM, before chat. This does not use the skill; it proves `edgible` on PATH is logged in.

```bash
which edgible
edgible --version
edgible whoami
```

You want a version, then a block with Profile, Environment, Account, Organization. If `whoami` fails, fix CLI login (`edgible auth login`). `/skill` cannot succeed until this does.

Optional: `edgible doctor` (diagnostics). That is a real top-level command, not app list.

Not this test: `openclaw` has no `edgible whoami`. OpenClaw’s `/whoami` in chat is a different command ([5.4](#54-control-ui-skill-pass-through)).

---

## 5.4 Control UI: skill pass-through

**Smoke test.** Open Control UI ([3. OpenClaw Control UI through Edgible](03-publish-openclaw-control-ui.md) or local dashboard). New session (`/new`). Leave the model picker on **Default**. Send exactly:

```text
/skill edgible whoami
```

Success: the bubble contains the same Profile / Environment / Account / Organization you saw in the shell. The model must `exec` `edgible whoami` and paste stdout. A tool card with no bubble text is not enough.

Also useful:

```text
/skill edgible --version
/skill edgible doctor
```

`doctor` must run `edgible doctor`, not app list. If the reply invents an app named `dcotr` / `whoami`, the skill copy is stale. Run a `--force` install, restart, then `/new`.

### Do not confuse these

| Where | Command | What you get |
| --- | --- | --- |
| VM shell | `edgible whoami` | Edgible session (org, account, environment) |
| Control UI | `/skill edgible whoami` | Same CLI, via the skill (OpenClaw model turn) |
| Control UI or Telegram | `/whoami` or `/id` | OpenClaw sender id (`webchat:…` / `telegram:123…`). Instant. Not Edgible. |

`/skill` is a full model turn. It can be slow on Gemini free tier (429). The CLI itself is milliseconds. If chat hangs, `/stop`, then retry in Control UI, not Telegram, for the first skill check. A paid or local primary is [9. Models beyond free Gemini](09-models-beyond-free-gemini.md).

Exec may wait for approval (`approve-reads`). Approve `edgible whoami`.

### Verify

- [ ] `openclaw skills list` shows `edgible` (not the old three `edgible-app-*` skills).
- [ ] VM: `edgible whoami` prints org/account.
- [ ] Control UI: `/skill edgible whoami` repeats that in the bubble (not only a tool card).
- [ ] Control UI: `/whoami` is OpenClaw identity, not the Edgible block.
- [ ] `/skill edgible doctor` is a doctor report, not an app list.

---

## 5.5 After it works

English “list my apps on this machine” / “publish this port” / “take that URL down” use the Python helpers. CLI-shaped text stays pass-through (`/skill edgible device list --type serving`). Create flags and safety (never `none` on port `18789`) are in the [skill repo](https://github.com/Edgible/openclaw-edgible).

Telegram: same `/skill edgible whoami` in [chapter 6](06-telegram-pocket-client.md) after pairing. Prove it in Control UI first.

---

## Next

[6. Telegram pocket client for OpenClaw](06-telegram-pocket-client.md). Other models: [9. Models beyond free Gemini](09-models-beyond-free-gemini.md). Series: [README](README.md).
