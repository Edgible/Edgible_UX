# 9. Models beyond free Gemini

**Flash proved hello. This is how you live on a paid or local model — with a fallback.**

Cloud keys and a **small** same-LAN Ollama failover belong here. Publishing a **big** local or remote LLM through Edgible, then pointing n8n **and** OpenClaw at that URL, is [3. LLM on Edgible](../llm-on-edgible/README.md) — not this chapter.

## 9.1 The job

[2. OpenClaw on the VM](02-openclaw-on-the-box.md) onboarded **free Gemini Flash**. That is enough for the series. Free-tier **429**s, `Think: medium` hangs, and a huge local failover are why Telegram then feels broken. Here you add another provider **without** reinstalling the Gateway: DeepSeek, OpenAI, Groq, Claude, or a small Ollama on the same LAN. Optional: a fallback list so a 429 still answers. A published model URL is [3. LLM on Edgible](../llm-on-edgible/README.md).

A Cursor subscription is **not** a chat model. That is [8. Cursor Agent](08-cursor-agent.md) (ACP). Do not paste a Cursor key into `openclaw models set`.

**Done when**

- `openclaw models list --provider <that-provider>` prints the id you will use.
- `openclaw agent --agent main --thinking off --model <provider/id> --message "Say hello in one sentence."` replies on the VM.
- `openclaw config get agents.defaults.model` shows that id as **primary** if you switched the default (Control UI picker still **Default**).
- Optional: `fallbacks` includes Gemini Flash and/or a small Ollama tag; a DM can show `↪️ Model Fallback: … (rate_limit)`.

**Need first:** [2. OpenClaw on the VM (loopback Gateway)](02-openclaw-on-the-box.md) (Gateway up, Gemini hello already worked). The rest of the series can stay on Flash until you do this.

**Not this chapter:** installing OpenClaw, publishing Control UI, pairing Telegram, hiring Cursor, or publishing an Ollama / vLLM Edgible app ([3. LLM on Edgible](../llm-on-edgible/README.md)).

## 9.2 Rules that stay

Do this on the **VM** (Gateway host). Put keys in `~/.openclaw/.env` so systemd sees them. Do **not** re-run full `openclaw onboard` unless you want to redo Gateway setup.

| Rule | Why |
| --- | --- |
| Control UI / Telegram picker **Default** | A pinned `/model` is **strict** — no failover. |
| `/think off` (or `thinkingDefault off`) | Flash and DeepSeek V4 both hang if thinking stays on **medium**. |
| `models set` = primary; `fallbacks` = backup | Fallback is turn-local. Next message starts on primary again. |
| Use an id `list` actually prints | Guessing `deepseek/deepseek-v4-flash` when the catalog says something else is “model not found”. |
| Do **not** publish Ollama or the Gateway on Edgible **None** | Control UI stays **org**. A published inference URL is [3. LLM on Edgible](../llm-on-edgible/README.md), never **None**. |

Check cooldown **before** blaming the new key:

```bash
openclaw models status
openclaw status --usage
```

## 9.3 DeepSeek V4 Flash (cheap paid default)

Best first paid try for this tutorial load (hellos, `/skill`, small cron): **not** Gemini Flash, **not** Grok Fast, **not** DeepSeek R1 / “thinking” SKUs.

1. Create a key at [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys) and put credit on the account.
2. On the VM, add it to `~/.openclaw/.env`:

```bash
# one line, no quotes
echo 'DEEPSEEK_API_KEY=sk-YOURKEY' >> ~/.openclaw/.env
openclaw gateway restart
```

3. List, pin Flash (onboarding wizards often default to **Pro**):

```bash
openclaw models list --provider deepseek
openclaw models set deepseek/deepseek-v4-flash
openclaw gateway restart
```

Use the Flash id `list` printed. Then:

```bash
openclaw agent --agent main --thinking off \
  --model deepseek/deepseek-v4-flash \
  --message "Say hello in one sentence."
```

Identity ritual still counts. If that fails, prove the key without OpenClaw:

