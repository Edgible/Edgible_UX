# 3. n8n uses the published Ollama URL

**n8n is a remote self-hosted caller.** It uses `https://ollama.<org>.edgible.com/v1` with Bearer — not the Mac’s LAN.

The Mac (and its Ubuntu guest) only **serve** Ollama and the website. n8n runs on a **different** self-hosted VM (for example on a Windows host). That is the use case: workflow box → published LLM, GPU stays on the Mac. n8n’s **Ollama self-hosted** endpoint speaks Ollama’s **OpenAI-compatible** API (`/v1/models`, `/v1/chat/completions`). Origin + **`/v1`** + the secret. Do not put that secret on a public webhook. Do not set the **ollama** app to **None**.

## 3.1 The job

You point n8n at the published URL, pick **`qwen2.5:7b`**, and run one chain. GPU stays on the Mac.

**Done when**

- The endpoint **tests successfully**.
- The model is **`qwen2.5:7b`** (or your `ollama ls` tag), not **qwen3-coder**.
- One **Execute** returns a sentence. Mac `ollama ps` shows GPU.

**Need first:** n8n’s editor (on the Windows VM, or its own Edgible **org** URL). [Chapter 2](02-edgible-to-ollama.md) — cellular `curl` to `/api/tags` with Bearer already works.

**Not this chapter:** installing n8n on the Mac guest, pulling **qwen3-coder**, Open WebUI on the 4 GB UTM VM, n8n’s **AI Assistant sandbox**, or OpenClaw.

## 3.2 n8n does not require qwen3-coder

Ollama’s n8n page uses **`qwen3-coder`** as an example. Use **`qwen2.5:7b`** from `ollama ls` on the Mac. Do **not** pull `qwen3-coder` (~**19 GB**).

## 3.3 Credential (Edgible + `/v1`)

In **your** n8n editor (Windows VM — not the Mac):

1. Add an **Ollama** credential / **self-hosted** endpoint.
2. **Endpoint / Base URL** = `https://ollama.YOUR-ORG.edgible.com/v1`  
   Copy the host from `edgible app list` on the **Mac guest**. **Include `/v1`.** No `:11434`. No `/api`.
3. **API Key** = the **secret** from [2.5](02-edgible-to-ollama.md) (not the key **id**).
4. **Save.** Connection test succeeds.

`/v1` is required: this form calls `/v1/models`, not `/api/tags`.

Do **not** use `localhost:11434` or a UTM `192.168.64.1` from Windows — those are the Mac’s loopback / virt LAN. The Windows VM is off that network.

Then set the **model** to **`qwen2.5:7b`**.

### Skip the n8n sandbox

The AI settings wizard’s next step is a **sandbox**. That is for n8n’s **AI Assistant** (it writes workflows and runs code in extra containers). It is **not** required to call Ollama from a workflow.

**Skip it** for this chapter. Daytona or `n8n-sandbox` can wait until you want Assistant on the Windows VM. Leave Assistant unfinished if the UI complains.

### Classic Ollama Chat Model (no `/v1`)

Some n8n builds still have a credential that GETs `/api/tags`. That one must **not** have `/v1`. For an off-box caller it is still the Edgible origin **without** `/v1`, plus the same Bearer secret. Prefer **3.3** when the UI is “self-hosted” and the test only passed with `/v1`.

## 3.4 One chain

1. **Add workflow.** **Manual Trigger**.
2. Add **Basic LLM Chain** (or **AI Agent**).
3. Attach the chat model that uses the credential from 3.3.
4. **Model:** **`qwen2.5:7b`**. Turn **Enable Thinking** **off** if the 7B has no thinking mode.
5. Prompt: `Say hello in one sentence`. **Save.** **Execute workflow.**

First run can take several seconds (Mac cold load). You want a short sentence and Mac `ollama ps` on **GPU**.

### Verify

- [ ] Endpoint is `https://ollama.<org>.edgible.com/v1` and the **secret**, test OK.
- [ ] Model is **`qwen2.5:7b`**, not qwen3-coder.
- [ ] Execute returns text; Mac `ollama ps` is GPU.
- [ ] **ollama** app is still **api-key**. The Mac guest still is not running n8n.

---

## Next

[4. OpenClaw uses that URL](04-openclaw-uses-ollama.md). Series: [README](README.md).
