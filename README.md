# Welcome

Edgible publishes a service running on a machine you own at a public HTTPS hostname. This site is a growing library of guides that show that happening, one use case at a time, with commands you can paste and results you can check.

## What Edgible does

The machine you are serving from dials out on TCP 443 and keeps that connection open. A hostname then appears, with a certificate already issued and an access rule already applied. Nothing listens for inbound connections, so there is no port to forward and no firewall hole to maintain.

Each published hostname carries its own auth mode: `org` puts a login from your organisation in front of it, `api-key` accepts a bearer secret from machines that cannot log in, and `None` leaves it open for callers like payment or repository webhooks. Because the rule belongs to the hostname rather than to the service, one running process can be published more than once with different protection on each hostname.

What you do not have to run: dynamic DNS, certbot and its renewal cron, a hand-written nginx or Caddy config, or a mesh VPN that every device needs enrolling into.

## Why these guides are worth your time

Product pages assert things. These guides show them, on ordinary hardware, in the order you would actually do them.

- Every chapter is one job. It states what you will have when you finish, and ends with a checklist that mirrors it item for item, so you always know whether the step worked.
- Commands are literal and complete, and each chapter says which machine to run them on.
- Every claim has an observable check behind it. When a guide says a service is reachable without a forwarded port, the test is loading it on a phone with Wi-Fi turned off.
- Each series ends with a teardown chapter, so a guide you tried out of curiosity leaves nothing running.

Nothing here needs a paid account with a third party to complete, and the services being published are stock software, unmodified.

## The guides

New guides get added over time, each taking a service people genuinely self-host and putting it online the same way. The three available now:

- [1. n8n on Edgible](guides/n8n-on-edgible/README.md). A workflow platform whose editor holds all your credentials, kept behind an `org` login, while a second hostname on `None` accepts webhooks from services that cannot sign in. Six chapters.
- [2. OpenClaw on Edgible](guides/openclaw-on-edgible/README.md). An AI agent you can reach from your phone over HTTPS, with its Gateway still bound to loopback on the machine and no VPN on the phone. Ten short chapters.
- [3. LLM on Edgible](guides/llm-on-edgible/README.md). A self-hosted Ollama that keeps the model weights and the GPU at home, published with `api-key` and called over HTTPS by other machines you own. Four chapters.

## Where to start

If you have never published anything with Edgible, start with [Edgible on an Ubuntu VM](guides/openclaw-on-edgible/01-edgible-on-vm.md). It installs the serving agent and gets one page online, and it is the shared first chapter for all three guides rather than the start of the OpenClaw one. From there, pick whichever guide is closest to something you already run.

If you would rather see the feature list first, [What Edgible does, and where these guides prove it](capabilities.md) maps each capability to the chapter that demonstrates it.

If you are reading alongside a coding agent or a chat assistant, [Working with an AI tool](working-with-ai.md) covers the markdown sources, the `llms.txt` index and the whole site in one fetch.
