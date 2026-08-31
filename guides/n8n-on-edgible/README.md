# n8n on Edgible: chapters

**The back office workhorse: the automation that runs at 3am, on a machine in your own building.**

Chasing an invoice, routing a form, moving a row from one system into another that was never meant to talk to it. This is the unglamorous work every business runs on, and it is usually handed to a hosted automation service along with the API keys to everything it touches. Here the credentials sit in a container on your machine, the canvas that holds them opens only to your organisation, and the one URL that strangers must reach is a separate hostname that reaches the same process.

![A phone and outside services reach two hostnames, one behind an org login and one open, both arriving at a single n8n process on loopback](../../images/diagrams/n8n-on-edgible-light.svg#only-light)
![A phone and outside services reach two hostnames, one behind an org login and one open, both arriving at a single n8n process on loopback](../../images/diagrams/n8n-on-edgible-dark.svg#only-dark)

n8n runs workflows on a box you own (webhooks, cron, glue between APIs). Edgible publishes it on a `https://<app>.<org>.edgible.com` hostname over outbound 443 only, with no port-forward and no mesh VPN. This series does not use OpenClaw.

This is the demo of internet publishing and per-app auth. n8n is one process on loopback `5678`. Edgible publishes it as two apps: n8n (`org`) is the editor; `n8n-hooks` (`None`) is the public endpoint for inbound calls. Auth is a property of the hostname, not of a path. Without that split you either set the webhook hostname to `org` (GitHub never gets in) or set the editor hostname to `None` (anyone who finds the host gets the canvas). Chapters 1 to 5 are the demo; [6](06-n8n-teardown.md) is teardown. Control UI is [OpenClaw on Edgible](../openclaw-on-edgible/README.md). A remote self-hosted n8n calling a self-hosted Ollama on another machine, with the workflow on `qwen2.5:7b` (thinking off), **AI Assistant** chat on a thinking tag (`gpt-oss:20b`), and the sandbox on that same n8n VM, is [LLM on Edgible](../llm-on-edgible/README.md).

Each chapter is one job and one smoke test. Do them in order.

**How to read a chapter:** a one-line hook under the title, then **N.0 Why** (what is missing without this chapter, and which machine you run it on), then **N.1 The job** (what you’ll do, how you’ll know, what you need, what this is not). Steps after that, a **Verify** checklist that mirrors *Done when*, and **Next** at the end.

**Need first:** [Start here](../start-here/README.md) (serving device `minipc`, Hello World on the phone). Leave `hello-world` running.

| # | Chapter | Smoke test |
| --- | --- | --- |
| 1 | [1. n8n on the VM](01-n8n-on-the-vm.md) | `curl http://127.0.0.1:5678/` on the guest; n8n is not on the internet |
| 2 | [2. n8n editor through Edgible](02-n8n-editor-through-edgible.md) | Phone (cellular) opens `n8n.<org>.edgible.com` (`org`), canvas loads |
| 3 | [3. Public webhook hostname](03-n8n-public-webhook-hostname.md) | `n8n-hooks.<org>.edgible.com` exists; n8n `WEBHOOK_URL` is that origin |
| 4 | [4. A cron workflow](04-n8n-cron.md) | Active schedule writes an **Executions** row (no inbound URL) |
| 5 | [5. A webhook a stranger can hit](05-n8n-public-webhook.md) | Cellular (or off-LAN) GET/POST to the hooks production URL returns JSON |
| 6 | [6. Tear down n8n](06-n8n-teardown.md) | n8n and `n8n-hooks` gone; nothing on `5678`; OpenClaw / ollama / serving agent left unless you opt in |

Next guides: [OpenClaw on Edgible](../openclaw-on-edgible/README.md), [LLM on Edgible](../llm-on-edgible/README.md).
