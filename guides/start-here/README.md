# Start here: chapters

**From a blank virtual machine to a page the internet can load, without touching your router.**

One chapter, and every other guide depends on it. You end with a machine you own, registered to your organisation, serving a page that loads on a phone with Wi-Fi turned off. That last check is the whole idea in one test: nothing connects in, so there is no port to forward, and the page is still public.

![A phone on cellular reaches one open hostname, which arrives at Hello World on loopback on a machine you own, with no forwarded port](../../images/diagrams/start-here-light.svg#only-light)
![A phone on cellular reaches one open hostname, which arrives at Hello World on loopback on a machine you own, with no forwarded port](../../images/diagrams/start-here-dark.svg#only-dark)

Chapters share a shape: a one-line hook under the title, then **N.0 Why** (what is missing without this chapter, and which machine you run it on), then **N.1 The job** (what you'll do, how you'll know, what you need, what this is not). Steps after that, a **Verify** checklist that mirrors *Done when*, and **Next** at the end.

**Need first:** a computer that can run a virtual machine, a phone, and an Edgible account, which you create yourself at [www.edgible.com](https://www.edgible.com). No router change, no domain, no cloud account.

| # | Chapter | Smoke test |
| --- | --- | --- |
| 1 | [1. Edgible on an Ubuntu VM](01-edgible-on-vm.md) | `edgible whoami` on the VM; Hello World on a phone (cellular) |

Leave Hello World running when you finish. The other guides use it as the check that publishing still works, and each of them ends with a teardown chapter that removes its own services and leaves Hello World and the serving agent alone. Each of those chapters ends with an optional step for removing Hello World too, once no other guide needs it.

Then pick a guide by what you want to stop paying for or stop handing over:

- [Website on Edgible](../website-on-edgible/README.md): a site, its analytics and its uptime monitor, all on your machine.
- [n8n on Edgible](../n8n-on-edgible/README.md): the back office automation, with the credentials it holds staying in your building.
- [OpenClaw on Edgible](../openclaw-on-edgible/README.md): an AI agent with a shell, reachable from your phone, never exposed.
- [LLM on Edgible](../llm-on-edgible/README.md): a model on your own GPU, called over HTTPS by other machines you own.
