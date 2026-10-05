# Self Hosting is Social: chapters

**A proven solution can be shared as a pattern, so someone else can reproduce it.**

Self-hosting keeps a service on hardware you own. The data stays there, and so do the passwords and the volumes. That is a private arrangement, which is why calling it social sounds like a contradiction. The contradiction is the point. The service stays private. The pattern of how you published it is what another person can use.

A useful self-hosted setup is a set of decisions: which programs, which images, which ports, which auth mode on each hostname, which files they need, and which of those programs share a serving device. Those decisions are what took the time. They usually live in one person's command history. A screenshot shows that it worked. It does not give the next person a way to stand the same thing up on their own machine.

Edgible is what makes the pattern separable from your machine. Each published app already has its own hostname and its own auth mode, `None`, `org`, or `api-key`, independent of the program behind it. A card writes those decisions down and leaves out what is yours alone: the device name, the hostnames, and the organization id. Whoever receives the card maps each place to a serving device they have, and Edgible publishes the apps on their hostnames.

The card is meant to be complete enough that the person sharing it does not also have to host the programs. An image is named by the registry that already publishes it. A Compose file is named by its public URL. When that file needs a change to be safe to publish this way, such as binding a port to `127.0.0.1`, the card lists the change instead of asking the sharer to rehost the file. Passwords and volume data are still created on the machine that runs the pattern.

What you stop doing is rebuilding a known setup from memory. What you can hand over is the pattern. The chapters after this page are examples of that. The first is a website. The second is n8n, starting from the Compose file n8n publishes.

Chapters share a shape: a one-line hook under the title, then **N.0 Why** (what is missing without this chapter, and which machine you run it on), then **N.1 The job** (what you'll do, how you'll know, what you need, what this is not). Steps after that, a **Verify** checklist that mirrors *Done when*, and **Next** at the end.

**Need first:** [Start here](../start-here/README.md), so a serving agent is installed. The website example also needs [Tear down the website stack](../website-on-edgible/06-website-teardown.md). The n8n example also needs [Tear down n8n](../n8n-on-edgible/06-n8n-teardown.md).

| # | Chapter | Smoke test |
| --- | --- | --- |
| 1 | [1. The website card](01-website-card.md) | `edgible app list` shows `site`, `analytics`, `umami` and `status` again |
| 2 | [2. The n8n card](02-n8n-card.md) | `edgible app list` shows `n8n` (`org`) and `n8n-hooks` (`None`) |
