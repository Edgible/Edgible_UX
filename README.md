# Edgible_UX

Tutorials and getting-started guides for [Edgible](https://edgible.com). This repo is documentation — not the OpenClaw skill, and not the Edgible CLI.

The OpenClaw skill (`/skill edgible`) lives in **[openclaw-edgible](https://github.com/Edgible/openclaw-edgible)**. How to install and check it: [5. OpenClaw skill for the Edgible CLI](guides/openclaw-on-edgible/05-edgible-openclaw-skill.md). Do not copy skill folders from this repo.

Three guides. Guides 1 and 2 publish the app from the box that runs it ([Edgible on an Ubuntu VM](guides/openclaw-on-edgible/01-edgible-on-vm.md) is the shared Hello World, not “start OpenClaw”). Guide 3 is the **remote caller**: Ollama stays on one home machine; n8n and OpenClaw on **other** self-hosted VMs call it. Telegram / WhatsApp are OpenClaw chat doors, not Edgible apps, and not an n8n chapter.

- **1. n8n on Edgible** — publishing plus **per-app auth**: one process, **org** editor, **None** webhook hostname.
- **2. OpenClaw on Edgible** — Control UI on `https://` with **org**, from a phone, no port-forward and no mesh VPN on the laptop.
- **3. LLM on Edgible** — self-hosted Ollama (GPU on the Mac), published **api-key**, called from a **remote** self-hosted n8n or OpenClaw VM.

## Contents

- [1. n8n on Edgible](guides/n8n-on-edgible/README.md) — six chapters (org editor, None webhooks, cron, smoke GET, teardown). Need the VM first; this series does not use OpenClaw.
- [2. OpenClaw on Edgible](guides/openclaw-on-edgible/README.md) — ten short chapters (VM + Edgible → OpenClaw → Control UI → public page → skill → Telegram → WhatsApp → Cursor → models → teardown). Skip the VM chapter if you already did it for n8n.
- [3. LLM on Edgible](guides/llm-on-edgible/README.md) — publish a self-hosted Ollama; **remote** n8n (`/v1`) and OpenClaw (native API) call it with Bearer.
