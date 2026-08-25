# 8. Cursor Agent from OpenClaw on the Edgible site

**Cursor engineers the site Gemini only dumped. Same URL. Night and day.**

## 8.1 The job

[4. OpenClaw changes the public Edgible site](04-openclaw-changes-edgible-site.md) proved OpenClaw can change a public URL. The HTML is a dump. Here you put the **starting** Hello World page back, hire Cursor over ACP to build On this day (layout, CSS, updater, state, cron installer), and hard-refresh the **same** hostname. Gemini stays the OpenClaw chat brain. You do **not** paste a Cursor key into `openclaw models set`. `approve-all` plus this spawn writes the **public** site.

Skip without a Cursor subscription. Finish chapter 4 first so the A/B is honest — this chapter **wipes** Gemini’s page on purpose.

**Done when**

- `/acp doctor` in Control UI is healthy.
- Cellular hard-refresh of **hello-world** is a designed On this day page (not a Gemini dump).
- Cursor documented (or installed) **on-this-day-rotate** as an OpenClaw **command** cron.
- `permissionMode` is **approve-reads** again. openclaw-ui stays **org**.

**Need first:** [4. OpenClaw changes the public Edgible site](04-openclaw-changes-edgible-site.md), [3. OpenClaw Control UI through Edgible](03-publish-openclaw-control-ui.md) (`openclaw-ui` **org**), nginx bind-mount from [1.9](01-edgible-on-vm.md). Control UI **cannot bind** — spawn then **steer**. WhatsApp ([7](07-whatsapp-pocket-client.md)) can `--bind here`.

**Not this chapter:** Cursor.app on the Mac; making Cursor the default chat model; another ACP spawn for the hourly tick (`python3` cron after install).

## 8.2 Words you'll use

The job runs on the **Gateway host** (this Ubuntu VM). One-off ACP jobs on `~/hello-world` — write on the **host**, not `docker exec`. The hourly tick after install is `python3` via OpenClaw **command** cron, not another ACP spawn.

**ACP** (Agent Client Protocol) is a small language two programs speak over stdin/stdout: start a session, send a prompt, stream tool calls, finish. OpenClaw is the client. Cursor CLI (`agent acp`) is the server.

**acpx** is OpenClaw’s plugin that owns that client. Until it is installed, **enabled**, and the Gateway **restarted**, `/acp doctor` reports `ACP_BACKEND_MISSING`. On 2026.7 the runtime is **embedded in the plugin**.

| Word | What it is here |
| --- | --- |
| **Harness** | Cursor CLI running as that ACP server. |
| **Session** | One hired job. Key looks like `agent:cursor:acp:<uuid>`. |
| **`/acp doctor`** | Is acpx loaded and can it start `agent acp`? |
| **`/acp spawn`** | Start a session and point it at a directory (`--cwd`). On Control UI this does **not** send the coding task. |
| **`/acp steer`** | Send the actual prompt to that session key. |
| **`/acp close`** | End that Cursor job from OpenClaw’s side (stop the harness process, drop the session key). Does not close the Control UI, uninstall acpx, or log out `agent`. |
| **Bind** | Pin *this chat* so follow-ups go to Cursor. Control UI is **webchat** and **cannot bind** — that is why **this** step uses `/acp spawn` then `/acp steer` with a uuid. [WhatsApp](07-whatsapp-pocket-client.md) can `/acp spawn cursor --bind here --cwd …`; after that you type a normal message, no steer. **Telegram** is [6. Telegram pocket client for OpenClaw](06-telegram-pocket-client.md) (Bot API, not ACP bind). |
| **Oneshot** | Do the task and finish. |
| **`approve-all`** | Headless writes. Applies to **all** ACP jobs on this Gateway until `approve-reads`. |

Once, in order: **reset + inspect Hello World** → CLI + acpx → doctor → spawn → steer the **full** product (site + rotation tools) → run Cursor’s installer → `/acp close` → tighten permissions.

