# For evaluators and architects

**Where Edgible sits if you already know tunnels, reverse proxies, and self-hosted ingress.**

You have probably already tried one or more of: a forwarded port, dynamic DNS with certbot, a hand-rolled reverse proxy, a managed outbound tunnel, or a mesh VPN. This page names the job in that vocabulary, states what any serious ingress product already does, and spells out what Edgible emphasises on top. For hands-on proof, follow the [guides](../README.md) or see [What Edgible does](../capabilities.md).

## The job, in words you already use

People label the same outcome differently. Edgible is aimed at all of the following:

| Term | What it usually means here |
| --- | --- |
| **Ingress** | Public internet traffic reaching a process on a machine you control |
| **Reverse tunnel / outbound tunnel** | Your machine holds an outbound connection; nothing listens for inbound connections on the router |
| **Remote access** | Reaching a home or VM service from outside the LAN without a VPN client on the visitor |
| **No port forwarding** | No router rule exposing a local port; often required anyway when the ISP puts you behind carrier-grade NAT |
| **Tunnel** | Traffic carried inside another connection. The word covers public ingress, mesh VPNs, and short-lived dev relays; it does not specify which |
| **Self-hosting** | The app runs on hardware you own; ingress is what turns "works locally" into "reachable from anywhere" |

**The job, stated plainly:** a service runs on your machine. You want a stable `https://` URL that the people and systems you choose can reach, without forwarding a port, operating dynamic DNS, renewing certificates yourself, or copying the workload to someone else's server.

The guides on this site are use cases (websites, workflows, agents, models). Ingress is the capability they share.

## Where Edgible sits

Edgible is **managed ingress for self-hosted services**.

A **serving agent** on your machine holds an **outbound** connection on TCP 443. Edgible provisions a **hostname**, issues and renews **TLS certificates**, and **routes** HTTPS to a local port. You choose an **auth mode per app**: `org` for a browser login from your organisation, `api-key` for machine callers, or `None` for open access.

Published hostnames use the shape `https://<app>.<org>.edgible.com`. First publish is **zero-DNS**: a working `https://` name with certificate and routing, and no registrar or zone edit. Bring your own domain later with **one `CNAME`** at the DNS provider you already use.

Traffic path in outline:

```text
Visitor → HTTPS → Edgible gateway → outbound tunnel from your device → your service
```

TLS terminates on your machine. Your LAN does not accept inbound connections for this path.

## How you operate it

Edgible is a **managed commercial service**: the gateway and control plane run on Edgible's side; you run the serving agent and your workloads. You are not maintaining tunnel server, certificate automation, and an admin UI fork yourself.

