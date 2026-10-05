# Self Hosting is Social: chapters

**A proven solution can be shared as a pattern, so someone else can reproduce it.**

The service stays on hardware you own. The pattern of how you published it is what someone else can reuse.

A card is that pattern when several apps have to coexist and work together to solve one problem. It names the programs, the images, the ports, the auth mode, and which apps share a serving device. It leaves out your device name, your hostnames, and your organization id. The next person maps each place to a serving device they have, and Edgible publishes the apps. The auth mode stays `None`, `org`, or `api-key`, separate from the program.

What you stop doing is rebuilding a known setup from memory. The website card is four apps in two places. The n8n card is two hostnames on one process, the editor on `org` and the hooks on `None`. One app on one port is a single `edgible app create existing`, which is the whole job.

Hover a step.

![You build several Edgible apps, write them as a card, add files such as tailor.sh, and publish the card. Someone else finds that card, tailors it for their machine, turns it into a stack file, and deploys the stack.](../../images/diagrams/self-hosting-is-social-light.svg#only-light)
![You build several Edgible apps, write them as a card, add files such as tailor.sh, and publish the card. Someone else finds that card, tailors it for their machine, turns it into a stack file, and deploys the stack.](../../images/diagrams/self-hosting-is-social-dark.svg#only-dark)

## The card

The cards live in [Edgible/cards](https://github.com/Edgible/cards). [card.schema.json](https://github.com/Edgible/cards/blob/main/tools/card.schema.json) is the source of truth for the file. [card-to-stack.py](https://github.com/Edgible/cards/blob/main/tools/card-to-stack.py) writes the stack file, filling in your device name and your organization id. When a card includes `tailor.sh`, that card's README is how you run it. [1. The website card](01-website-card.md) and [2. The n8n card](02-n8n-card.md) use the files from that repo.

Each chapter is one job and one smoke test. Do them in order.

Chapters share a shape: a one-line hook under the title, then **N.0 Why** (what is missing without this chapter, and which machine you run it on), then **N.1 The job** (what you'll do, how you'll know, what you need, what this is not). Steps after that, a **Verify** checklist that mirrors *Done when*, and **Next** at the end.

**Need first:** [Start here](../start-here/README.md), so a serving agent is installed. The website example also needs [Tear down the website stack](../website-on-edgible/06-website-teardown.md). The n8n example also needs [Tear down n8n](../n8n-on-edgible/06-n8n-teardown.md).

| # | Chapter | Smoke test |
| --- | --- | --- |
| 1 | [1. The website card](01-website-card.md) | `edgible app list` shows `site`, `analytics`, `umami` and `status` again |
| 2 | [2. The n8n card](02-n8n-card.md) | `edgible app list` shows `n8n` (`org`) and `n8n-hooks` (`None`) |
