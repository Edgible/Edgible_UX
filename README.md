# Edgible_UX

Tutorials and getting-started guides for [Edgible](https://edgible.com). This repo is documentation — not the OpenClaw skill, and not the Edgible CLI.

The OpenClaw skill (`/skill edgible`) lives in **[openclaw-edgible](https://github.com/Edgible/openclaw-edgible)**. How to install and check it: [5. OpenClaw skill for the Edgible CLI](guides/openclaw-on-edgible/05-edgible-openclaw-skill.md). Do not copy skill folders from this repo.

Three guides. Same box from [Edgible on an Ubuntu VM](guides/openclaw-on-edgible/01-edgible-on-vm.md) (that file lives in the OpenClaw folder; it is the shared Hello World, not “start OpenClaw”). Telegram / WhatsApp are OpenClaw chat doors, not Edgible apps, and not an n8n chapter.

- **1. n8n on Edgible** — publishing plus **per-app auth**: one process, **org** editor, **None** webhook hostname.
- **2. OpenClaw on Edgible** — Control UI on `https://` with **org**, from a phone, no port-forward and no mesh VPN on the laptop.
- **3. LLM on Edgible** — not written yet. Publish a local or remote model you control (**api-key**), then point n8n **and** OpenClaw at it. Do not do that hook-up in guides 1 or 2.

## Contents

- [1. n8n on Edgible](guides/n8n-on-edgible/README.md) — five chapters. Need the VM first; this series does not use OpenClaw.
- [2. OpenClaw on Edgible](guides/openclaw-on-edgible/README.md) — nine short chapters (VM + Edgible → OpenClaw → Control UI → public page → skill → Telegram → WhatsApp → Cursor → models). Skip the VM chapter if you already did it for n8n.
- [3. LLM on Edgible](guides/llm-on-edgible/README.md) — stub until the model answers on the serving box.