```bash
set -a && source "$HOME/.openclaw/.env" && set +a
curl -sS https://api.deepseek.com/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"Reply with exactly: ds-ok"}],"max_tokens":16}'
```

JSON with a short completion means the guest can reach DeepSeek. If curl works and `openclaw agent` does not, the Gateway is not loading `.env` — restart again.

Optional wizard (only if you never added the provider): `openclaw onboard --auth-choice deepseek-api-key`. Skip it if the Gateway is already how you like it.

## 9.4 Other cloud keys

Same pattern: env var in `~/.openclaw/.env`, `gateway restart`, `models list --provider …`, `models set`, then the `--model` hello from 9.3.

| You want | Typical env | List / set (confirm with `list`) |
| --- | --- | --- |
| DeepSeek V4 Flash | `DEEPSEEK_API_KEY` | `deepseek/deepseek-v4-flash` |
| Groq (snappy, cheap) | `GROQ_API_KEY` | `groq/llama-3.3-70b-versatile` |
| OpenAI Platform | `OPENAI_API_KEY` | `openai/…` from `list` — not ChatGPT Free |
| Claude Sonnet | `ANTHROPIC_API_KEY` | `anthropic/claude-sonnet-…` from `list` |
| OpenRouter (many models, one bill) | `OPENROUTER_API_KEY` | `openrouter/…` |
| xAI Grok | see [xAI](https://docs.openclaw.ai/providers/xai) | not Groq |

Exact `--auth-choice` flags: [CLI automation](https://docs.openclaw.ai/start/wizard-cli-automation) and [model providers](https://docs.openclaw.ai/concepts/model-providers). Set a spend cap on the provider console.

**Claude vs Cursor:** a Cursor product sub does not fill `ANTHROPIC_API_KEY`. Sonnet as Telegram’s brain needs an Anthropic key (or Claude Code on the box — not this chapter).

**Cost for these tutorials** (fat OpenClaw prompt, short replies): DeepSeek Flash is **cents**. Grok mid-tier is **dollars**. Sonnet is **tens of times** DeepSeek on output, and hourly On this day cron is the only thing that can add up. Keep cron on Flash or DeepSeek Flash.

## 9.5 Local Ollama

Prompts stay on hardware you own. If OpenClaw and Ollama **share a LAN** (Gateway in the Mac’s UTM guest), point at the LAN URL ([9.5.2](#952-ollama-on-the-mac-openclaw-in-the-vm-32-gb-mac)) — do not hairpin through Edgible. If the Gateway is on a **different** home VM (the layout in [3. LLM on Edgible](../llm-on-edgible/README.md)), skip 9.5.2–9.5.3 and use [4. OpenClaw uses that URL](../llm-on-edgible/04-openclaw-uses-ollama.md).

### 9.5.1 Same machine as OpenClaw (enough RAM)

| RAM on the VM / mini-PC | What to expect |
| ----------------------- | -------------- |
| **4 GB** (this guide’s VM default) | Too small. Stay on a cloud key. |
| **8 GB** | Floor. Tiny model only (~1B). Weak at tools. |
| **16 GB+** | Usable local chat. |

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:1b
ollama run llama3.2:1b "Say hello in one word"
```

Onboard-style (only if you are **not** already on Gemini): `--auth-choice ollama --custom-model-id llama3.2:1b`. Otherwise register the provider as in 9.5.3.

### 9.5.2 Ollama on the Mac, OpenClaw in the VM (32 GB Mac)

Do **not** put the weights in the 8 GB guest. Install [Ollama for Mac](https://ollama.com/download). After the VM’s 8 GB, you have on the order of **16 GB** left for a model.

On the **Mac**:

```bash
ollama pull qwen2.5:7b
ollama run qwen2.5:7b "Say hello in one word"
```

**Fallback** should be a **7B-class** chat model (`qwen2.5:7b` or `llama3.1:8b`). `gpt-oss:20b` (13 GB) and `qwen3.5:27b` (17 GB) are slow failovers next to the guest — they make a Gemini 429 feel like a hang. Use a 20B only as an explicit `/model` when you want a slow local turn.

Ollama defaults to **Mac localhost only**. The VM’s `127.0.0.1` is the *guest*. Listen on the LAN (home only — do not port-forward **11434** on the router):

```bash
launchctl setenv OLLAMA_HOST "0.0.0.0:11434"
killall Ollama; open -a Ollama
```

On the **VM**:

```bash
HOST=$(ip route | awk '/default/ {print $3; exit}')
curl -sS "http://${HOST}:11434/api/tags"
```

You want JSON with your tag, not connection refused. UTM NAT is often `192.168.64.1` if `$HOST` is wrong. Do **not** curl `127.0.0.1` **on the VM**.

### 9.5.3 Point the Gateway at Mac Ollama

There is no real Ollama key — `ollama-local` is a dummy. An explicit `models.providers.ollama` block **turns off** auto-discovery. Register the tag from `/api/tags`:

```bash
HOST=$(ip route | awk '/default/ {print $3; exit}')
openclaw config set models.providers.ollama.baseUrl "http://${HOST}:11434"
openclaw config set models.providers.ollama.api ollama
openclaw config set models.providers.ollama.apiKey ollama-local
openclaw config set models.providers.ollama.models \
  '[{"id":"qwen2.5:7b","name":"qwen2.5:7b"}]' --strict-json
openclaw gateway restart
openclaw models list --provider ollama
```

`list` must print `ollama/qwen2.5:7b` (or your tag). Then either `openclaw models set ollama/qwen2.5:7b` (local primary) or leave DeepSeek/Gemini as primary and put Ollama in **fallbacks** (9.7).

Ollama often hides models that `/api/show` does not mark as **tool-capable** with **≥16K** context. Fallback can still use the config id. To pin local in chat: `/model ollama/qwen2.5:7b`.

## 9.6 A published model (another home VM)

If OpenClaw is **not** next to the Mac, do not use `$HOST:11434`. Register `https://ollama.<org>.edgible.com` with the **api-key** secret: [4. OpenClaw uses that URL](../llm-on-edgible/04-openclaw-uses-ollama.md). Do not set that app to **None**.

## 9.7 Fallback chain

Example: DeepSeek Flash primary, Gemini Flash then local 7B when DeepSeek is down:

```bash
openclaw models list --provider deepseek
openclaw models list --provider google
openclaw models list --provider ollama
openclaw models set deepseek/deepseek-v4-flash
openclaw config set agents.defaults.model.fallbacks \
  '["google/<the-flash-id-from-list>","ollama/qwen2.5:7b"]' --strict-json
openclaw gateway restart
openclaw config get agents.defaults.model
```

You want `primary` = DeepSeek Flash and `fallbacks` listing ids that `list` printed.

Failover applies to the **configured default** and to **cron** ([chapter 4](04-openclaw-changes-edgible-site.md)). It does **not** apply if you pick a model in the Control UI or `/model`. Leave the picker on **Default**.

In a **Telegram DM**, a switch can show once per state change:

```text
↪️ Model Fallback: ollama/qwen2.5:7b (selected deepseek/deepseek-v4-flash; rate_limit)
```

Groups suppress that notice; `/status` still has Fallback. The notice is **not** a live ticker at the instant of the 429 — typing until the fallback has tokens.

## 9.8 Verify

- [ ] `openclaw agent … --model <id> … hello` replies (identity ritual counts).
- [ ] `openclaw models status` shows the new primary; cooldown empty or understood.
- [ ] Control UI picker is **Default**. `/status` in Telegram matches.
- [ ] `/think off` (or `openclaw config set agents.defaults.thinkingDefault off`).
- [ ] If you set fallbacks: `config get agents.defaults.model` lists them; you did **not** use a 20B/27B as the snappy backup.
- [ ] Hello World and openclaw-ui still load. You did not publish **11434** or **18789** on the router.

---

## Next

That's the series for models. [10. Tear down OpenClaw](10-openclaw-teardown.md) when you want the agent and **openclaw-ui** gone. [Index](README.md). Cursor ACP (not a chat key) is [8. Cursor Agent from OpenClaw on the Edgible site](08-cursor-agent.md). A published LLM is [3. LLM on Edgible](../llm-on-edgible/README.md).
