# LLM on Edgible: chapters

**Private AI: the prompts, the documents and the weights never leave hardware you own.**

Every prompt sent to a hosted model is a document handed to somebody else's logs, which is why the interesting questions are the ones people will not type into one. A GPU at home answers those, and the usual catch is that only the machine holding the GPU can use it. Here it answers over HTTPS to other machines you own, authenticated by a bearer secret rather than a port left open, and the weights stay where they were downloaded.

![An n8n VM and an OpenClaw VM on other machines call ollama.<org>.edgible.com with a bearer key. It arrives at Ollama on the Mac, bound to 0.0.0.0:11434 and published by the serving agent on that Mac, so the model weights and the GPU stay home and the router has no forwarded port.](../../images/diagrams/llm-on-edgible-light.svg#only-light)
![An n8n VM and an OpenClaw VM on other machines call ollama.<org>.edgible.com with a bearer key. It arrives at Ollama on the Mac, bound to 0.0.0.0:11434 and published by the serving agent on that Mac, so the model weights and the GPU stay home and the router has no forwarded port.](../../images/diagrams/llm-on-edgible-dark.svg#only-dark)

The use case: a self-hosted LLM on one home machine, called from a different self-hosted machine (n8n, OpenClaw, `curl`, Chatbox). Weights and GPU stay on the machine that runs the model. The remote box only sends HTTPS + `Authorization: Bearer`. No port-forward, no mesh VPN, no putting n8n or OpenClaw on the GPU box.

That is why the auth mode is `api-key` on `https://<app>.<org>.edgible.com`: zero-DNS publish for the inference hostname, with no DNS step (see [Glossary](../../glossary.md)). With `None`, anyone on the internet could run inference on your GPU. `org` is a human browser login, which a workflow or Gateway cannot complete. A same-LAN `http://<mac-ip>:11434` is not this use case.

A full private AI estate mixes auth modes: inference stays `api-key` here; automation that needs webhooks uses split-surface publish on n8n in [n8n on Edgible](../n8n-on-edgible/README.md) (editor `org`, hooks `None`); agent UIs stay `org` in [OpenClaw on Edgible](../openclaw-on-edgible/README.md). Ollama itself is one locked surface, not two hostnames on the same port.

## Pattern

The serving agent runs on the Mac, on the same machine as Ollama. Chapter 2 sets `OLLAMA_HOST` to `0.0.0.0:11434` and creates an existing app on that port. n8n and OpenClaw each run on a different VM, on a different home computer, and call the published hostname.

| Machine | OS | You run |
| --- | --- | --- |
| Mac | macOS | Ollama.app, `launchctl setenv OLLAMA_HOST`, serving agent under your account, `edgible app create existing` on port `11434` |
| Other home PC | n8n’s VM | n8n + `n8n-sandbox` ([chapter 3](03-n8n-uses-ollama.md)) |
| Other home PC | OpenClaw’s VM | Gateway / Control UI ([chapter 4](04-openclaw-uses-ollama.md)) |

Do not install Ollama on the n8n or OpenClaw VM. Do not point those VMs at the Mac’s LAN address on `11434`. Do not port-forward `11434` on the router. n8n and OpenClaw use the published `api-key` URL.

## Chapters

Each chapter is one job and one smoke test. Do them in order. Chapters 1 to 4 are the demo; [5](05-llm-teardown.md) removes the published hostname, revokes the secret and puts the Mac back on loopback.

**How to read a chapter:** a one-line hook under the title, then **N.0 Why** (what is missing without this chapter, and which machine you run it on), then **N.1 The job** (what you’ll do, how you’ll know, what you need, what this is not). Steps after that, a **Verify** checklist that mirrors *Done when*, and **Next** at the end.

**Need first:** the Edgible CLI on the Mac, logged in, and a serving agent on that Mac. [Chapter 2](02-edgible-to-ollama.md) installs the agent under your account if it is not already healthy. [n8n on Edgible](../n8n-on-edgible/README.md) and [OpenClaw on Edgible](../openclaw-on-edgible/README.md) are how you publish those apps from their own VMs.

| # | Chapter | Smoke test |
| --- | --- | --- |
| 1 | [1. Ollama on bare metal](01-ollama-on-bare-metal.md) | Mac `ollama run` replies; `ollama ls` lists the tag; `ollama ps` shows GPU |
| 2 | [2. Edgible publishes Ollama](02-edgible-to-ollama.md) | Cellular `curl` with Bearer; optional [Chatbox](02-edgible-to-ollama.md#25-optional-a-real-chat-ui-not-curl) on the Mac |
| 3 | [3. n8n uses that URL](03-n8n-uses-ollama.md) | Use case 1: workflow on `qwen2.5:7b` (thinking off). Use case 2: Assistant `gpt-oss:20b` + sandbox + SearXNG; Hello, then edgible.com / n8n summary |
| 4 | [4. OpenClaw uses that URL](04-openclaw-uses-ollama.md) | OpenClaw `ollama/gpt-oss:20b` via Edgible `api-key` (no `/v1`); agent hello, then a code change |
| 5 | [5. Tear down the published LLM](05-llm-teardown.md) | The old Bearer token fails from cellular; nothing on `11434`; Mac back on loopback |

OpenClaw chapter 8 is cloud keys plus optional same-LAN Ollama (Gateway next to the Mac). If the Gateway is on another home VM, skip 8.5 LAN and use [chapter 4](04-openclaw-uses-ollama.md). n8n stays editor `org` and webhook `None` on its own VM. The published inference URL lives here.
