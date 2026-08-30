# 1. Ollama on bare metal

**A model answering on your own GPU, with nothing leaving the machine yet.**

## 1.0 Why

Nothing can be published until something is actually answering, and the machine that answers has to be the one with the GPU. On this topology that is the Mac host. `ollama`, the menu-bar Ollama app and Metal are all macOS, and there is no `apt install ollama` anywhere in this chapter. So use Terminal.app (or iTerm) on the MacBook or Mac mini, never an SSH session into the UTM guest.

Do not install Ollama inside the Ubuntu guest, where Edgible’s serving agent already lives. A UTM guest cannot access the Mac’s GPU, so inference falls back to CPU, and it takes RAM from a 4 GB guest that has to run Edgible and the website. Keep the weights and the GPU on the Mac, leave Ollama on its default Mac localhost bind, and let [chapter 2](02-edgible-to-ollama.md) do the forwarding and the publishing.

**Where you run this:** every command in this chapter runs on the **macOS host** (Terminal.app on the Mac), not in the Ubuntu guest.

## 1.1 The job

You install Ollama on the Mac that hosts the Ubuntu VM, pull a 7B-class chat model, run a one-line hello, and list what is on disk (`ollama ls`). You confirm the process is on GPU (Metal), not a slow CPU fall-through. Extra tags below are optional now; they are the ones n8n and OpenClaw will want later.

**Done when**

- Ollama is installed on macOS, not in the Ubuntu guest (`which ollama` on the Mac).
- `ollama run qwen2.5:7b "Say hello in one word"` prints a short reply on the Mac (Terminal or the Ollama app).
- `ollama ls` lists `qwen2.5:7b` (and any extras you pulled).
- `ollama ps` shows that chat model with a GPU processor (not 100% CPU).
- You did not change `OLLAMA_HOST` yet.
- Port `11434` is not forwarded on the router.

**Need first:** A Mac with enough RAM left after the Ubuntu VM: a 7B wants on the order of 8 GB+ for weights. The VM from [Edgible on an Ubuntu VM](../start-here/01-edgible-on-vm.md) can stay running; you do not use it in this chapter. [Ollama for Mac](https://ollama.com/download).

**Not this chapter:** `OLLAMA_HOST=0.0.0.0`, socat, an Edgible app, n8n, OpenClaw, or `curl` from the VM.

## 1.2 Install and hello (macOS host only)

On the Mac, in host Terminal, not the Ubuntu VM:

1. Install from [ollama.com/download](https://ollama.com/download). Open Ollama once so the menu-bar app is running.
2. Pull and run:

```bash
ollama pull qwen2.5:7b
ollama run qwen2.5:7b "Say hello in one word"
```

**Smoke test (macOS host).** You want a single word (or a short line) in a few seconds, not a multi-minute crawl.

3. See what is installed:

```bash
ollama ls
```

You want a row for `qwen2.5:7b` (size on the order of 4–5 GB). `ls` is the disk catalog. `ps` (next) is what is loaded right now.

4. Optional. Pull a small set for [chapter 3](03-n8n-uses-ollama.md) / [chapter 4](04-openclaw-uses-ollama.md) so you are not waiting on downloads later. Skip any tag that will not fit next to the Ubuntu VM.

| Tag | Later | Notes |
| --- | --- | --- |
| `qwen2.5:7b` | OpenClaw chat / tools; n8n workflow | Required for this chapter. 7B-class, tool-friendly. |
| `gpt-oss:20b` | n8n **AI Assistant** chat | Must support thinking (~13 GB). The AI Assistant always sends thinking; a 7B fails Hello. Proven with sandbox + SearXNG (search-backed chat). Pull for [chapter 3](03-n8n-uses-ollama.md) use case 2. Not for OpenClaw failover. |
| `llama3.1:8b` | Same roles as 7B, second chat model | Alternate 7B-class if Qwen misbehaves. |
| `llama3.2:3b` | n8n smoke, cheap retries | Smaller, weaker at tools. Fine for “did n8n get a completion?” |
| `nomic-embed-text` | n8n embeddings / RAG | Not a chat model. Tiny. Pull if you will index text in n8n. |

```bash
ollama pull llama3.1:8b
ollama pull llama3.2:3b
ollama pull nomic-embed-text
ollama ls
```

Do not put `gpt-oss:20b` / `qwen3.5:27b` in OpenClaw fallbacks. They make a Gemini 429 feel hung ([OpenClaw chapter 8](../openclaw-on-edgible/08-models-beyond-free-gemini.md)). `gpt-oss:20b` is the n8n Assistant chat model, not the OpenClaw default.

5. In another Terminal, while the 7B is loaded (or run the prompt again):

```bash
ollama ps
```

You want a GPU / Metal processor for `qwen2.5:7b`. 100% CPU means the model is not on the GPU. Free RAM, quit other apps, or use a smaller tag only to debug the install, then come back to 7B.

Leave Ollama’s default bind (Mac localhost). The VM still cannot reach it; that is [chapter 2](02-edgible-to-ollama.md).

### Verify

- [ ] Ollama is installed on macOS, not in the Ubuntu guest (`which ollama` on the Mac).
- [ ] `ollama run qwen2.5:7b "Say hello in one word"` prints a short reply on the Mac (Terminal or the Ollama app).
- [ ] `ollama ls` lists `qwen2.5:7b` (and any extras you pulled).
- [ ] `ollama ps` shows that chat model with a GPU processor (not 100% CPU).
- [ ] You did not change `OLLAMA_HOST` yet.
- [ ] Port `11434` is not forwarded on the router.

---

## Next

[2. Edgible publishes Ollama](02-edgible-to-ollama.md). Series: [README](README.md).
