# What Edgible does, and where these guides prove it

Edgible publishes a service running on a machine you own at a public HTTPS hostname, using only an outbound connection on TCP 443. The alternatives each cost something. Port-forwarding exposes the service, and anything it holds, to the open internet. A mesh VPN requires enrolling every device that will ever need access. A reverse proxy with certbot and dynamic DNS means you operate TLS and a domain yourself. With Edgible the machine dials out, and a hostname appears with a certificate already issued and an auth mode already applied.

## The three differentiators

**1. The connection is outbound only.** The serving agent holds an outbound 443 connection, so NAT is sufficient and no router configuration is required. Every chapter's verify list ends by confirming the app's port is still not forwarded. Demonstrated in [Start here](guides/start-here/01-edgible-on-vm.md), where the test is a phone with Wi‑Fi off loading the page over cellular.

**2. Auth is a property of the hostname.** Each app carries an auth mode, chosen when you create it: `org` restricts access to your organisation behind a browser login, `api-key` accepts a bearer secret from machines that cannot log in, and `None` is open. Auth attaches to the app, not to a path inside it.

**3. One process can have several hostnames with different auth modes.** Because auth attaches to the hostname, the same running service can be published more than once with different protection. n8n's editor holds credentials and every workflow, so it stays `org`. Stripe and GitHub cannot complete a browser login, so they call a second hostname on `None`. One container on port 5678, two hostnames. Demonstrated in [n8n 2](guides/n8n-on-edgible/02-n8n-editor-through-edgible.md) and [n8n 3](guides/n8n-on-edgible/03-n8n-webhook-door.md).

## Feature, benefit, and where it is demonstrated

Where names the chapter that demonstrates the feature. How is the observable proof: what you watch happen.

| Feature | Benefit | Where | How |
| --- | --- | --- | --- |
| Public HTTPS with no inbound port | No inbound port to attack | [Start here](guides/start-here/01-edgible-on-vm.md) | Loads on a phone with Wi‑Fi off |
| A certificate per hostname, issued for you | Never operate TLS | [n8n 2](guides/n8n-on-edgible/02-n8n-editor-through-edgible.md) | Console shows the certificate issued |
| `org` auth | Keep the agent private | [OpenClaw 3](guides/openclaw-on-edgible/03-publish-openclaw-control-ui.md) | Phone opens the UI; Gateway on loopback |
| `None` auth | Accept webhook callers | [n8n 5](guides/n8n-on-edgible/05-n8n-public-webhook.md) | An off-network GET returns JSON |
| `api-key` auth | Secure Ollama | [LLM 2](guides/llm-on-edgible/02-edgible-to-ollama.md) | Bearer `curl` works; without it, `401` |
| Two auth modes on one process | Protect the credential store | [n8n 3](guides/n8n-on-edgible/03-n8n-webhook-door.md), [Website 4](guides/website-on-edgible/04-publish-umami.md) | Editor asks for login; hooks does not |
| A static site published from your own disk | No web host, no rented box | [Website 2](guides/website-on-edgible/02-publish-the-site.md) | A phone on cellular loads files from your machine |
| API key create, list, revoke | Cut off a caller | [LLM 2](guides/llm-on-edgible/02-edgible-to-ollama.md) | Secret prints once; revoked key fails |
| Device registration and health | Confirm the machine is connected | [Start here](guides/start-here/01-edgible-on-vm.md) | **Health check OK** in about 15 seconds |
| Publishes software you did not write | Publish stock apps | [LLM 2](guides/llm-on-edgible/02-edgible-to-ollama.md) | Stock Ollama, unmodified, goes public |
| CLI, console and wizard parity | Repeatable setup | [n8n 2](guides/n8n-on-edgible/02-n8n-editor-through-edgible.md) | Same app from flags or prompts |
| Clean unpublish | Reversible demo | [n8n 6](guides/n8n-on-edgible/06-n8n-teardown.md), [OpenClaw 10](guides/openclaw-on-edgible/10-openclaw-teardown.md) | Hostnames dead; other apps still serving |
| Many apps on one machine, each with its own auth mode | One machine, mixed estate | [LLM 3](guides/llm-on-edgible/03-n8n-uses-ollama.md) | `None`, `org` and `api-key` at once |

## The set-piece demos

**A marketing site with analytics and monitoring, all self-hosted.** [Website on Edgible](guides/website-on-edgible/README.md) publishes four hostnames off one machine: the site on `None`, the Umami tracking script on `None`, and the Umami and Uptime Kuma interfaces on `org`. It is the shortest demonstration that the access rule belongs to the hostname rather than to the service.

**A workflow platform with a public webhook and a private canvas.** [n8n on Edgible](guides/n8n-on-edgible/README.md) covers the auth split end to end, including the `WEBHOOK_URL` setting that makes n8n print the public origin while traffic still reaches one process.

**An AI agent reachable from a phone.** [OpenClaw on Edgible](guides/openclaw-on-edgible/README.md) keeps the Gateway on loopback and lets the phone in through `org`. The agent edits a live public page in [chapter 4](guides/openclaw-on-edgible/04-openclaw-changes-edgible-site.md), and [chapter 5](guides/openclaw-on-edgible/05-edgible-openclaw-skill.md) installs a skill that lets it run the Edgible CLI.

**A self-hosted GPU serving two other self-hosted machines.** In [LLM on Edgible](guides/llm-on-edgible/README.md), Ollama and the model weights stay on one machine while n8n on a second and OpenClaw on a third call it over HTTPS with a bearer secret. No port-forward and no mesh VPN. This combination exercises private inference, machine authentication and remote self-hosted callers together.

## What it replaces

Port-forwarding and the firewall rules around it. Dynamic DNS. Certbot and renewal cron. A hand-rolled nginx or Caddy reverse proxy. Mesh VPN enrolment for every client device. Ad-hoc tunnels that change URL on restart and cannot give one hostname a login and another none.

## Known limits

- **No macOS serving agent yet.** [LLM on Edgible](guides/llm-on-edgible/README.md) works around this: Ollama runs on the Mac for GPU access, and an Ubuntu guest publishes it through a loopback forwarder. A macOS agent would remove that hop.
- **TLS terminates on the serving device**, so the gateway cannot inject HTTP headers. The original client IP therefore does not reach the app, which breaks visitor geolocation in analytics tools. [Website 4.5](guides/website-on-edgible/04-publish-umami.md#45-what-the-country-column-will-not-tell-you) shows the empty country column and proves the cause. PROXY protocol between gateway and device would close this gap.
- **WebSocket-heavy apps** should be checked on first publish. [n8n 2](guides/n8n-on-edgible/02-n8n-editor-through-edgible.md) describes what it means when the page shell loads but the canvas stays blank.

---

Start at [Welcome](README.md) for where to begin, or go straight to [Start here](guides/start-here/README.md).
