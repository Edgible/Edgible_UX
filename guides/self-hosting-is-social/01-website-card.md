# 1. The website card

**A website others can reproduce: the site, its editor, the analytics and the monitor, written as one card.**

## 1.0 Why

[Website on Edgible](../website-on-edgible/README.md) published a public site, an open tracking script, a locked analytics dashboard, and a locked uptime monitor. [Tear down the website stack](../website-on-edgible/06-website-teardown.md) deleted those hostnames and stopped the containers. This chapter runs the website again from the [website card](https://github.com/Edgible/cards/blob/main/cards/website/README.md). The site is a React app. The editor is Strapi.

The card has two places. `site`, `strapi`, `analytics`, and `umami` are `web`. `status` is `monitor`. This chapter maps both places to `minipc`.

![The website card lists five apps in two places, and no hostnames. Place web is one serving device: site is your pages, served by React on port 8080, open to anyone. strapi is Strapi editor on port 1337, org login. analytics is Umami tracking script, same process as umami on port 3000, open to anyone. umami is Umami dashboard on port 3000, org login. Place monitor may be another serving device: status is Uptime Kuma on port 3001, org login. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/cards/website/images/card-light.svg#only-light)
![The website card lists five apps in two places, and no hostnames. Place web is one serving device: site is your pages, served by React on port 8080, open to anyone. strapi is Strapi editor on port 1337, org login. analytics is Umami tracking script, same process as umami on port 3000, open to anyone. umami is Umami dashboard on port 3000, org login. Place monitor may be another serving device: status is Uptime Kuma on port 3001, org login. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/cards/website/images/card-dark.svg#only-dark)

**Where you run this:** the **Ubuntu guest**. Follow the [website card](https://github.com/Edgible/cards/blob/main/cards/website/README.md) in your home directory.

## 1.1 The job

You follow the How on the website card.

**Done when**

- `edgible app list` shows `site`, `strapi`, `analytics`, `umami` and `status`.

**Need first:** [Tear down the website stack](../website-on-edgible/06-website-teardown.md), including the serving agent still installed. `hello-world` can stay.

**Not this chapter:** the commands, the Compose files, and `card.env`. Those are the [website card](https://github.com/Edgible/cards/blob/main/cards/website/README.md).

## 1.2 How

The commands are on the [website card](https://github.com/Edgible/cards/blob/main/cards/website/README.md). In your home directory:

1. Fetch the card.
2. Edit `card.env`. Set `WEB_DEVICE` and `MONITOR_DEVICE` to `minipc`.
3. Start the site and Umami.
4. Start the monitor. Both places are this machine.
5. Publish.

```bash
edgible app list
```

`edgible app list` shows `site` and `analytics` with `None`, and `strapi`, `umami`, and `status` with `org`.

If the teardown removed the Umami tracking snippet from your pages, put it back from [Publish Umami](../website-on-edgible/04-publish-umami.md) when you want page views again. The hostnames publish either way.

## 1.3 Getting started

Follow Getting Started on the [website card](https://github.com/Edgible/cards/blob/main/cards/website/README.md).

## Verify

- [ ] `edgible app list` shows `site`, `strapi`, `analytics`, `umami` and `status`.

## Next

[2. The n8n card](02-n8n-card.md). Series: [README](README.md).
