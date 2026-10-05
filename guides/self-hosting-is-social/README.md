# Self Hosting is Social: chapters

**A proven solution can be shared as a pattern, so someone else can reproduce it.**

A self-hosted setup that solves a real problem usually lives in one person's command history. The next person, or you months later, rebuilds it from memory: the same images, the same ports, the same auth modes, and a fresh set of mistakes. A pattern is that solution written down so it can be handed over. What you share is the apps, what each one is, where it comes from, the port, the auth mode, and the public URLs of the Compose files that start them. What you leave out is yours alone: the device name, the hostnames, and the organization id. Whoever receives the pattern fills those in on their own machine and stands the same solution up again.

The file for a pattern is a card. One card is enough to see the solution, and, once a device name is supplied, to publish it again.

The first pattern here is a website. [Website on Edgible](../website-on-edgible/README.md) is that solution built the long way: nginx serving your files, Umami for the visits, Uptime Kuma for the monitor, four hostnames, two of them open and two behind an `org` login. This series writes that website as a card and reproduces it. Further patterns, for other problems, can follow the same shape.

![The website card lists four apps in two places, and no hostnames. Place web is one serving device: site is nginx serving your files on port 8080, open to anyone. analytics is the Umami tracking script on port 3000, open to anyone. umami is the Umami dashboard on that same port, with Postgres, behind an org login. Place monitor may be a second serving device: status is Uptime Kuma on port 3001, behind an org login. The card names no device and no organization.](../../images/diagrams/self-hosting-is-social-light.svg#only-light)
![The website card lists four apps in two places, and no hostnames. Place web is one serving device: site is nginx serving your files on port 8080, open to anyone. analytics is the Umami tracking script on port 3000, open to anyone. umami is the Umami dashboard on that same port, with Postgres, behind an org login. Place monitor may be a second serving device: status is Uptime Kuma on port 3001, behind an org login. The card names no device and no organization.](../../images/diagrams/self-hosting-is-social-dark.svg#only-dark)

One chapter, for this first pattern. It assumes the website stack has been torn down, so the containers are stopped and the hostnames are gone. The card names the images, the ports, and the public URLs of the Compose files. Volume data and passwords stay out of the card.

In this chapter you write the card by hand. A later tool will generate one from a running setup, and an AI can draft one from a description of the apps. The program that turns the card into a stack file is the stand-in for a later Edgible command.

Chapters share a shape: a one-line hook under the title, then **N.0 Why** (what is missing without this chapter, and which machine you run it on), then **N.1 The job** (what you'll do, how you'll know, what you need, what this is not). Steps after that, a **Verify** checklist that mirrors *Done when*, and **Next** at the end.

**Need first:** [Tear down the website stack](../website-on-edgible/06-website-teardown.md), with the serving agent from [Start here](../start-here/README.md) still installed.

| # | Chapter | Smoke test |
| --- | --- | --- |
| 1 | [1. The website card](01-website-card.md) | `edgible app list` shows `site`, `analytics`, `umami` and `status` again |

The Compose files and the passwords stay in [Website on Edgible](../website-on-edgible/README.md). This chapter does not rewrite them.
