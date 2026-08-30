# Glossary

Every term these guides use, in one place. Chapters restate the parameters they depend on, so you should not need this page to follow one, but a term you meet halfway through is defined here.

## Edgible

| Term | What it means here |
| --- | --- |
| Serving agent | The daemon installed on the machine that runs your service. It holds an outbound connection on TCP 443 and proxies traffic to a local port. |
| Serving device | The registered record of that machine in the console, with a name such as `mini-pc` and a health state. Not interchangeable with serving agent. |
| App | One published hostname pointing at one local port, with one auth mode. A single process can be published as several apps. |
| Published hostname | The public HTTPS address an app answers on, in the form `<app>.<org>.edgible.com`, with its certificate issued for you. |
| Custom domain | A name of your own added to an app, pointed at its Edgible hostname with a `CNAME`. Edgible then issues a certificate for it too. |
| Auth mode | The access rule attached to a hostname, chosen when the app is created: `org`, `api-key` or `None`. |
| `org` | Auth mode requiring a browser login from your organisation. Used for anything holding credentials, such as the n8n editor or the OpenClaw Control UI. |
| `api-key` | Auth mode accepting a bearer secret, for callers that cannot complete a browser login. Used for the published Ollama. |
| `None` | Auth mode with no check, for callers such as Stripe or GitHub webhooks that cannot sign in. |
| Org | Your organisation in Edgible. It appears in every hostname and defines who `org` auth lets in. |
| Unpublish | Removing an app, which takes its hostname down while leaving the service running and other apps serving. |

## Networking

| Term | What it means here |
| --- | --- |
| Outbound only | The serving agent dials out and keeps that connection open, so nothing listens for inbound connections and no router change is needed. |
| Port forward | A router rule exposing a local port to the internet. These guides never use one, and the checklist of every chapter that publishes a port confirms it is still not forwarded. |
| Virt LAN | The private network between a host and its own virtual machines, often `192.168.64.x` under UTM. It reaches the host, and nothing outside that machine. |
| `socat` | A small relay. In [LLM on Edgible](guides/llm-on-edgible/README.md) it listens on the guest's loopback and forwards to Ollama on the host, so the serving agent has a local port to publish. |
| E.164 | The international phone number format, such as `+61412345678`, used when allow-listing who may message an agent. |
| Loopback | The `127.0.0.1` address, reachable only from the machine itself. Services in these guides bind here, and the serving agent reaches them locally. |
| NAT | The address translation a home router does. It is sufficient for Edgible, because the connection is outbound. |
| Mesh VPN | A private network requiring every client device to be enrolled. One of the alternatives Edgible replaces. |
| Reverse proxy | A server such as nginx or Caddy placed in front of a service, usually paired with certbot and dynamic DNS. Another alternative Edgible replaces. |
| TLS termination | Where HTTPS is decrypted. With Edgible it happens on the serving device, which is why the original client IP does not reach the app. |
| Webhook | An HTTPS URL another system calls. It needs a hostname reachable without a login, so `None` rather than `org`. |

## Website, analytics and monitoring

| Term | What it means here |
| --- | --- |
| Static site | A directory of files a web server hands over unchanged, whatever produced them. Nothing runs per request. |
| Umami | Self-hosted web analytics: page views without cookies, with the database on your own machine. |
| Tracking script | The `script.js` Umami serves and your pages load. It must come from a hostname with `None`, because visitors have no login. |
| Website ID | The UUID Umami assigns your site, named in the tracking snippet so hits are attributed to it. |
| Ingest hostname | The `None` hostname visitors' browsers reach, as opposed to the `org` hostname you read the numbers on. Both point at the same process. |
| Uptime Kuma | Self-hosted uptime monitoring: it requests a URL on a schedule and notifies you when the answer changes. |
| `8080` | The site's nginx port on the guest, bound to loopback. |
| `3000` | Umami's port on the guest, bound to loopback. |
| `3001` | Uptime Kuma's port on the guest, bound to loopback. |

## n8n

| Term | What it means here |
| --- | --- |
| n8n | The workflow runner: the canvas and the executions. Not OpenClaw. |
| Editor | The n8n canvas in a browser. Published with `org` because it holds every credential you have added. |
| `n8n-hooks` | The second app on the same container, with `None`, so outside callers can reach webhook URLs. |
| `WEBHOOK_URL` | The n8n setting naming the origin it prints on webhook nodes. It changes what n8n advertises, not where traffic lands. |
| `5678` | n8n's HTTP port on the guest, bound to loopback. |

## OpenClaw

| Term | What it means here |
| --- | --- |
| Gateway | The OpenClaw process on the VM. It stays on loopback; Edgible publishes it rather than it listening publicly. |
| Control UI | The OpenClaw web interface, published with `org` so it opens on a phone without a VPN. |
| Skill | A capability added to OpenClaw. The Edgible skill lets it run the Edgible CLI. |
| ACP | Agent Client Protocol, the exchange two programs hold over stdin and stdout: start a session, send a prompt, stream tool calls, finish. OpenClaw is the client. |
| `acpx` | The OpenClaw plugin that owns the ACP client. Until it is installed and the Gateway restarted, `/acp doctor` reports `ACP_BACKEND_MISSING`. |
| Harness | Cursor CLI running as the ACP server, via `agent acp`. |
| Session | One ACP job, keyed as `agent:cursor:acp:<uuid>`. |
| `18789` | The OpenClaw Gateway port on the VM, bound to loopback. |
| `permissionMode` | How much OpenClaw does without asking. `approve-reads` asks before writing; `approve-all` stops asking, which is what an unattended coding pass needs and what you set back afterwards. |
| BotFather | Telegram's own bot for creating bots. It issues the token the Telegram client uses. |
| Linked device | A WhatsApp session paired by scanning a QR code, the same mechanism as WhatsApp Web. |
| SearXNG | A self-hosted search backend. n8n's AI Assistant uses it rather than a hosted search API. |

## Self-hosted models

| Term | What it means here |
| --- | --- |
| Ollama | The local model runner these guides publish with `api-key`. |
| Ollama.app | The macOS menu-bar app. The error `could not find ollama app` means you are on Linux, or the app is quit. |
| Bare metal | macOS on the Mac itself, not the Ubuntu guest inside it. Ollama runs here for GPU access. |
| Metal | How Ollama reaches the Mac GPU. A UTM guest cannot, which is why inference stays on the host. |
| Model tag | The name and size of a model, such as `qwen2.5:7b` or `gpt-oss:20b`. |
| `11434` | Ollama's HTTP port, on the Mac by default. |

## The machines in these guides

| Term | What it means here |
| --- | --- |
| Ubuntu guest | The virtual machine running the serving agent, created in [Edgible on an Ubuntu VM](guides/start-here/01-edgible-on-vm.md). Most commands run here. |
| Host computer | The laptop or desktop the virtual machine runs on. In [LLM on Edgible](guides/llm-on-edgible/README.md) it is a Mac, and it runs Ollama. |
| Hello World | The first published page, used throughout as the check that publishing still works. |
| `8081` | The Hello World nginx port on the guest, bound to loopback. Later chapters check it is still what `hello-world` points at. |