## 8.3 Clean slate (Hello World, no rotation cron)

The A/B only works if you can **see** the starting page. Restore [1.9](01-edgible-on-vm.md)’s HTML, delete extra files from chapter 4, remove Gemini rotation jobs. nginx stays up; you are not recreating the Edgible app.

On the VM:

```bash
openclaw cron list
```

Remove (or disable) every job that rewrites hello-world / On this day. In Control UI → Automations you can delete them too. Then:

```bash
cd "$HOME/hello-world"
# keep .git if you want history; drop the Gemini/Cursor leftovers
find . -mindepth 1 -maxdepth 1 ! -name '.git' ! -name 'index.html' -exec rm -rf {} +
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Hello World</title></head>
<body>
  <h1>Hello World</h1>
  <p>Served from your Ubuntu VM through Edgible.</p>
</body>
</html>
EOF
ls -la
curl -sS http://127.0.0.1:8081/
```

`ls` should be `index.html` (and maybe `.git`). curl should be **Hello World**, not a biography. On the **phone** (cellular), hard-refresh `https://hello-world.YOUR-ORG.edgible.com`. Same starting page as 1.9. That is the before shot.

## 8.4 Cursor CLI on the VM

On the **VM** (guest terminal, same user as the Gateway):

```bash
curl https://cursor.com/install -fsS | bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
agent --version
```

You want a version string. The binary is **`agent`**. Some docs say `cursor-agent`; if `which cursor-agent` is empty, that is fine.

Sign in with the **VM desktop browser** (same Cursor account as the Mac is fine):

```bash
agent login
agent status
```

You want a logged-in account, not a prompt to log in. systemd will not see a GUI keychain the way macOS does; Ubuntu file auth from `agent login` as this user is enough.

Do **not** publish Cursor through Edgible. Do **not** put a Cursor API key in Hello World.

echo "$HOME/hello-world" — that path is `--cwd` later. Do **not** spawn against `~/.openclaw`.

## 8.5 Install the ACP runtime (acpx plugin)

`ACP_BACKEND_MISSING` / `ACP runtime backend is not configured` means the **Gateway process** has no acpx backend yet. `/acp doctor` in chat cannot fix that — install on the VM, **restart**, then doctor again. Do not `/acp spawn` until doctor is healthy.

On this OpenClaw (**2026.7.x**) the doctor’s own next step is the bare plugin id. On the VM:

```bash
openclaw plugins install acpx
openclaw config set plugins.entries.acpx.enabled true
openclaw config set acp.enabled true
openclaw config set acp.backend acpx
openclaw gateway restart
openclaw plugins list
```

You want `acpx` **enabled** and **loaded** (not only “installed”). If `install acpx` fails or list stays empty:

```bash
openclaw plugins install @openclaw/acpx
openclaw config set plugins.entries.acpx.enabled true
openclaw gateway restart
openclaw plugins list
```

Still missing: `openclaw plugins install clawhub:@openclaw/acpx`, then restart and list again.

If `openclaw config get plugins.allow` prints a JSON list, **`acpx` must be in it**. `plugins install` usually appends it; if not, add `acpx` to that list (keep the other ids) and restart.

`/acp install` in Control UI prints the same enable steps. `acpx --help` is a 2026.7 hint for a **standalone** CLI. Newer acpx is **embedded in the plugin** — if `acpx --help` is “command not found” but `plugins list` shows loaded, ignore the binary and continue. Do not `npm i -g acpx` unless doctor still says backend missing after a loaded plugin + restart.

Then the Cursor harness + a narrow allowlist:

```bash
openclaw config set acp.defaultAgent cursor
openclaw config set acp.allowedAgents '["cursor"]' --strict-json
openclaw config set plugins.entries.acpx.config.probeAgent cursor
```

