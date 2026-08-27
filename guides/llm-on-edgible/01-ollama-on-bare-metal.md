# 1. Ollama on bare metal

**The model runs on the Mac, with the GPU. The VM does not see it yet.**

A UTM Ubuntu guest cannot use the Mac’s GPU. If you install Ollama *inside* the VM, you get CPU inference and you steal RAM from the guest. This chapter only proves Ollama on **macOS**. Edgible and the loopback forwarder are [chapter 2](02-edgible-to-ollama.md).

## 1.1 The job

You install Ollama on the Mac that hosts the Ubuntu VM, pull a 7B-class chat model, and run a one-line hello. You confirm the process is on **GPU** (Metal), not a slow CPU fall-through.

**Done when**

- `ollama run qwen2.5:7b "Say hello in one word"` prints a short reply on the **Mac** (Terminal or the Ollama app).
- `ollama ps` shows that model with a **GPU** processor (not 100% CPU).
- You did **not** install Ollama in the Ubuntu guest.
- Port **11434** is not forwarded on the router.

**Need first:** A Mac with enough RAM left **after** the Ubuntu VM: a **7B** wants on the order of **8 GB+** for weights. The VM from [Edgible on an Ubuntu VM](../openclaw-on-edgible/01-edgible-on-vm.md) can stay running; you do not use it in this chapter. [Ollama for Mac](https://ollama.com/download).

**Not this chapter:** `OLLAMA_HOST=0.0.0.0`, socat, an Edgible app, n8n, OpenClaw, or `curl` from the VM.

## 1.2 Words you'll use

| Word | Here |
| --- | --- |
| **Bare metal** | macOS on the MacBook (or Mac mini) — not the UTM guest. |
| **11434** | Ollama’s HTTP port. Default is **localhost on the Mac only**. |
| **Metal** | How Ollama uses the Mac GPU. The Ubuntu VM cannot do this. |
| **7B** | Size class for this smoke test (`qwen2.5:7b`). Bigger tags wait until hello is fast. |

## 1.3 Install and hello

On the **Mac** (host Terminal, not SSH into the VM):

1. Install from [ollama.com/download](https://ollama.com/download). Open **Ollama** once so the menu-bar app is running.
2. Pull and run:

```bash
ollama pull qwen2.5:7b
ollama run qwen2.5:7b "Say hello in one word"
```

You want a single word (or a short line) in a few seconds, not a multi-minute crawl.

3. In another Terminal, while that model is loaded (or run the prompt again):

```bash
ollama ps
```

You want a **GPU** / Metal processor for `qwen2.5:7b`. **100% CPU** means this is not the Edgible GPU story — free RAM, quit other apps, or use a smaller tag only to debug install, then come back to 7B.

Leave Ollama’s default bind (**Mac localhost**). The VM still cannot reach it; that is [chapter 2](02-edgible-to-ollama.md).

### Verify

- [ ] Ollama is installed on **macOS**, not in the Ubuntu guest (`which ollama` on the Mac).
- [ ] `ollama run qwen2.5:7b "Say hello in one word"` replies.
- [ ] `ollama ps` shows **GPU** for that tag.
- [ ] You did not change `OLLAMA_HOST` yet.
- [ ] Port **11434** is not forwarded on the router.

---

## Next

[2. Edgible publishes Ollama](02-edgible-to-ollama.md). Series: [README](README.md).
