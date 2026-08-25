# OpenClaw on Edgible — chapters

**Guide 2.** Each chapter is one job and one smoke test. Do them in order. If [1. n8n on Edgible](../n8n-on-edgible/README.md) already left Hello World up, skip [chapter 1](01-edgible-on-vm.md) and start at [chapter 2](02-openclaw-on-the-box.md).

**How to read a chapter:** one-line hook under the title, then **N.1 The job** (what you’ll do, how you’ll know, what you need, what this is not). Steps after that. **Next** at the end.

**OpenClaw** chats and uses tools on a box you own. **Edgible** is the public `https://<app>.<org>.edgible.com` door (outbound 443 only — no port-forward, no mesh VPN). The Edgible story here is the **Control UI**: phone browser, **org** login, no tunnel on the laptop. Telegram / WhatsApp are chat doors; they are not Edgible apps.

Publishing plus two locks on one process (editor **org**, webhooks **None**) is [1. n8n on Edgible](../n8n-on-edgible/README.md). Hooking n8n and OpenClaw to a **big** local or remote LLM you publish through Edgible is [3. LLM on Edgible](../llm-on-edgible/README.md) — not this series, not chapter 9.

| # | Chapter | Smoke test |
| --- | --- | --- |
| 1 | [1. Edgible on an Ubuntu VM](01-edgible-on-vm.md) | `edgible whoami` on the VM; Hello World on a **phone (cellular)** |
| 2 | [2. OpenClaw on the VM (loopback Gateway)](02-openclaw-on-the-box.md) | `openclaw agent … hello`; local Control UI (`openclaw dashboard`) if the guest has a desktop |
| 3 | [3. OpenClaw Control UI through Edgible](03-publish-openclaw-control-ui.md) | Phone opens `openclaw-ui.<org>.edgible.com` (**org** auth), chat works |
| 4 | [4. OpenClaw changes the public Edgible site](04-openclaw-changes-edgible-site.md) | Control UI rewrites Hello World; optional hourly On this day |
| 5 | [5. OpenClaw skill for the Edgible CLI](05-edgible-openclaw-skill.md) | VM `edgible whoami` and Control UI `/skill edgible whoami` |
| 6 | [6. Telegram pocket client for OpenClaw](06-telegram-pocket-client.md) | DM **your** bot; `/skill edgible whoami` |
| 7 | [7. WhatsApp linked device for OpenClaw](07-whatsapp-pocket-client.md) | Linked device `hello` with `[OpenClaw]`; optional ACP `--bind here` |
| 8 | [8. Cursor Agent from OpenClaw on the Edgible site](08-cursor-agent.md) | `/acp doctor` then spawn; Control UI uses steer; WhatsApp can bind |
| 9 | [9. Models beyond free Gemini](09-models-beyond-free-gemini.md) | `openclaw agent --model … hello` on DeepSeek / Ollama / another key; optional fallbacks |

Do **not** use `! edgible whoami` as the OpenClaw check in chapter 2. That is **host bash** (`commands.bash`), off by default, and needs elevated allowlists. Chapter 5 is `/skill edgible whoami`. Chapter 6 can enable `!` if you want a host shell from Telegram.

The skill source is [openclaw-edgible](https://github.com/Edgible/openclaw-edgible), not this repo.

Workflows (webhooks and auth split, not an agent): [1. n8n on Edgible](../n8n-on-edgible/README.md) — same VM from [chapter 1](01-edgible-on-vm.md). A model you control, published for both products: [3. LLM on Edgible](../llm-on-edgible/README.md) (stub).
