# Welcome

Edgible is a software platform that makes self-hosting easy and safe. It takes a service already running on a machine you own, a mini-PC at home, a spare laptop, a VM, and puts it on a public HTTPS hostname that anyone you choose can reach. No port forwarded on your router, no certificate to renew, and no copying your data onto somebody else's server.

This site is a growing library of guides that show that happening, one use case at a time, with commands you can paste and results you can check.

![A desktop PC on a home office desk at night, lit fans above a large graphics card that carries the Edgible hexagon as a faint watermark](images/self-hosted-machine.jpg){ .hero }

## What Edgible does

The machine you are serving from opens an outbound connection on TCP 443 and keeps it open. A hostname then appears, with a certificate already issued and an access rule already applied. Nothing listens for inbound connections, so there is no port to forward and no firewall hole to maintain.

Each published hostname carries its own auth mode: `org` puts a login from your organisation in front of it, `api-key` accepts a bearer secret from machines that cannot log in, and `None` leaves it open for callers like payment or repository webhooks. Because the rule belongs to the hostname rather than to the service, one running process can be published more than once with different protection on each hostname.

What you do not have to run: dynamic DNS, certbot and its renewal cron, a hand-written nginx or Caddy config, or a mesh VPN that every device needs enrolling into.

## Why these guides are worth your time

Product pages assert things. These guides show them, on ordinary hardware, in the order you would actually do them.

- Every chapter is one job. It states what you will have when you finish, and ends with a checklist that mirrors it item for item, so you always know whether the step worked.
- Commands are literal and complete, and each chapter says which machine to run them on.
- Every claim has an observable check behind it. When a guide says a service is reachable without a forwarded port, the test is loading it on a phone with Wi-Fi turned off.
- Each use case series ends with a teardown chapter, so a guide you tried out of curiosity leaves nothing running.

The services being published are stock software, unmodified: nginx, n8n, Umami, Uptime Kuma, Ollama and OpenClaw are all open source, and you install them from their own projects. Where a chapter reaches for an outside service, it says at the top what that service asks of you, as [Cursor Agent](guides/openclaw-on-edgible/07-cursor-agent.md) and [Models beyond free Gemini](guides/openclaw-on-edgible/08-models-beyond-free-gemini.md) do. Both of those are optional.

## The guides

New guides get added over time, each taking a service people genuinely self-host and putting it online the same way. Every one of them starts from [Start here](guides/start-here/README.md), which installs the serving agent and gets a first page online. The four available now:

- [Website on Edgible](guides/website-on-edgible/README.md). **The whole small-site stack, on hardware you own.** A static site, self-hosted analytics and uptime monitoring on one machine, published as four hostnames with three different access rules. The easiest place to begin. Six chapters.
- [n8n on Edgible](guides/n8n-on-edgible/README.md). **The back office workhorse, with the credentials staying in your building.** The editor that holds them is behind an `org` login, while a second hostname on `None` accepts webhooks from services that cannot sign in. Six chapters.
- [OpenClaw on Edgible](guides/openclaw-on-edgible/README.md). **The agent everyone is currently trying, on hardware you control.** Reachable from your phone over HTTPS, with its Gateway still bound to loopback and no VPN on the phone. Nine short chapters.
- [LLM on Edgible](guides/llm-on-edgible/README.md). **Private AI, where the prompts and the weights stay home.** A self-hosted Ollama published with `api-key` and called over HTTPS by other machines you own. Five chapters.

## Where to start

Everyone starts with [Start here](guides/start-here/README.md). It installs the serving agent on a machine you own and gets one page online, which every other guide builds on. From there, pick whichever guide is closest to something you already run.

If you would rather see the feature list first, [What Edgible does, and where these guides prove it](capabilities.md) maps each capability to the chapter that demonstrates it.

If you are reading alongside a coding agent or a chat assistant, [Working with an AI tool](working-with-ai.md) covers the markdown sources, the `llms.txt` index and the whole site in one fetch.
