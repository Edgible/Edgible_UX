# What Edgible does — and where these guides prove it

**One page.** Every claim below is demonstrated by a numbered chapter with its own smoke test, so nothing here is a slide-only feature.

The problem Edgible solves: you have something running on a box you own — a workflow runner, an AI agent, a GPU with a model on it — and you need people or machines on the internet to reach it, safely, without turning your home network into an attack surface. The usual answers all cost something. Port-forwarding puts a credential store on the open internet. A mesh VPN means enrolling every device that will ever need access. A reverse proxy plus certbot plus dynamic DNS means you now operate TLS and a domain. Edgible replaces all three: the box dials **out** on TCP 443, and a public HTTPS hostname appears with a certificate already on it and a lock already in front of it.

## The three differentiators

**1. The door opens outward.** The serving agent holds an outbound 443 connection. NAT is enough, nothing dials in, and no router configuration ever happens. Every chapter's verify list ends with a line confirming the app's port is *still* not forwarded — that is the point being made twenty-three times. Proven in [OpenClaw 1](guides/openclaw-on-edgible/01-edgible-on-vm.md), where the honest test is a phone with Wi‑Fi off loading your page over cellular.

**2. Auth is a property of the hostname, not an afterthought.** Each app carries its own lock, chosen at creation: **org** (only your organisation gets past a browser login), **api-key** (a bearer secret for machines that cannot log in), or **None** (open, for genuinely public endpoints). This is the primitive the whole product rests on, and it is why you never end up choosing between "locked and useless" and "working and exposed".

**3. One process, many doors, many locks.** Because auth attaches to the hostname rather than the path, the same running service can be published twice with different protection. This is the demo that lands hardest: n8n's editor holds your credentials and every workflow, so it stays **org** — while Stripe and GitHub, which cannot complete a browser login, hit a *second* hostname on **None**. One container, port 5678, two doors. Proven in [n8n 2](guides/n8n-on-edgible/02-n8n-editor-through-edgible.md) and [n8n 3](guides/n8n-on-edgible/03-n8n-webhook-door.md).

## Feature, benefit, and where it is demonstrated

Read **How** as the observable proof — the thing you watch happen, not the thing we assert.

| Feature | Benefit | Where | How |
| --- | --- | --- | --- |
| Public HTTPS with no inbound port | No hole in the router | [OpenClaw 1](guides/openclaw-on-edgible/01-edgible-on-vm.md) | Your page loads on a phone with **Wi‑Fi off**, while the app's port stays unforwarded |
| A certificate per hostname, issued for you | Never operate TLS | [n8n 2](guides/n8n-on-edgible/02-n8n-editor-through-edgible.md) | The console reports the certificate issued before you first open the URL |
| **org** auth | Keep the agent private | [OpenClaw 3](guides/openclaw-on-edgible/03-publish-openclaw-control-ui.md) | Your agent's Control UI opens on a phone while its Gateway never leaves loopback |
| **None** auth | Let webhooks in | [n8n 5](guides/n8n-on-edgible/05-n8n-public-webhook.md) | A stranger's GET from off your network returns your workflow's JSON |
| **api-key** auth | Secure Ollama | [LLM 2](guides/llm-on-edgible/02-edgible-to-ollama.md) | Off-LAN `curl` with a bearer secret returns model tags; without it, **401** |
| Two locks on one process | Protect the credential store | [n8n 3](guides/n8n-on-edgible/03-n8n-webhook-door.md) | One container on 5678: the editor hostname demands a login, the hooks hostname does not |
| API key create, list, revoke | Cut off a caller | [LLM 2](guides/llm-on-edgible/02-edgible-to-ollama.md) | The secret prints once, the key **id** is visibly not the secret, and a revoked key stops working |
| Device registration and health | Trust the box first | [OpenClaw 1](guides/openclaw-on-edgible/01-edgible-on-vm.md) | The device appears in your org and reports **Health check OK** in about 15 seconds |
| Publishes software you did not write | Publish stock apps | [LLM 2](guides/llm-on-edgible/02-edgible-to-ollama.md) | Stock Ollama, unmodified, goes public behind a bearer secret |
| CLI, console and wizard parity | Repeatable setup | [n8n 2](guides/n8n-on-edgible/02-n8n-editor-through-edgible.md) | The same app is created either from flags or from interactive prompts |
| Clean unpublish | Reversible demo | [n8n 6](guides/n8n-on-edgible/06-n8n-teardown.md), [OpenClaw 10](guides/openclaw-on-edgible/10-openclaw-teardown.md) | The hostnames go dead on cellular while neighbouring apps keep serving |
| Many apps on one box, each with its own lock | One box, mixed estate | [LLM 3](guides/llm-on-edgible/03-n8n-uses-ollama.md) | `hello-world` on **None**, `n8n` on **org** and `ollama` on **api-key**, all serving at once |

## The three set-piece demos

**A workflow platform with a public webhook and a private canvas.** [Guide 1](guides/n8n-on-edgible/README.md) — the auth split, end to end, including the `WEBHOOK_URL` subtlety that makes n8n *print* the public origin while traffic still lands on one process.

**An AI agent you reach from your phone.** [Guide 2](guides/openclaw-on-edgible/README.md) — the Gateway never leaves loopback; the phone gets in through **org**. The agent then edits a live public page in [chapter 4](guides/openclaw-on-edgible/04-openclaw-changes-edgible-site.md), and [chapter 5](guides/openclaw-on-edgible/05-edgible-openclaw-skill.md) teaches it to drive the Edgible CLI itself — the platform operating the platform.

**A self-hosted GPU serving two other self-hosted machines.** [Guide 3](guides/llm-on-edgible/README.md) — Ollama and the weights stay on one machine; n8n on a second and OpenClaw on a third call it over HTTPS with a bearer secret. No port-forward, no mesh VPN, and the GPU never leaves the room it is in. This is the combination that shows the whole model at once: private inference, machine auth, and remote self-hosted callers.

## What it replaces

Port-forwarding and the firewall rules around it. Dynamic DNS. Certbot and renewal cron. A hand-rolled nginx or Caddy reverse proxy. Mesh VPN enrolment for every client device. Ad-hoc tunnels that change URL on restart and cannot express "this hostname needs a login and that one does not".

## Known limits, stated plainly

Worth keeping visible, because each is something a reader will otherwise discover mid-chapter:

- **No macOS serving agent yet.** [Guide 3](guides/llm-on-edgible/README.md) works around it: Ollama runs on the Mac for the GPU, and an Ubuntu guest publishes it over a loopback forwarder. When a macOS agent ships, that hop disappears.
- **TLS terminates on the serving device**, so the gateway cannot inject HTTP headers. The practical consequence is that the original client IP does not reach the app, which breaks visitor geolocation in analytics tools. PROXY protocol between gateway and device would close this.
- **WebSocket-heavy apps** deserve a check on first publish; [n8n 2](guides/n8n-on-edgible/02-n8n-editor-through-edgible.md) tells the reader what a shell-loads-but-canvas-stays-blank failure means rather than pretending it cannot happen.

---

Start at the [README](README.md) for reading order, or go straight to [1. n8n on Edgible](guides/n8n-on-edgible/README.md).
