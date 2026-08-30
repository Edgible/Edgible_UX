# Start here: chapters

One chapter, and every other guide depends on it. You end with a machine you own, registered to your organisation, serving a page the internet can load.

Chapters share a shape: a one-line hook under the title, then **N.0 Why** (what is missing without this chapter, and which machine you run it on), then **N.1 The job** (what you'll do, how you'll know, what you need, what this is not). Steps after that, a **Verify** checklist that mirrors *Done when*, and **Next** at the end.

**Need first:** a computer that can run a virtual machine, a phone, and an Edgible account, which you create yourself at [www.edgible.com](https://www.edgible.com). No router change, no domain, no cloud account.

| # | Chapter | Smoke test |
| --- | --- | --- |
| 1 | [1. Edgible on an Ubuntu VM](01-edgible-on-vm.md) | `edgible whoami` on the VM; Hello World on a phone (cellular) |

Leave Hello World running when you finish. The other guides use it as the check that publishing still works, and each of them ends with a teardown chapter that removes its own services and leaves Hello World and the serving agent alone. Each of those chapters ends with an optional step for removing Hello World too, once no other guide needs it.

Then pick a guide: [Website on Edgible](../website-on-edgible/README.md), [n8n on Edgible](../n8n-on-edgible/README.md), [OpenClaw on Edgible](../openclaw-on-edgible/README.md), or [LLM on Edgible](../llm-on-edgible/README.md).
