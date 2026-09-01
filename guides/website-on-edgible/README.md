# Website on Edgible: chapters

**The whole small-site stack on one machine you own, with nobody else holding the numbers.**

A site, the analytics that tell you whether anyone read it, and the monitor that tells you when it broke. Taken separately those are three outside services, each with a copy of your traffic. Here they are three containers on a machine you already own, published on four HTTPS hostnames, with no port forwarded and no cloud host. The visitor data lands on your disk, and the monitor watching your site answers to you.

The public address does not have to be an `edgible.com` one. Add your own name to the app and point a `CNAME` at the Edgible hostname, and the site on the machine in your house answers at `www.example.com` with a certificate for that name. All it asks of you is a domain you can add a DNS record to. That is [2.6](02-publish-the-site.md#26-a-domain-of-your-own-optional).

![A phone reaches four hostnames, two open and two behind an org login, all arriving at three containers on loopback on one machine you own](../../images/diagrams/website-on-edgible-light.svg#only-light)
![A phone reaches four hostnames, two open and two behind an org login, all arriving at three containers on loopback on one machine you own](../../images/diagrams/website-on-edgible-dark.svg#only-dark)

This is also the clearest demonstration that auth is a property of the hostname. The site is `None`, because strangers are the audience. The Umami dashboard and the Uptime Kuma interface are `org`, because you are. Umami uses **split-surface publish** (see [Glossary](../../glossary.md)): the tracking script is `None` on a second hostname pointing at the same process as the dashboard, because a visitor's browser has to fetch it and will never have a login.

Each chapter is one job and one smoke test. Do them in order.

Chapters share a shape: a one-line hook under the title, then **N.0 Why** (what is missing without this chapter, and which machine you run it on), then **N.1 The job** (what you'll do, how you'll know, what you need, what this is not). Steps after that, a **Verify** checklist that mirrors *Done when*, and **Next** at the end.

**Need first:** [Start here](../start-here/README.md) (serving device `minipc`, Hello World on the phone). Leave `hello-world` running. The guest wants 4 GB of memory by the time all three services are up.

| # | Chapter | Smoke test |
| --- | --- | --- |
| 1 | [1. The site on the VM](01-site-on-the-vm.md) | `curl http://127.0.0.1:8080/` on the guest; nothing on the internet yet |
| 2 | [2. Publish the site](02-publish-the-site.md) | Phone (cellular) loads `site.<org>.edgible.com`, no login; optionally your own domain |
| 3 | [3. Umami on the VM](03-umami-on-the-vm.md) | Heartbeat on `127.0.0.1:3000`; default password changed |
| 4 | [4. Publish Umami](04-publish-umami.md) | `/script.js` open on `analytics.<org>…`; dashboard behind `org` on `umami.<org>…`; a cellular visit appears |
| 5 | [5. Uptime monitoring with Uptime Kuma](05-uptime-kuma.md) | Monitor green, then red when the site container stops, then green again |
| 6 | [6. Tear down the website stack](06-website-teardown.md) | Four hostnames gone; nothing on `8080`, `3000`, `3001`; `hello-world` and the serving agent left unless you opt in |

Two limits are stated where they arise rather than glossed over: visitor country is unavailable to self-hosted analytics behind Edgible ([4.5](04-publish-umami.md#45-what-the-country-column-will-not-tell-you)), and a monitor running on the machine it watches cannot report that machine going down ([5.5](05-uptime-kuma.md#55-what-this-cannot-tell-you)).

Next guides: [n8n on Edgible](../n8n-on-edgible/README.md), [OpenClaw on Edgible](../openclaw-on-edgible/README.md), [LLM on Edgible](../llm-on-edgible/README.md).