The Gateway daemon often **does not** have `~/.local/bin` on `PATH`. Point ACP at the real binary (your `$HOME`):

```bash
openclaw config set plugins.entries.acpx.config.agents.cursor.command "$HOME/.local/bin/agent"
openclaw config set plugins.entries.acpx.config.agents.cursor.args '["acp"]' --strict-json
```

If `which cursor-agent` printed a path instead, use that path and args `["acp"]`.

Headless ACP cannot click “allow write.” For **this demo only**:

```bash
openclaw config set plugins.entries.acpx.config.permissionMode approve-all
openclaw gateway restart
```

`approve-all` is for ACP sessions on this Gateway, not only hello-world. Put **org** back on openclaw-ui if you flipped it. After 8.7, set `permissionMode` back to `approve-reads`.

Open a **new** Control UI chat (an old tab can still think ACP is missing). Then `/acp doctor`.

## 8.6 Doctor, then spawn from the phone

On the VM, Gateway running. In Control UI chat (local dashboard **or** phone on cellular — same as [chapter 3](03-publish-openclaw-control-ui.md)):

```text
/acp doctor
```

Healthy looks like: `configuredBackend: acpx`, `registeredBackend: acpx`, `runtimeDoctor: ok (embedded ACP runtime ready)`, `agent=cursor`, `command=/home/YOURUSER/.local/bin/agent acp`, `healthy: yes`. Doctor’s `cwd` is often `~/.openclaw/workspace` — that is the **probe**, not the site. Spawn still needs `--cwd` from 8.3.

`ACP_BACKEND_MISSING` is the failure. Zero sessions / zero turns is normal before the first spawn.

Then spawn (unbound — Control UI cannot `--bind here`; see Approach). Use **your** path from 8.3:

```text
/acp spawn cursor --mode oneshot --thread off --cwd /home/YOURUSER/hello-world --label hello-world
```

Success looks like: `Spawned ACP session agent:cursor:acp:<uuid> (oneshot, backend acpx). Session is unbound…` Ignore the hint to `--bind here` on webchat. Copy that **full session key** for steer (do not type the next prompt as a normal chat line — this conversation is still Gemini, not Cursor):

```text
/acp steer --session agent:cursor:acp:YOUR-UUID This folder is the original Hello World page (1.9). Build a phone-friendly On this day mini-site. One notable person born on this calendar date (Wikipedia births). Page structure, every time:
- Name, birth–death years, and a one-line label (what they are known as)
- Who they were
- Why they still matter
- A quirky detail
- Footer at the end: next rotation time in **Europe/London** (IANA zone — readers may substitute their own), human-readable (include the offset or BST/GMT). Compute from “hourly from this run,” e.g. this update + 1 hour, in that zone — not UTC and not the browser’s local zone.
Readable typography and a simple layout (CSS file is fine). Those three sections must be real headings, not a single blob. Public sources only. Nothing about me. Do not docker exec (nginx mount is read-only). Do not touch ~/.openclaw, Edgible config, or openclaw-ui.
```

`--session hello-world` only works if the label stuck; the uuid key always works. `/acp sessions` if you lost it. `/acp status` if it goes quiet. First Cursor run can be slow (login + model). Completions still announce back into this Control UI as a parent task.

Success looks like: `ACP steer sent to…` then a Cursor summary of HTML/CSS/state/script. That write-up is the **harness**, not Gemini describing a change it did not make.

Leave Control UI. On the **phone** (cellular), hard-refresh `https://hello-world.YOUR-ORG.edgible.com`. You want a designed page with **Who they were / Why they still matter / A quirky detail**, and a footer **Next rotation** in Europe/London time — not a single Gemini dump, not “Hello World”, not “OpenClaw was here.”

```bash
cd ~/hello-world
git diff --stat
ls -la
```

You want CSS plus (after 8.6) an updater and a way to register hourly **command** cron. Rotation infra is a **second Cursor coding pass**, not a timer that launches Cursor.

