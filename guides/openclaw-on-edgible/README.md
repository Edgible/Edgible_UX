# OpenClaw on Edgible — chapters

Each chapter is one job and one smoke test. Do them in order.

**How to read a chapter:** one-line hook under the title, then **N.1 The job** (what you’ll do, how you’ll know, what you need, what this is not). Steps after that. **Next** at the end.

**OpenClaw** chats and uses tools on a box you own. **Edgible** is the public `https://<app>.<org>.edgible.com` door (outbound 443 only — no port-forward, no Tailscale). Telegram / WhatsApp are chat doors; they are not Edgible apps.

| # | Chapter | Smoke test |
| --- | --- | --- |
| 1 | [1. VM and Edgible](01-edgible-on-vm.md) | `edgible whoami` on the VM; Hello World on a **phone (cellular)** |
| 2 | [2. OpenClaw on this box](02-openclaw-on-the-box.md) | `openclaw agent … hello`; local Control UI (`openclaw dashboard`) if the guest has a desktop |
| 3 | [3. Publish Control UI](03-publish-openclaw-control-ui.md) | Phone opens `openclaw-ui.<org>.edgible.com` (**org** auth), chat works |
| 4 | [4. OpenClaw changes the Edgible site](04-openclaw-changes-edgible-site.md) | Control UI rewrites Hello World; optional hourly On this day |
| 5 | [5. Edgible skill](05-edgible-openclaw-skill.md) | VM `edgible whoami` and Control UI `/skill edgible whoami` |
| 6 | [6. Telegram](06-telegram-pocket-client.md) | DM **your** bot; `/skill edgible whoami` |
| 7 | [7. WhatsApp](07-whatsapp-pocket-client.md) | Linked device `hello` with `[OpenClaw]`; optional ACP `--bind here` |
| 8 | [8. Cursor Agent](08-cursor-agent.md) | `/acp doctor` then spawn; Control UI uses steer; WhatsApp can bind |

Do **not** use `! edgible whoami` as the OpenClaw check in chapter 2. That is **host bash** (`commands.bash`), off by default, and needs elevated allowlists. Chapter 5 is `/skill edgible whoami`. Chapter 6 can enable `!` if you want a host shell from Telegram.

The skill source is [openclaw-edgible](https://github.com/Edgible/openclaw-edgible), not this repo.
