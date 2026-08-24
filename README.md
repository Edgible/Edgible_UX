# Edgible_UX

Tutorials and getting-started guides for [Edgible](https://edgible.com). This repo is documentation and UX rehearsal — not the OpenClaw skill, and not the Edgible CLI.

The OpenClaw skill (`/skill edgible`) lives in **[openclaw-edgible](https://github.com/Edgible/openclaw-edgible)**. Install it from that repo (`git:Edgible/openclaw-edgible`). Do not copy skill folders from here.

## Contents

- [OpenClaw on Edgible — Getting started](guides/openclaw-on-edgible/01-invite-through-edgible-on-vm.md) — invite email through Edgible on an Ubuntu 24.04 VM (VirtualBox or UTM): Hello World, model, Control UI, public page, optional Cursor/WhatsApp.
- [Telegram as the pocket client](guides/openclaw-on-edgible/02-telegram-pocket-client.md) — BotFather bot, Gateway token, pairing, `/whoami` vs `/skill edgible`, model fallback. Telegram dials out; it is not an Edgible app.
- [Early-access UX simulation](canvases/edgible-beta-ux-simulation.canvas.tsx) — plan for rehearsing invited-beta first-run.

The `.canvas.tsx` file is the git copy. In Cursor it also live-renders as a canvas beside chat when opened from Cursor’s managed canvases folder (`Cmd+P`, then `edgible-beta-ux-simulation`).
