# Self Hosting is Social: chapters

**The website pattern is one file you can hand over, and the file that publishes those apps again.**

[Website on Edgible](../website-on-edgible/README.md) builds four apps as four separate answers: the site, the tracking script, the analytics dashboard and the monitor. The file you can hand to someone else is those four answers written once. Your device name, your hostnames and your organization id stay out of it. The same file is what puts the apps back.

![The website card lists four apps and no hostnames. site is nginx serving your files on port 8080, open to anyone. analytics is the Umami tracking script on port 3000, open to anyone. umami is the Umami dashboard on that same port, with Postgres, behind an org login. status is Uptime Kuma on port 3001, behind an org login. The card names no device and no organization.](../../images/diagrams/self-hosting-is-social-light.svg#only-light)
![The website card lists four apps and no hostnames. site is nginx serving your files on port 8080, open to anyone. analytics is the Umami tracking script on port 3000, open to anyone. umami is the Umami dashboard on that same port, with Postgres, behind an org login. status is Uptime Kuma on port 3001, behind an org login. The card names no device and no organization.](../../images/diagrams/self-hosting-is-social-dark.svg#only-dark)

One chapter. It assumes the website stack has been torn down, so the containers are stopped and the hostnames are gone, and the Compose files are still on disk.

Chapters share a shape: a one-line hook under the title, then **N.0 Why** (what is missing without this chapter, and which machine you run it on), then **N.1 The job** (what you'll do, how you'll know, what you need, what this is not). Steps after that, a **Verify** checklist that mirrors *Done when*, and **Next** at the end.

**Need first:** [Tear down the website stack](../website-on-edgible/06-website-teardown.md), with the serving agent still installed.

| # | Chapter | Smoke test |
| --- | --- | --- |
| 1 | [1. The website card](01-website-card.md) | The card lists the four apps and no hostname; `edgible app list` shows them again |

The Compose files and the passwords stay in [Website on Edgible](../website-on-edgible/README.md). This chapter does not rewrite them.
