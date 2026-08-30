# 4. OpenClaw uses the published Ollama URL

**Point the OpenClaw Gateway at the published Ollama hostname with a bearer secret.**

## 4.0 Why

OpenClaw and n8n each have their own VM on a different home computer from the Mac, and an agent that drives tools needs a model it can actually reach. The Gateway cannot be pointed at `192.168.64.1` or UTM `$HOST`. That virt LAN is only the Mac and its own guest, not this box. It cannot use an `org` hostname either, because there is no human to complete a browser login mid-turn, and with `None` anyone on the internet could run inference on your GPU. So the Gateway calls the published `api-key` origin with a Bearer secret, and the secret stays in this VM’s config, not behind a Control UI left on `None`.

[OpenClaw chapter 8](../openclaw-on-edgible/08-models-beyond-free-gemini.md) 8.5 is same-LAN only (Gateway next to the Mac). Skip it here. Cloud keys in that chapter can stay; this chapter only registers the published 20B.

```
OpenClaw VM (other PC)   Gateway ──► https://ollama.<org>.edgible.com   (+ Bearer, no /v1)
                                              │
Ubuntu guest             Edgible serving agent ──► 127.0.0.1:11434 (socat)
                                              │
macOS host               Ollama.app (Metal) — gpt-oss:20b loads here
```

**Where you run this:** every `openclaw` command runs on the **OpenClaw VM** (a different home computer); only `ollama ls` / `ollama ps` / `ollama show` run on the **macOS host**, and the hostname and secret are copied from the **Ubuntu guest**.

## 4.1 The job

On the OpenClaw VM, register the Edgible origin as the Ollama provider, list `ollama/gpt-oss:20b`, and get one hello.

**Why this tag.** `qwen2.5:7b` is fine for the `curl` and n8n workflow smoke tests, but OpenClaw drives tools: read a file, edit it, run a command. A 7B drops tool calls on multi-step work. `gpt-oss:20b` (~13 GB, thinking-capable) is the local tag that holds a code-change turn. Keep the 7B as a fallback, not the model you hand real work to.

**Done when**

- `baseUrl` is the `ollama.` Edgible host, no `/v1` for `api ollama`, secret not id.
- `openclaw models list --provider ollama` prints `ollama/gpt-oss:20b`.
- `openclaw agent --agent main --thinking off --model ollama/gpt-oss:20b --message "Say hello in one sentence."` replies, and Mac `ollama ps` shows that tag on GPU.
- `ollama` app is still `api-key`. This VM is not the Mac guest.

**Need first:** Gateway up on this VM ([OpenClaw on Edgible](../openclaw-on-edgible/README.md) applied here, not on the Mac). [Chapter 2](02-edgible-to-ollama.md), with cellular `curl` and Bearer already working. `gpt-oss:20b` pulled on the Mac, so `ollama ls` on the host shows it ([chapter 3](03-n8n-uses-ollama.md) pulls it for the Assistant). ~13 GB of Mac RAM free after the UTM guest.

**Not this chapter:** installing Ollama on the OpenClaw VM, n8n, or LAN `http://$HOST:11434`.

## 4.2 Provider (native Ollama API)

OpenClaw’s `api ollama` talks `/api/tags` and `/api/chat`. No `/v1` (that suffix is n8n’s self-hosted / Chatbox path).

On the OpenClaw VM (not the Mac):

```bash
openclaw config set models.providers.ollama.baseUrl "https://ollama.YOUR-ORG.edgible.com"
openclaw config set models.providers.ollama.api ollama
openclaw config set models.providers.ollama.apiKey "<secret-from-chapter-2.5>"
openclaw config set models.providers.ollama.models \
  '[{"id":"gpt-oss:20b","name":"gpt-oss:20b"},{"id":"qwen2.5:7b","name":"qwen2.5:7b"}]' --strict-json
openclaw gateway restart
openclaw models list --provider ollama
```

Copy the host from `edgible app list` on the Mac guest. The secret is from `api-keys create`, not the key id. Prefer putting the secret in `~/.openclaw/.env` if you already keep provider keys there, so it is not sitting in shell history.

`list` must print `ollama/gpt-oss:20b` (and the 7B). HTML / login: the `ollama` app is `org`. 401: wrong secret. Empty list / timeout: Mac Ollama quit, forwarder down, or the Mac VM slept.

Then either:

```bash
openclaw models set ollama/gpt-oss:20b
```

or keep Gemini/DeepSeek as primary and put `ollama/gpt-oss:20b` in fallbacks ([8.7](../openclaw-on-edgible/08-models-beyond-free-gemini.md)). `/think off` (or `thinkingDefault off`) still applies.

**Thinking.** Unlike the 7B, this tag can think: `ollama show gpt-oss:20b` lists thinking under capabilities. Use `--thinking off` for the hello below so a cold 20B does not look like a hang. Leave thinking on when you want it planning a code change.

Do not make the 20B a fallback. 13 GB on a cold load makes a cloud 429 feel like a hang ([8.5.2](../openclaw-on-edgible/08-models-beyond-free-gemini.md#852-ollama-on-the-mac-openclaw-in-the-vm-32-gb-mac)). Fallback stays `ollama/qwen2.5:7b`; reach for the 20B as an explicit primary or `/model`.

Ollama may hide tags that `/api/show` does not mark as tool-capable with ≥16K context. Fallback can still use the config id. Pin in chat: `/model ollama/gpt-oss:20b`.

If `list` fails but n8n’s `/v1` test works, OpenClaw may be hitting the OpenAI-compatible surface. Try `api` `openai-completions` and `baseUrl` `https://ollama.YOUR-ORG.edgible.com/v1` with the same secret. Prefer native `ollama` when `list` already works.

## 4.3 Hello

```bash
openclaw agent --agent main --thinking off --model ollama/gpt-oss:20b --message "Say hello in one sentence."
```

**Smoke test (OpenClaw VM).** First run can take tens of seconds, because 13 GB has to load into Mac RAM. You want a short sentence and Mac `ollama ps` on GPU. Ask again straight after and it should be quick, since the model stays resident.

Once hello works, give it real work in chat (`/model ollama/gpt-oss:20b`, thinking on), e.g. rename a function across a file and read back the diff. A 7B drops tool calls on that kind of multi-step turn.

### Verify

- [ ] `baseUrl` is the `ollama.` Edgible host, no `/v1` for `api ollama`, secret not id.
- [ ] `openclaw models list --provider ollama` prints `ollama/gpt-oss:20b`.
- [ ] `openclaw agent --agent main --thinking off --model ollama/gpt-oss:20b --message "Say hello in one sentence."` replies, and Mac `ollama ps` shows that tag on GPU.
- [ ] `ollama` app is still `api-key`. This VM is not the Mac guest.

---

## Next

That’s this series. [Index](README.md).
