# 4. OpenClaw uses the published Ollama URL

**OpenClaw is a remote self-hosted caller.** The Gateway uses `https://ollama.<org>.edgible.com` with Bearer — not the Mac’s LAN.

OpenClaw and n8n each have their **own** VM on a **different** home computer from the Mac. The Mac guest only publishes Ollama (**api-key**). Do not point this Gateway at `192.168.64.1` or UTM `$HOST` — that virt LAN is not this box. Do not put the Edgible secret on Control UI **None**. Do not set the **ollama** app to **None**.

[OpenClaw chapter 9](../openclaw-on-edgible/09-models-beyond-free-gemini.md) **9.5** is same-LAN only (Gateway next to the Mac). Skip it here. Cloud keys in that chapter can stay; this chapter only registers the published 7B.

## 4.1 The job

On the **OpenClaw** VM, register the Edgible origin as the Ollama provider, list `ollama/qwen2.5:7b`, and get one hello.

**Done when**

- `openclaw models list --provider ollama` prints `ollama/qwen2.5:7b` (or your tag).
- `openclaw agent --agent main --thinking off --model ollama/qwen2.5:7b --message "Say hello in one sentence."` replies.
- Mac `ollama ps` shows that tag on **GPU**.

**Need first:** Gateway up on **this** VM ([2. OpenClaw on Edgible](../openclaw-on-edgible/README.md) applied here, not on the Mac). [Chapter 2](02-edgible-to-ollama.md) — cellular `curl` with Bearer already works.

**Not this chapter:** installing Ollama on the OpenClaw VM, n8n, or LAN `http://$HOST:11434`.

## 4.2 Provider (native Ollama API)

OpenClaw’s `api ollama` talks `/api/tags` and `/api/chat`. **No `/v1`** (that suffix is n8n’s self-hosted / Chatbox path).

On the **OpenClaw** VM (not the Mac):

```bash
openclaw config set models.providers.ollama.baseUrl "https://ollama.YOUR-ORG.edgible.com"
openclaw config set models.providers.ollama.api ollama
openclaw config set models.providers.ollama.apiKey "<secret-from-chapter-2.5>"
openclaw config set models.providers.ollama.models \
  '[{"id":"qwen2.5:7b","name":"qwen2.5:7b"}]' --strict-json
openclaw gateway restart
openclaw models list --provider ollama
```

Copy the host from `edgible app list` on the **Mac guest**. The **secret** is from `api-keys create`, not the key **id**. Prefer putting the secret in `~/.openclaw/.env` if you already keep provider keys there, so it is not sitting in shell history.

`list` must print `ollama/qwen2.5:7b`. HTML / login: the **ollama** app is **org**. 401: wrong secret. Empty list / timeout: Mac Ollama quit, forwarder down, or the Mac VM slept.

Then either:

```bash
openclaw models set ollama/qwen2.5:7b
```

or keep Gemini/DeepSeek as primary and put `ollama/qwen2.5:7b` in **fallbacks** ([9.7](../openclaw-on-edgible/09-models-beyond-free-gemini.md)). `/think off` (or `thinkingDefault off`) still applies.

Ollama may hide tags that `/api/show` does not mark as tool-capable with **≥16K** context. Fallback can still use the config id. Pin in chat: `/model ollama/qwen2.5:7b`.

If `list` fails but n8n’s **`/v1`** test works, OpenClaw may be hitting the OpenAI-compatible surface — try `api` `openai-completions` and `baseUrl` `https://ollama.YOUR-ORG.edgible.com/v1` with the same secret. Prefer native `ollama` when `list` already works.

## 4.3 Hello

```bash
openclaw agent --agent main --thinking off --model ollama/qwen2.5:7b --message "Say hello in one sentence."
```

First run can take several seconds (Mac cold load). You want a short sentence and Mac `ollama ps` on **GPU**.

### Verify

- [ ] `baseUrl` is the **ollama.** Edgible host, **no** `/v1` for `api ollama`, **secret** not id.
- [ ] `models list --provider ollama` shows `qwen2.5:7b`.
- [ ] Agent hello replies; Mac GPU.
- [ ] **ollama** app is still **api-key**. This VM is not the Mac guest.

---

## Next

That's this series. [Index](README.md).