When you are done with the visual pass (or after 8.6):

```text
/acp close
```

Natural language can work **after** doctor is green. Prefer `/acp spawn` + `/acp steer` for this first run.

## 8.7 Rotation infra (Cursor implements it)

**Outcome:** Cursor Agent adds the **tools** for hourly rotation in `~/hello-world`: updater script, already-shown state, midnight rollover, and an installer (or a printed `openclaw cron create …`) that registers a **command** job. You run that installer **once**. After that, the hour belongs to OpenClaw’s scheduler executing Python.

Spawn like 8.5 (`--cwd` `~/hello-world`). Steer:

```text
/acp steer --session agent:cursor:acp:YOUR-UUID Keep the current visual design. Implement hourly rotation infrastructure in this folder:
1. A Python 3 updater that fetches Wikipedia births for today's month-day, picks one notable person not already shown today, rewrites index.html using the existing CSS and the same sections every time (name + dates, Who they were, Why they still matter, A quirky detail, footer with next rotation in Europe/London), updates a state file, and starts a new list after local midnight. Print the chosen name to stdout. Next rotation = this run + 1 hour, formatted in IANA Europe/London (not UTC).
2. A small install script (or README with the exact command) that registers an OpenClaw command cron: every 1h, python3 the updater, cwd this folder. Name the job on-this-day-rotate. Use --command (shell), not an OpenClaw chat prompt and not ACP/Cursor.
3. Tell me the exact commands to run once on the VM.
Do not docker exec. Do not edit ~/.openclaw by hand. Do not schedule Cursor or /acp spawn. Public sources only. Nothing about me.
```

`/acp close` when the summary lists files + the install command. On the VM, run **what Cursor specified** (example only — prefer their output):

```bash
ls -la ~/hello-world
cd ~/hello-world
python3 update.py
```

Hard-refresh the public URL: **different name, same look**. Then run their installer, or if they only printed cron:

```bash
openclaw cron list
openclaw cron create "every 1h" \
  --name "on-this-day-rotate" \
  --command "python3 update.py" \
  --command-cwd "$HOME/hello-world"
```

**Run now** in Automations. Disable the [chapter 4](04-openclaw-changes-edgible-site.md) Gemini job that rewrites HTML in chat — it will overwrite this CSS.

## 8.8 Tighten permissions

```bash
openclaw config set plugins.entries.acpx.config.permissionMode approve-reads
openclaw gateway restart
```

Leave ACP **installed** if you will use it again; `allowedAgents: ["cursor"]` stays a narrow door. Do not set `gateway.auth` to none. Do not spawn against `~/.openclaw`.

### Verify

- [ ] `agent status` on the VM shows a logged-in Cursor account.
- [ ] `/acp doctor` in Control UI is healthy.
- [ ] Phone on **cellular**, hard-refresh **hello-world**: designed On this day page with **Who they were**, **Why they still matter**, and **A quirky detail**; footer shows **next rotation** in Europe/London time; still a person born on this date; still no personal data.
- [ ] `~/hello-world` contains updater + state, and Cursor documented (or installed) **on-this-day-rotate** as an OpenClaw **command** cron. The chapter 4 Gemini HTML job is disabled or gone.
- [ ] A second run (next hour or Run now) shows a **different** person, not a repeat.
- [ ] `permissionMode` is **approve-reads** again (or you accept the wider ACP blast radius and said so).
- [ ] openclaw-ui protection is still **org**. Port **18789** is still not forwarded.

## Next

That's the series. [Index](README.md). WhatsApp as the bindable client is [7. WhatsApp linked device for OpenClaw](07-whatsapp-pocket-client.md). Telegram is [6. Telegram pocket client for OpenClaw](06-telegram-pocket-client.md). The **edgible** skill is [5. OpenClaw skill for the Edgible CLI](05-edgible-openclaw-skill.md).

