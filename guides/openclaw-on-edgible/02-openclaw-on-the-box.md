# 2. OpenClaw on the VM (loopback Gateway)

**OpenClaw on *your* VM that can say hello — still not on the internet.**

## 2.1 The job

You install OpenClaw on the same Ubuntu guest as Hello World. The Gateway stays on **loopback** (`127.0.0.1:18789`). Pin Gemini **Flash** on the free AI Studio key (not Pro/preview — that is the 429). Optional: Ollama on a RAM-heavy Mac as failover.

**Done when**

- Gateway running on the VM, bind **loopback**, port **18789**.
- A **Flash** default if you used Gemini free tier.
- `openclaw agent --agent main --thinking off --message "Say hello in one sentence."` replies in the VM terminal.
- Optional: `openclaw dashboard` opens **local** Control UI and chat works (guest desktop only).
- Hello World on the phone still loads.

**Need first:** [1. Edgible on an Ubuntu VM](01-edgible-on-vm.md) (Hello World still up).

**Not this chapter:** publishing Control UI ([3](03-publish-openclaw-control-ui.md)), the Edgible skill ([5](05-edgible-openclaw-skill.md)), or `! edgible whoami` (host bash — off by default; [6.10](06-telegram-pocket-client.md#610-optional-host-bash--bash) if you want it later).

## 2.2 Choose a model

**Outcome:** A model OpenClaw can call — a Gemini API key (default), local Ollama if the box is big enough, or a private model URL from someone you trust.

OpenClaw onboarding will not finish until a **real completion** succeeds. **ChatGPT Free** (chatgpt.com) is not that: it is a website, not an API key. Same Google/OpenAI *login* can open a developer console; usage is a separate product.

Leave **hello-world** running. Pick **one** of the options below. You will paste the key (or point at Ollama) in the next step, when OpenClaw is installed.

### 2.2.1 Google Gemini (default, free)

Do this on the **host** browser, not inside the VM. You need a Google account (Gmail is fine).

1. Open [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey) and sign in.
2. If Google shows terms for AI Studio / the Gemini API, accept them.
3. Click **Create API key**.
4. Choose **Create API key in a new project** unless you already know which Google Cloud project to use.
5. Copy the key (it usually starts with `AIza`). Store it like a password — you will type it on the VM in the next step. Do not commit it, paste it into a chat, or put it in Hello World.

The free tier is enough to prove `hello`. It is rate-limited. Outside the EU, Google may use free-tier traffic to improve products; that is Google’s policy, not Edgible’s.

Optional check from the **VM** (proves the key *and* that the guest can reach Google). Paste is hidden:

```bash
read -s GEMINI_API_KEY
export GEMINI_API_KEY
curl -sS "https://generativelanguage.googleapis.com/v1beta/models?key=${GEMINI_API_KEY}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['models'][0]['name'])"
```

You want a model name such as `models/gemini-2.5-flash`, not `API_KEY_INVALID` or a hang. (If you piped the full JSON to `head` instead, `curl: (23) Failure writing output to destination` after that JSON is still success — `head` closed the pipe early.) If the request itself fails on the VM, fix outbound HTTPS before installing OpenClaw.

### 2.2.2 Local Ollama (same machine, enough RAM)

Use this if you want prompts to stay on the mini-PC. OpenClaw will call Ollama at `http://127.0.0.1:11434`. **Do not** publish Ollama through Edgible when it is on the same box.

| RAM on the VM / mini-PC | What to expect |
| ----------------------- | -------------- |
| **4 GB** (this guide’s VM default) | Too small. Use Gemini (2.2.1) or give the guest more RAM. |
| **8 GB** | Floor. Pull a **tiny** model only (about 1B parameters). |
| **16 GB+** | Usable local chat. |

If you have the RAM:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:1b
ollama run llama3.2:1b "Say hello in one word"
```

**Ollama on the Mac, OpenClaw in the VM (32 GB Mac):** Do **not** put the model in the 8 GB guest. Install [Ollama for Mac](https://ollama.com/download). After the VM’s 8 GB, you have on the order of **16 GB** left for a model once macOS and the browser have a share — enough for OpenClaw, tight for a 27B if Chrome is fat.

On the **Mac**:

```bash
ollama pull gpt-oss:20b
# or, if `ollama run` stays snappy with the VM up: ollama pull qwen3.5:27b
ollama run gpt-oss:20b "Say hello in one word"
```

`gpt-oss:20b` is the safer fit next to an 8 GB VM. Try **Qwen 27B** only if Activity Monitor still has headroom (no swap storm).

Ollama defaults to **Mac localhost only**. The VM’s `127.0.0.1` is the *guest*, so OpenClaw will not see it. Listen on all interfaces on the Mac (home LAN only — do not port-forward **11434** on the router):

```bash
launchctl setenv OLLAMA_HOST "0.0.0.0:11434"
killall Ollama; open -a Ollama
```

On the **VM**, the host is the default gateway (UTM NAT is often `192.168.64.1`; VirtualBox NAT is often `10.0.2.2`):

```bash
HOST=$(ip route | awk '/default/ {print $3; exit}')
curl -sS "http://${HOST}:11434/api/tags"
```

You want JSON with your model name, not connection refused. UTM NAT is often `192.168.64.1` if `$HOST` is wrong. Do **not** test `127.0.0.1` **on the VM** — that is the guest, not the Mac.

Ollama is the **runtime** on the Mac. Qwen / gpt-oss is the **model** you pulled. There is no Google-style API key; OpenClaw still wants a dummy `apiKey` (`ollama-local`).

Do **not** publish Ollama through Edgible on **None**. The VM talking to the Mac on the virtual LAN is enough. After OpenClaw is installed, point it at this host in [2.3.7](#237-point-openclaw-at-ollama-on-the-mac-optional).

### 2.2.3 Another cloud provider

Any key OpenClaw onboarding accepts is fine: **OpenAI Platform** (`sk-…` at [platform.openai.com/api-keys](https://platform.openai.com/api-keys), billed separately from ChatGPT), **Groq**, **OpenRouter** (`:free` models, tight daily caps). Set a spend cap if the provider bills.

### 2.2.4 A private model via Edgible (someone you trust)

Someone else (or your other site) runs a model on **their** hardware — Ollama, vLLM, a fine-tune — and publishes that API through Edgible. You point OpenClaw at their `https://<app>.<org>.edgible.com` URL instead of Gemini.

This is a real Edgible job. It is **not** this trial’s path if you already have Gemini (2.2.1).

You need from the operator:

- The **HTTPS URL** of the model API (OpenAI-compatible or Ollama-style).
- A **machine credential** OpenClaw can send on every request (Edgible **API key** protection, or the model’s own key). Browser-only login will not work — OpenClaw is not a browser.
- Confirmation the endpoint is **not** `None` (public). A raw model API on the internet is a gift to strangers.

Trust: they can see your prompts. Treat it like handing them a diary, not like Google’s privacy policy.

When you install OpenClaw, that URL is a **custom / OpenAI-compatible provider**, not “Google” in the wizard. Exact flags wait until the install step.

### 2.2.5 Verify

- [ ] If you used Mac Ollama: `curl` from the **VM** to `http://$HOST:11434/api/tags` returns JSON (not `127.0.0.1` on the guest).
- [ ] You did **not** use ChatGPT Free as the model.
- [ ] The key or private URL was not pasted into Slack, git, or the Hello World page.

---

## 2.3 Install OpenClaw locally

**Outcome:** OpenClaw Gateway running on the VM; you can send `hello` from the guest terminal and get a reply. It is not on the internet yet.

Still **inside the VM**. Leave **hello-world** and the Edgible serving agent running. Do **not** install OpenClaw on the Mac/PC host for this guide.

This VM is Ubuntu **Server** — there is no desktop browser. Local proof is the CLI, not `openclaw dashboard`.

### 2.3.1 Install the OpenClaw CLI

OpenClaw needs **Node.js 22.22.3+** (the installer can provision it). That is newer than Edgible’s Node 20 floor; let this installer handle it.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

`--no-onboard` skips the long interactive wizard (Telegram and friends). We will onboard with Gemini in the next substep.

Reload PATH if `openclaw` is not found (new shell, or `source ~/.bashrc`):

```bash
openclaw --version
```

Official reference: [Install](https://docs.openclaw.ai/install).

### 2.3.2 Onboard with your model (Gemini default)

If `GEMINI_API_KEY` is empty in this shell, paste it again (hidden):

```bash
read -s GEMINI_API_KEY
export GEMINI_API_KEY
```

Then:

```bash
openclaw onboard --non-interactive --accept-risk \
  --mode local \
  --auth-choice gemini-api-key \
  --gemini-api-key "$GEMINI_API_KEY" \
  --gateway-bind loopback \
  --install-daemon \
  --skip-skills
```

`--accept-risk` is OpenClaw’s required flag for unattended setup (OpenClaw can use tools and a shell). It is not an Edgible setting.

`--gateway-bind loopback` keeps the Control UI on `127.0.0.1:18789` only. Do **not** bind `0.0.0.0` and do **not** port-forward 18789 on the router.

`--skip-skills` keeps this first `hello` about the Gateway + Gemini, not extra downloads. The Edgible CLI skill is [chapter 5](05-edgible-openclaw-skill.md). Telegram is [chapter 6](06-telegram-pocket-client.md).

If you used **2.2.2 / 2.2.3 / 2.2.4** instead of Gemini, swap only the auth flags:

| 2.2 choice | Onboard auth |
| ------------- | ------------ |
| 2.2.1 Gemini | as above |
| 2.2.2 Ollama **in the guest** | `--auth-choice ollama --custom-model-id llama3.2:1b` (tiny; only if the VM has enough RAM) |
| 2.2.2 Ollama **on the Mac** | `--auth-choice ollama --custom-base-url "http://$HOST:11434" --custom-model-id gpt-oss:20b` (no `/v1`; `$HOST` from 2.2.2). Or onboard Gemini first, then **2.3.7**. |
| 2.2.3 OpenAI / Groq / … | that provider’s `--auth-choice` and key flag ([CLI automation](https://docs.openclaw.ai/start/wizard-cli-automation)) |
| 2.2.4 private Edgible URL | `--auth-choice custom-api-key --custom-base-url 'https://<app>.<org>.edgible.com/v1' --custom-model-id '…' --custom-api-key "$CUSTOM_API_KEY"` |

### 2.3.3 Pin a Flash model (required on Gemini free tier)

OpenClaw’s Google default is often a **Pro / preview** model. Free-tier quota on those is tiny — that is the **429** you hit if you skip this.

Google’s API name from 2.2.1 (`models/gemini-2.5-flash`) is **not** always OpenClaw’s id. Do not guess. List what *this* install knows, then set a **Flash** or **Flash-Lite** row from that list (avoid Pro / preview):

```bash
openclaw models list --provider google
```

Copy an id from the output. Pick in this order (use a row that is **actually listed**):

1. **`flash` in the name, no `pro`, no `preview`** — e.g. `google/gemini-2.5-flash`, `google/gemini-3-flash`, `google/gemini-flash-latest`.
2. If several Flash rows: prefer **latest / highest 2.x or 3.x Flash**, not `-lite`, not `-thinking`.
3. **Flash-Lite** only if you are hitting 429s on Flash and need more RPM (weaker at tools).
4. **Never** Pro, Ultra, or `*-preview` on the AI Studio **free** key — that is the 429.

Then:

```bash
openclaw models set google/<the-flash-id-from-list>
openclaw gateway restart
```

If `set` or the next chat says **model was not found**, you guessed. Run `list` again and set an id that is actually printed.

Skip this substep if you onboarded Ollama (2.2.2) or another cloud provider (2.2.3) whose default already works.

OpenClaw’s **memory search** still defaults to OpenAI embeddings even when chat is Gemini. You will see a warning that no `OPENAI_API_KEY` was found. That is not required for this trial — do **not** add an OpenAI key just to silence it. Disable it:

```bash
openclaw config set agents.defaults.memorySearch.enabled false
openclaw gateway restart
```

To keep semantic memory on the same Gemini key instead: `openclaw config set agents.defaults.memorySearch.provider gemini` (uses extra quota). Verify with `openclaw memory status --deep`.

### 2.3.4 Confirm the Gateway

```bash
openclaw gateway status
openclaw doctor
```

Expect the Gateway **running** on port **18789**, loopback. Confirm the bind with:

```bash
openclaw config get gateway.bind
ss -ltnp | grep 18789
```

You want `bind` = **loopback** (or equivalent), and `ss` showing **`127.0.0.1:18789`** (and maybe `[::1]:18789`). **`0.0.0.0:18789`** or `*:18789` means it is listening on every interface — not what this guide wants. NAT still hides that from the internet, but do not leave it that way.

Linux installs a **systemd user** unit. If you use SSH and then log out, keep it alive:

```bash
sudo loginctl enable-linger "$USER"
```

If status is down:

```bash
openclaw gateway install
openclaw gateway restart
openclaw logs --follow
```

(`Ctrl+C` stops following logs.)

### 2.3.5 Chat from the VM terminal

The Gateway must be up. Do **not** pass `--local` (that fights the running Gateway).

```bash
openclaw agent --agent main --thinking off --message "Say hello in one sentence."
```

You should get a short reply in the terminal. That is local OpenClaw working. Your phone still cannot reach it.

The **first** turn is often OpenClaw’s identity ritual (`Who am I? Who are you?`) instead of a literal hello. That still counts. Answer in one line, for example:

```bash
openclaw agent --agent main --thinking off --message "You are OpenClaw on my Ubuntu VM. I am Stefano. Say hello in one sentence."
```

**If the model was not found:** go back to **2.3.3**. You set an id OpenClaw does not have.

**If you see 429 / quota exceeded:** OpenClaw is fine — Google’s free tier said stop. You are still on Pro/preview, or you already used the daily cap. Pin Flash (2.3.3), wait a minute (RPM) or until tomorrow (daily). If logs say **google** is in **cooldown**, wait that out. To keep going now, use 2.2.3 (Groq / OpenRouter `:free` / OpenAI Platform) and re-onboard. Usage: [Google AI Studio](https://aistudio.google.com/).

Optional TUI on the VM console:

```bash
openclaw tui
```

### 2.3.6 Control UI in a browser (before Edgible)

If this Ubuntu VM has a **desktop**, do **not** hunt for the token and paste a URL by hand. From a **terminal on the VM desktop** (so it can open Firefox/Chromium):

1. Make sure the Gateway is running. If `openclaw gateway status` is not up:

```bash
openclaw gateway
```

Leave that terminal open (foreground). Or use `openclaw gateway start` if the systemd unit is installed.

2. In a **second** terminal on the same desktop:

```bash
openclaw dashboard
```

That launches the VM browser onto the Control UI (with a short-lived handoff — you should not need to paste `gateway.auth.token`). Send `hello`.

`curl` → **200** only means HTML is served. `openclaw dashboard` is the check that the **browser + WebSocket** path works.

If there is no GUI, there is no in-guest browser — skip to Edgible, or forward host `127.0.0.1:18789` → guest `18789` in UTM/VirtualBox and use the Mac browser. Do not port-forward 18789 on the router.

### 2.3.7 Point OpenClaw at Ollama on the Mac (optional)

**Outcome:** Chat on the VM uses the Mac’s local model (unlimited tokens, no Gemini quota), still via native Ollama — not `/v1`. The dashboard picker lists that model after you register it.

Do this if you already onboarded with **Gemini** (2.3.2) and **2.2.2** `curl` from the VM already returns JSON. Do **not** re-run full `openclaw onboard` unless you want to redo Gateway setup.

On the **VM**:

```bash
HOST=$(ip route | awk '/default/ {print $3; exit}')
echo "Ollama host: $HOST"
curl -sS -m 5 "http://${HOST}:11434/api/tags"
```

Copy a model **name** from that JSON (example: `gpt-oss:20b` or `qwen3.5:27b`). There is no real Ollama key — `ollama-local` is a dummy.

An explicit `models.providers.ollama` block (`baseUrl`, `api`, `apiKey`) **turns off** auto-discovery. The Control UI picker stays Google-only until you also register the pulled tag in the provider `models` array (use the name from `/api/tags`, not a guess):

```bash
openclaw config set models.providers.ollama.baseUrl "http://${HOST}:11434"
openclaw config set models.providers.ollama.api ollama
openclaw config set models.providers.ollama.apiKey ollama-local
openclaw config set models.providers.ollama.models \
  '[{"id":"gpt-oss:20b","name":"gpt-oss:20b"}]' --strict-json
openclaw gateway restart
openclaw models list --provider ollama
```

`list` must print `ollama/gpt-oss:20b` (or your tag). Then you can pin it as primary if you want local-only chat:

```bash
openclaw models set ollama/gpt-oss:20b
openclaw gateway restart
```

Use the tag you actually pulled (`ollama/qwen3.5:27b` if that is the name). Then:

```bash
openclaw agent --agent main --thinking off --message "Say hello in one sentence."
```

First reply can be slow (Mac loads the weights). If it still behaves like Gemini, `models set` missed — `list` again and set an id that is printed.

To make **Gemini Flash the default** and **gpt-oss only when Gemini has no capacity** (429 / quota / timeout), do **not** leave `models set ollama/…` as primary. After the Ollama provider is configured (the `config set` lines above), on the VM:

```bash
openclaw models list --provider google
openclaw models list --provider ollama
```

Use ids that `list` actually prints (Flash, not Pro; `ollama/gpt-oss:20b` or whatever tag you pulled — **not** a 20 GB-resident Qwen). Then:

```bash
openclaw models set google/<the-flash-id-from-list>
openclaw config set agents.defaults.model.fallbacks '["ollama/gpt-oss:20b"]' --strict-json
openclaw gateway restart
openclaw config get agents.defaults.model
```

You want `primary` = `google/…flash…` and `fallbacks` including `ollama/…`.

**Control UI picker.** Fallbacks do **not** fill the dashboard list. After `gateway restart`, **refresh** the Control UI tab. gpt-oss appears only when `openclaw models list --provider ollama` already prints it (the `models` array above). If `list` omits it, the picker stays Google-only — Ollama often hides models that `/api/show` does not mark as **tool-capable** with **≥16K** context. Fallback can still use `ollama/gpt-oss:20b` from config. To pin local in chat anyway: `/model ollama/gpt-oss:20b`.

Failover applies to the **configured default** and to **cron** ([chapter 4](04-openclaw-changes-edgible-site.md)). It does **not** apply if you pick a model in the Control UI picker or `/model` — that choice is strict. Leave the picker on **Default** so Gemini can fail over.

Keep the Ollama model small enough that the Mac does not swap, or the “backup” is slower than waiting for Gemini. Do not publish port **11434** on the router.

### 2.3.8 Do not do these yet

- Telegram / Discord — they already dial out; they are not the Edgible job. Skill: [chapter 5](05-edgible-openclaw-skill.md). Telegram: [chapter 6](06-telegram-pocket-client.md). WhatsApp: [chapter 7](07-whatsapp-pocket-client.md).
- Tailscale Serve / Funnel / Cloudflare Tunnel.
- `gateway.auth` set to none.

### 2.3.9 Verify

- [ ] `openclaw --version` prints a version on the VM.
- [ ] `openclaw gateway status` shows running on **18789** (loopback).
- [ ] After **2.3.3**, `openclaw models status` shows a **Flash** (not Pro/preview) default if you used Gemini free tier.
- [ ] After **2.3.7** (optional): `openclaw models list --provider ollama` prints `ollama/gpt-oss:…` (or your tag); Control UI picker shows that model after a refresh; leave picker on **Default** if Gemini should fail over. `openclaw models status` and a hello reply still work (Mac Ollama, not `127.0.0.1` on the guest).
- [ ] `openclaw agent --agent main --thinking off --message "Say hello in one sentence."` returns a reply (identity ritual counts).
- [ ] Hello World on the phone still loads (Edgible tunnel unchanged).
- [ ] `curl` to `http://127.0.0.1:18789/` on the VM returns **200**.
- [ ] From a VM **desktop** terminal: Gateway running, then `openclaw dashboard` opens the Control UI and chat works.

---

## Next

[3. OpenClaw Control UI through Edgible](03-publish-openclaw-control-ui.md). Skill (not this chapter): [5. OpenClaw skill for the Edgible CLI](05-edgible-openclaw-skill.md). Series: [README](README.md).
