# Edgible_UX

Tutorials and getting-started guides for [Edgible](https://edgible.com). This repo is documentation. It is not the OpenClaw skill, and not the Edgible CLI.

The OpenClaw skill (`/skill edgible`) lives in [openclaw-edgible](https://github.com/Edgible/openclaw-edgible). To install and check it, see [5. OpenClaw skill for the Edgible CLI](guides/openclaw-on-edgible/05-edgible-openclaw-skill.md). Do not copy skill folders from this repo.

There are three guides. Guides 1 and 2 publish an app from the machine that runs it; [Edgible on an Ubuntu VM](guides/openclaw-on-edgible/01-edgible-on-vm.md) is the shared Hello World chapter for all three series, not the start of OpenClaw. Guide 3 covers the remote caller case: Ollama stays on one home machine, and n8n and OpenClaw on other self-hosted VMs call it. Telegram and WhatsApp are OpenClaw chat clients, not Edgible apps, and not an n8n chapter.

- **1. n8n on Edgible.** Publishing plus per-app auth: one process, an `org` editor and a `None` webhook hostname.
- **2. OpenClaw on Edgible.** Control UI over HTTPS with `org`, from a phone, with no port-forward and no mesh VPN on the laptop.
- **3. LLM on Edgible.** Self-hosted Ollama with the GPU on the Mac, published with `api-key`, called from a remote self-hosted n8n or OpenClaw VM.

For a one-page summary, [What Edgible does, and where these guides prove it](capabilities.md) maps each feature to the chapter that demonstrates it.

## Contents

- [1. n8n on Edgible](guides/n8n-on-edgible/README.md). Six chapters: `org` editor, `None` webhooks, cron, smoke GET, teardown. Set up the VM first. This series does not use OpenClaw.
- [2. OpenClaw on Edgible](guides/openclaw-on-edgible/README.md). Ten short chapters: VM and Edgible, OpenClaw, Control UI, public page, skill, Telegram, WhatsApp, Cursor, models, teardown. Skip the VM chapter if you already did it for n8n.
- [3. LLM on Edgible](guides/llm-on-edgible/README.md). Publish a self-hosted Ollama, then call it from a remote n8n (`/v1`) and OpenClaw (native API) with a bearer secret.
