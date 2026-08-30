# LLM on Edgible: chapters

Each chapter is one job and one smoke test. Do them in order. Chapters 1 to 4 are the demo; [5](05-llm-teardown.md) removes the published hostname, revokes the secret and puts the Mac back on loopback.

How to read a chapter: a one-line hook under the title, then N.0 Why (what is missing without this chapter, and which machine you run it on), then N.1 The job (what you’ll do, how you’ll know, what you need, what this is not). Steps after that, a **Verify** checklist that mirrors *Done when*, and **Next** at the end.

The use case: a self-hosted LLM on one home machine, called from a different self-hosted machine (n8n, OpenClaw, `curl`, Chatbox). Weights and GPU stay on the machine that runs the model. The remote box only sends HTTPS + `Authorization: Bearer`. No port-forward, no mesh VPN, no putting n8n or OpenClaw on the GPU box.

That is why the auth mode is `api-key` on `https://<app>.<org>.edgible.com`. With `None`, anyone on the internet could run inference on your GPU. `org` is a human browser login, which a workflow or Gateway cannot complete. Same-LAN `http://192.168.64.1:11434` is only the UTM guest talking to the Mac; it is not this use case.

## Pattern (for the time being)

The serving agent does not run on macOS yet. Ollama stays on the Mac (Metal / GPU). The Ubuntu guest (UTM) only publishes it (and the website). n8n and OpenClaw each run on a different VM, on a different home computer.

| Machine | OS | You run |
| --- | --- | --- |
| Mac host | macOS | Ollama.app, `ollama …`, `launchctl`, `open -a`, `lsof` |
| Mac guest | Ubuntu in UTM | `edgible …`, socat forwarder, website; not n8n, not OpenClaw |
| Other home PC | n8n’s VM | n8n + `n8n-sandbox` ([chapter 3](03-n8n-uses-ollama.md)) |
| Other home PC | OpenClaw’s VM | Gateway / Control UI ([chapter 4](04-openclaw-uses-ollama.md)) |

Do not install Ollama in the UTM guest. Do not run `launchctl` / `open -a Ollama` in Ubuntu; those are macOS-only. Do not point n8n or OpenClaw at UTM `192.168.64.1` / `$HOST:11434` from the other computer.

Edgible cannot aim at the Mac’s IP. It proxies `127.0.0.1` on the UTM guest. Chapter 2 puts a loopback forwarder there so that port is Ollama on the Mac. When a macOS agent exists, this hop can go away.

Do not port-forward `11434` on the router. Same-LAN HTTP is only the guest → Mac hop for the forwarder. n8n and OpenClaw use the published `api-key` URL.

**Need first:** [Edgible on an Ubuntu VM](../start-here/01-edgible-on-vm.md) on the Mac guest (`mini-pc`, Hello World on cellular). Leave that VM and `hello-world` running. [n8n on Edgible](../n8n-on-edgible/README.md) and [OpenClaw on Edgible](../openclaw-on-edgible/README.md) are how you publish those apps from their own VMs, not from the Mac.

| # | Chapter | Smoke test |
| --- | --- | --- |
| 1 | [1. Ollama on bare metal](01-ollama-on-bare-metal.md) | Mac `ollama run` replies; `ollama ls` lists the tag; `ollama ps` shows GPU |
| 2 | [2. Edgible publishes Ollama](02-edgible-to-ollama.md) | Cellular `curl` with Bearer; optional [Chatbox](02-edgible-to-ollama.md#26-optional-a-real-chat-ui-not-curl) on the Mac |
| 3 | [3. n8n uses that URL](03-n8n-uses-ollama.md) | Use case 1: workflow on `qwen2.5:7b` (thinking off). Use case 2: Assistant `gpt-oss:20b` + sandbox + SearXNG; Hello, then edgible.com / n8n summary |
| 4 | [4. OpenClaw uses that URL](04-openclaw-uses-ollama.md) | OpenClaw `ollama/gpt-oss:20b` via Edgible `api-key` (no `/v1`); agent hello, then a code change |
| 5 | [5. Tear down the published LLM](05-llm-teardown.md) | The old Bearer token fails from cellular; nothing on `11434`; Mac back on loopback |

OpenClaw chapter 8 is cloud keys plus optional same-LAN Ollama (Gateway next to the Mac). If the Gateway is on another home VM, skip 8.5 LAN and use [chapter 4](04-openclaw-uses-ollama.md). n8n stays editor `org` and webhook `None` on its own VM. The published inference URL lives here.
