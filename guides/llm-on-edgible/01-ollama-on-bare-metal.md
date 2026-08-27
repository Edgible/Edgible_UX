# 1. Ollama on bare metal

**The model runs on macOS, with the GPU. The Ubuntu VM does not see it yet.**

**This whole chapter is macOS.** Use **Terminal.app** (or iTerm) on the MacBook / Mac mini — the **host**, not an SSH session into the UTM guest. `ollama`, the menu-bar **Ollama** app, and Metal are macOS. There is no `apt install ollama` here.

A UTM Ubuntu guest cannot use the Mac’s GPU. If you install Ollama *inside* the VM, you get CPU inference and you steal RAM from the guest. Edgible and the loopback forwarder are [chapter 2](02-edgible-to-ollama.md).

## 1.1 The job

You install Ollama on the Mac that hosts the Ubuntu VM, pull a 7B-class chat model, run a one-line hello, and list what is on disk (`ollama ls`). You confirm the process is on **GPU** (Metal), not a slow CPU fall-through. Extra tags below are optional now; they are the ones n8n and OpenClaw will want later.

**Done when**

- `ollama run qwen2.5:7b "Say hello in one word"` prints a short reply on the **Mac** (Terminal or the Ollama app).
- `ollama ls` lists **qwen2.5:7b** (and any extras you pulled).
- `ollama ps` shows that chat model with a **GPU** processor (not 100% CPU).
- You did **not** install Ollama in the Ubuntu guest.
- Port **11434** is not forwarded on the router.

**Need first:** A Mac with enough RAM left **after** the Ubuntu VM: a **7B** wants on the order of **8 GB+** for weights. The VM from [Edgible on an Ubuntu VM](../openclaw-on-edgible/01-edgible-on-vm.md) can stay running; you do not use it in this chapter. [Ollama for Mac](https://ollama.com/download).

**Not this chapter:** `OLLAMA_HOST=0.0.0.0`, socat, an Edgible app, n8n, OpenClaw, or `curl` from the VM.

## 1.2 Words you'll use

| Word | Here |
| --- | --- |
| **Bare metal** | **macOS** on the MacBook (or Mac mini) — not the UTM Ubuntu guest. |
| **Ollama.app** | macOS menu-bar app. The Linux CLI error “could not find ollama app” means you are not on macOS, or the app is quit. |
| **11434** | Ollama’s HTTP port. Default is **localhost on the Mac only**. |
| **Metal** | How Ollama uses the Mac GPU. The Ubuntu VM cannot do this. |
| **7B** | Size class for this smoke test (`qwen2.5:7b`). Bigger tags wait until hello is fast. |

## 1.3 Install and hello (macOS host only)

On the **Mac** — host Terminal, **not** the Ubuntu VM:

1. Install from [ollama.com/download](https://ollama.com/download). Open **Ollama** once so the menu-bar app is running.
2. Pull and run:

```bash
ollama pull qwen2.5:7b
ollama run qwen2.5:7b "Say hello in one word"
```

You want a single word (or a short line) in a few seconds, not a multi-minute crawl.

3. See what is installed:

```bash
ollama ls
```

You want a row for **qwen2.5:7b** (size on the order of **4–5 GB**). `ls` is the disk catalog. `ps` (next) is what is **loaded** right now.

4. Optional — pull a small set for [chapter 3](03-n8n-uses-ollama.md) / [chapter 4](04-openclaw-uses-ollama.md) so you are not waiting on downloads later. Skip any tag that will not fit next to the Ubuntu VM.

| Tag | Later | Notes |
| --- | --- | --- |
| `qwen2.5:7b` | OpenClaw chat / tools; n8n HTTP | **Required** for this chapter. 7B-class, tool-friendly. |
| `llama3.1:8b` | Same roles, second chat brain | Alternate 7B-class if Qwen misbehaves. |
| `llama3.2:3b` | n8n smoke, cheap retries | Smaller, weaker at tools. Fine for “did n8n get a completion?” |
| `nomic-embed-text` | n8n embeddings / RAG | Not a chat model. Tiny. Pull if you will index text in n8n. |

```bash
ollama pull llama3.1:8b
ollama pull llama3.2:3b
ollama pull nomic-embed-text
ollama ls
```

Do **not** pull `gpt-oss:20b` / `qwen3.5:27b` as the default kit — they crowd the Mac next to the VM and make OpenClaw failover feel hung ([OpenClaw chapter 9](../openclaw-on-edgible/09-models-beyond-free-gemini.md)).

5. In another Terminal, while the 7B is loaded (or run the prompt again):

```bash
ollama ps
```

You want a **GPU** / Metal processor for `qwen2.5:7b`. **100% CPU** means this is not the Edgible GPU story — free RAM, quit other apps, or use a smaller tag only to debug install, then come back to 7B.

Leave Ollama’s default bind (**Mac localhost**). The VM still cannot reach it; that is [chapter 2](02-edgible-to-ollama.md).

### Verify

- [ ] Ollama is installed on **macOS**, not in the Ubuntu guest (`which ollama` on the Mac).
- [ ] `ollama run qwen2.5:7b "Say hello in one word"` replies.
- [ ] `ollama ls` shows **qwen2.5:7b** (plus any extras you chose).
- [ ] `ollama ps` shows **GPU** for the chat tag you ran.
- [ ] You did not change `OLLAMA_HOST` yet.
- [ ] Port **11434** is not forwarded on the router.

---

## Next

[2. Edgible publishes Ollama](02-edgible-to-ollama.md). Series: [README](README.md).