Day to day you use the **CLI** or the **dashboard** at [app.prod.edgible.com](https://app.prod.edgible.com/) — devices, apps, certificates, and health. The guides show the same publish flow from flags or from prompts; see [n8n editor through Edgible](../guides/n8n-on-edgible/02-n8n-editor-through-edgible.md) for both forms.

**Example:** something is already listening on a port — nginx, n8n, Ollama, a static file server. You do not write an ingress config or stand up a separate tunnel object first:

```bash
edgible app create existing
```

Answer name, auth mode, device, and port (or pass them as flags). Edgible discovers the listener, provisions the hostname, and starts certificate issuance. That is the shape most of these guides use.

Few products in this category collapse **publish an existing listener** into one step with **auth mode baked in**. Many split routing rules, DNS, and access policy across a config file and a web console. One-line dev relays are faster for a throwaway port expose; they typically do not carry name, device, certificate state, and per-hostname auth through the same tool — which is why the honest limit on demo speed stays in the table below.

### Use-case recipes, not in-product presets

Edgible deliberately keeps **one generic publish path** in the CLI and console (`app create existing` with name, device, port, and auth). There is no maintained catalogue of app-specific shortcuts — no `publish ollama` or `publish n8n` baked into the product that must track every upstream port and auth pattern.

**Use-case recipes live in the guides** instead: observable chapters for n8n, a static site stack, Ollama, OpenClaw, each with a smoke test. They change when the self-host landscape changes, without waiting for a CLI release.

That is intentional in an AI-assisted workflow: the same markdown the guides publish is fetchable at stable URLs, indexed in [`llms.txt`](../llms.txt), and described in [Working with an AI tool](../working-with-ai.md). An assistant reads the recipe and runs the generic CLI with the right flags — the product does not need to embed every popular app.

The same applies to **third-party products we do not own** (AI gateways, photo apps, new self-host favourites): we document **ingress patterns** (`api-key` for machine callers, split-surface for mixed visitors), not a maintained chapter per upstream that tracks their releases. Your agent combines Edgible’s guides with that product’s current documentation.

For evaluators, the question is not “does Edgible ship a preset for X?” but “is there a proven chapter for X, and does the generic publish primitive support it?” — including **split-surface publish** when one process needs two hostnames. For gateways and other complements, ask whether the **pattern** is proven and whether reachability is the job Edgible solves.

## What any serious ingress option already does

These are table stakes in the category. They are necessary to be credible; they are not unique to Edgible.

- Outbound connectivity, no public IP required on your side
- Automatic HTTPS certificates for the published hostname
- Works behind NAT and CGNAT
- A stable URL for a local service
- No port-forward rule on the router

If you are comparing products that all claim the above, the useful questions move to custody, policy, visitors, and operations.

## What Edgible emphasises

Stated without naming other products.

### 1. Zero-DNS publish

On first publish you get a working `https://` name, with certificate and routing in place, and **no DNS step** — no registrar, no zone record. Architects often describe this as a **generated hostname** or **platform-provided name**; we call it **zero-DNS publish**. Bring your own domain later if you want; you are not blocked waiting on a registrar.

### 2. Your DNS zone stays where it is

Custom domains attach with **one `CNAME`** at your existing provider. You do not move nameservers or hand over the whole zone to publish one service.

### 3. Split-surface publish

Each published app carries its own auth mode. The same process on the same port can be published **twice** with different rules — for example an admin UI on `org` and a webhook receiver on `None`, because payment providers and repository hosts cannot complete a browser login. That pattern is familiar as a **separate admin hostname** or **dual public exposure** of one backend; we call it **split-surface publish** (not split tunneling, which means something else in VPN literature).

A forwarded port is all-or-nothing. A mesh VPN is enrol-or-nothing for visitors. Per-hostname policy is the middle ground those two cannot offer.

Demonstrated in [Public webhook hostname](../guides/n8n-on-edgible/03-n8n-public-webhook-hostname.md) and [Publish Umami](../guides/website-on-edgible/04-publish-umami.md).

### 4. Nothing on the visitor

Browsers, webhooks, phone apps and customers reach a normal `https://` URL. No VPN client, no enrolled device, no special app on the caller side. This is the line between **public ingress** and **overlay VPN** approaches in the same "tunneling" lists.

### 5. Built for sustained self-hosted workloads

Photo libraries, media, large uploads and long-lived services are in scope. Some CDN-backed tunnel offerings restrict sustained media traffic in their terms; evaluate any product against the shape of traffic you actually intend to carry.

### 6. Against DIY and port forwarding

If you are still on a forwarded port or a hand-maintained reverse proxy, the comparison is different from comparing two managed tunnels.

- **CGNAT:** for a growing share of connections there is no public address to forward, so skill does not help.
- **Asymmetry:** an open port answers the internet continuously; you patch and renew on that schedule.
- **Capability:** one port cannot give one service two public identities with two access rules.

[Start here](../guides/start-here/01-edgible-on-vm.md) ends with the observable check: the page loads on a phone with Wi-Fi off, while the verify list still shows the port is not forwarded.

## Quick evaluation checklist

Questions an architect can answer from the guides without trusting marketing copy.

| Question | Where to look |
| --- | --- |
| Does publishing work with no inbound port? | [Edgible on an Ubuntu VM](../guides/start-here/01-edgible-on-vm.md): phone on cellular |
| Can you publish a port that is already listening, without a config file? | [Edgible on an Ubuntu VM](../guides/start-here/01-edgible-on-vm.md) §1.9: `edgible app create existing` |
| Are use-case recipes maintained outside the CLI (guides / `llms.txt`)? | [Welcome](../README.md) guide list, [Working with an AI tool](../working-with-ai.md) |
| Are certificates issued per hostname? | Console **Certificates**, or `edgible app list` / `edgible app status` |
| Can you publish with zero-DNS (no zone edit on first hostname)? | [Edgible on an Ubuntu VM](../guides/start-here/01-edgible-on-vm.md) §1.9: hostname before any `CNAME` |
| Can one process use split-surface publish (two hostnames, two auth modes)? | [n8n public webhook hostname](../guides/n8n-on-edgible/03-n8n-public-webhook-hostname.md), [Publish Umami](../guides/website-on-edgible/04-publish-umami.md) |
| Can machine callers use `api-key`? | [Edgible publishes Ollama](../guides/llm-on-edgible/02-edgible-to-ollama.md) |
| Can a custom domain point at an Edgible hostname? | [A domain of your own](../guides/website-on-edgible/02-publish-the-site.md#26-a-domain-of-your-own-optional) |
| Vocabulary in one fetch | [Glossary](../glossary.md) |

## Honest limits to weigh

No product wins every comparison. These are worth asking about in your environment.

| Topic | Note |
| --- | --- |
| **Global edge and DDoS** | A large CDN operator's edge network is bigger than a focused ingress platform's |
| **Time to first URL in a demo** | A one-line dev relay can be faster for a throwaway port expose |
| **Device-to-device mesh** | Overlay VPN products solve SSH and LAN extension between enrolled machines; that is a different job |
| **Identity policy depth** | Enterprise zero-trust products offer more identity providers and richer rules than three hostname auth modes |
| **Visitor IP at the app** | TLS terminates on your device (Edgible does not read HTTP), so apps that rely on `X-Forwarded-For` for geolocation or rate limits may see the tunnel hop until [client IP preservation](https://guides.edgible.com/guides/website-on-edgible/04-publish-umami.md#45-what-the-country-column-will-not-tell-you) ships; the platform should not permanently block honoring the real visitor |
| **Agent privileges** | The serving agent is installed with privileges sufficient to configure networking on the host today; confirm your security model against that |

## Related pages

- [What Edgible does](../capabilities.md): each feature mapped to the chapter that demonstrates it
- [Glossary](../glossary.md): `serving agent`, auth modes, published hostname, and the rest of the vocabulary
- [Working with an AI tool](../working-with-ai.md): fetch this page as markdown, or use `llms.txt` for the whole site
