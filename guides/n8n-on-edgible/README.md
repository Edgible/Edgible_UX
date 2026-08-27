# n8n on Edgible — chapters

**Guide 1.** Each chapter is one job and one smoke test. Do them in order.

**How to read a chapter:** one-line hook under the title, a short **why** (the auth split), then **N.1 The job** (what you’ll do, how you’ll know, what you need, what this is not). Steps after that. **Next** at the end.

**n8n** runs workflows on a box you own (webhooks, cron, glue between APIs). **Edgible** is the public `https://<app>.<org>.edgible.com` door (outbound 443 only — no port-forward, no mesh VPN). This series does **not** use OpenClaw.

This is the demo of **internet publishing** and **per-app auth**. n8n is **one** process on loopback **5678**. Edgible publishes it as **two** apps: **n8n** (**org**) is the editor; **n8n-hooks** (**None**) is the inbound door. Auth is a property of the hostname, not of a path. Without that split you either lock the webhooks (GitHub never gets in) or you unlock the canvas (anyone who finds the host gets the editor). Chapters 1–5 are the demo; [6](06-n8n-teardown.md) is teardown. Control UI is [2. OpenClaw on Edgible](../openclaw-on-edgible/README.md). A **remote** self-hosted n8n calling a **self-hosted** Ollama on another machine — workflow on **`qwen2.5:7b`** (thinking off), **AI Assistant** chat on a **thinking** tag (**`gpt-oss:20b`**), sandbox on that same n8n VM — is [3. LLM on Edgible](../llm-on-edgible/README.md).

**Need first:** [Edgible on an Ubuntu VM](../openclaw-on-edgible/01-edgible-on-vm.md) (serving device `mini-pc`, Hello World on the phone). That file is OpenClaw’s chapter 1 on disk; after Hello World, come here instead of installing OpenClaw. Leave **hello-world** running.

| # | Chapter | Smoke test |
| --- | --- | --- |
| 1 | [1. n8n on the VM](01-n8n-on-the-vm.md) | `curl http://127.0.0.1:5678/` on the guest; n8n is not on the internet |
| 2 | [2. n8n editor through Edgible](02-n8n-editor-through-edgible.md) | Phone (cellular) opens `n8n.<org>.edgible.com` (**org**), canvas loads |
| 3 | [3. Public webhook door](03-n8n-webhook-door.md) | `n8n-hooks.<org>.edgible.com` exists; n8n `WEBHOOK_URL` is that origin |
| 4 | [4. A cron workflow](04-n8n-cron.md) | Active schedule writes an **Executions** row (no inbound URL) |
| 5 | [5. A webhook a stranger can hit](05-n8n-public-webhook.md) | Cellular (or off-LAN) GET/POST to the **hooks** production URL returns JSON |
| 6 | [6. Tear down n8n](06-n8n-teardown.md) | **n8n** and **n8n-hooks** gone; nothing on **5678**; OpenClaw / ollama / serving agent left unless you opt in |

Next guides: [2. OpenClaw on Edgible](../openclaw-on-edgible/README.md), [3. LLM on Edgible](../llm-on-edgible/README.md).
