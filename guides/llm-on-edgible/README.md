# LLM on Edgible — chapters

**Guide 3.** Each chapter is one job and one smoke test. Do them in order.

**How to read a chapter:** one-line hook under the title, a short **why**, then **N.1 The job** (what you’ll do, how you’ll know, what you need, what this is not). Steps after that. **Next** at the end.

**The model you control,** published as `https://<app>.<org>.edgible.com`, then n8n and OpenClaw call it. Auth is **api-key** (machines send `Authorization: Bearer`). Never **None** — that would let strangers burn the GPU. **org** is for a human UI on another hostname, not for `curl` / n8n / OpenClaw.

## Pattern (for the time being)

The serving agent does **not** run on macOS yet. Ollama on Apple Silicon (or a Mac GPU) must stay on **bare metal** or the guest will infer on CPU. So this series uses two processes on **one** Mac:

| Where | What | Why |
| --- | --- | --- |
| **Bare metal** (macOS) | Ollama | Metal / GPU. Weights never go in the VM. |
| **Ubuntu VM** (UTM, same Mac) | Edgible serving agent | Publishes a **local** port on the guest. Hello World already proved this box. |

Edgible cannot aim at the Mac’s IP. It proxies `127.0.0.1` **on the VM**. Chapter 2 puts a loopback forwarder on the guest so that port is Ollama on the host. When a macOS agent exists, this hop can go away.

Do **not** port-forward **11434** on the router. Same-LAN HTTP from the guest to the Mac is enough for the forwarder.

**Need first:** [Edgible on an Ubuntu VM](../openclaw-on-edgible/01-edgible-on-vm.md) (`mini-pc`, Hello World on cellular). Leave the VM and **hello-world** running. [1. n8n on Edgible](../n8n-on-edgible/README.md) and [2. OpenClaw on Edgible](../openclaw-on-edgible/README.md) can wait until chapters 3–4.

| # | Chapter | Smoke test |
| --- | --- | --- |
| 1 | [1. Ollama on bare metal](01-ollama-on-bare-metal.md) | Mac `ollama run` replies; `ollama ps` shows GPU, not a CPU-only crawl |
| 2 | [2. Edgible publishes Ollama](02-edgible-to-ollama.md) | VM loopback `curl` matches the Mac; cellular `curl` with Bearer hits `https://ollama.<org>…` (**api-key**, not **None**) |
| 3 | [3. n8n uses that URL](03-n8n-uses-ollama.md) | Not written yet |
| 4 | [4. OpenClaw uses that URL](04-openclaw-uses-ollama.md) | Not written yet |

OpenClaw chapter 9 stays cloud keys plus a **small** same-LAN Ollama failover (no Edgible app). n8n stays editor **org** and webhook **None**. The published inference URL lives here.
