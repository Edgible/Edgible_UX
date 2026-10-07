# 1. The website card

**A website others can reproduce: the site, the analytics and the monitor, written as one card.**

## 1.0 Why

[Website on Edgible](../website-on-edgible/README.md) is four apps: a public site, an open tracking script, a locked analytics dashboard, and a locked uptime monitor. [Tear down the website stack](../website-on-edgible/06-website-teardown.md) deleted the hostnames and stopped the containers. This chapter takes that website from [cards](https://github.com/Edgible/cards) and publishes the four apps again.

The card for this example has two places. `site`, `analytics`, and `umami` are `web`. `analytics` and `umami` share port `3000`, so they stay on one serving device. `status` is `monitor`, which can be that same device or a second one. This chapter maps both places to `minipc`.

![The website card lists four apps in two places, and no hostnames. Place web is one serving device: site is your static files, served by nginx on port 8080, open to anyone. analytics is Umami tracking script, same process as umami on port 3000, open to anyone. umami is Umami dashboard on port 3000, org login. Place monitor may be another serving device: status is Uptime Kuma on port 3001, org login. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/cards/website/images/card-light.svg#only-light)
![The website card lists four apps in two places, and no hostnames. Place web is one serving device: site is your static files, served by nginx on port 8080, open to anyone. analytics is Umami tracking script, same process as umami on port 3000, open to anyone. umami is Umami dashboard on port 3000, org login. Place monitor may be another serving device: status is Uptime Kuma on port 3001, org login. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/cards/website/images/card-dark.svg#only-dark)

**Where you run this:** the **Ubuntu guest**. The four apps are gone. Follow the [website card](https://github.com/Edgible/cards/blob/main/cards/website/README.md) in your home directory. Both places are `minipc`.

## 1.1 The job

You follow the website card: fetch it, edit `card.env`, start nginx, Umami and Uptime Kuma, and publish the four apps.

**Done when**

- `~/website/card.yml` lists `site` on port `8080` with `none`, `analytics` on port `3000` with `none`, `umami` on port `3000` with `org`, and `status` on port `3001` with `org`.
- Each app has a `what` line and a `from` line. `umami` also names `postgres:15-alpine`. `analytics` names the same Umami image as `umami`. That image is `ghcr.io/umami-software/umami:latest`. `status` names `louislam/uptime-kuma:2`.
- The card has no `deviceName`, no `<org>.edgible.com` hostname, and no organization id.
- The card has no `resources` section. The Compose files sit in the card directory.
- `site`, `analytics` and `umami` have `place: web`. `status` has `place: monitor`.
- `ss` shows `127.0.0.1:8080`, `127.0.0.1:3000` and `127.0.0.1:3001`.
- `edgible app list` shows those four apps again.

**Need first:** [Tear down the website stack](../website-on-edgible/06-website-teardown.md), including the serving agent still installed. `hello-world` can stay. The card fetches into `website/`, so the old directories do not have to already be on disk.

**Not this chapter:** a second copy of the card. The file is [cards/website/card.yml](https://github.com/Edgible/cards/blob/main/cards/website/card.yml).

## 1.2 Fetch the website card

The card lives in [cards](https://github.com/Edgible/cards). This chapter does not contain a second copy. [Working with an AI tool](../../working-with-ai.md) is how these guides are meant to be read alongside one, when you are writing a new card rather than using this one.

On the guest, in your home directory, follow step 1 of the [website card](https://github.com/Edgible/cards/blob/main/cards/website/README.md). Running that step again replaces `card.env`. The file is `~/website/card.yml`.

`what` is the software. `from` is the image. `umami` also names its database image, because that dashboard does not run alone. `analytics` is not a second program: it is the tracking script from that same Umami image.

`none` in the file is the auth mode `None`. `org` is the auth mode `org`. `analytics` and `umami` are the split surface from [Publish Umami](../website-on-edgible/04-publish-umami.md): one port, two auth modes.

`place` is the topology. It is not a device name. Applications with the same place run on one serving device, and that device is where the serving agent for those apps runs. `site`, `analytics` and `umami` are `web`, and `analytics` and `umami` have to stay together because they are one process on port `3000`. `status` is `monitor`, so it can live on a second serving device. A monitor on the same machine as the site cannot report that machine going down, which is [What this cannot tell you](../website-on-edgible/05-uptime-kuma.md#55-what-this-cannot-tell-you). This chapter maps both places to `minipc`.

The Compose files are in `~/website/` after that fetch. The steps are on the [website card](https://github.com/Edgible/cards/blob/main/cards/website/README.md).

`subtype: existing` on every app means a process is already listening on that port. The card only records the port. nginx, Umami and Uptime Kuma are still stopped, from [Tear down the website stack](../website-on-edgible/06-website-teardown.md). The next step starts them, so those ports have something listening before you publish.

## 1.3 Edit card.env and start

Follow steps 2, 3, and 4 of the [website card](https://github.com/Edgible/cards/blob/main/cards/website/README.md). Set `WEB_DEVICE` and `MONITOR_DEVICE` to `minipc`.

```bash
ss -ltnp | grep -E '8080|3000|3001'
```

`127.0.0.1:8080`, `127.0.0.1:3000` and `127.0.0.1:3001` are listening. If [Tear down the website stack](../website-on-edgible/06-website-teardown.md) removed the Umami tracking snippet from your pages, put it back from [Publish Umami](../website-on-edgible/04-publish-umami.md) when you want page views again. The hostnames publish either way.

## 1.4 Publish

The ports from 1.3 are listening. Follow step 5 of the [website card](https://github.com/Edgible/cards/blob/main/cards/website/README.md). The organization id comes from the logged-in CLI.

```bash
edgible app list
```

`edgible app list` shows `site` and `analytics` with `None`, and `umami` and `status` with `org`.

## 1.5 Getting started

Follow Getting Started on the [website card](https://github.com/Edgible/cards/blob/main/cards/website/README.md). The site page contains `Served from a box I own.`

## Verify

- [ ] `grep -nE 'name: (site|analytics|umami|status)|port:|authModes:' ~/website/card.yml` shows the four apps, ports `8080`, `3000`, `3000`, `3001`, and auth modes `none`, `none`, `org`, `org`.
- [ ] `grep -nE 'what:|from:|database:' ~/website/card.yml` shows `nginx:alpine`, `ghcr.io/umami-software/umami:latest` on both `analytics` and `umami`, `postgres:15-alpine`, and `louislam/uptime-kuma:2`.
- [ ] `grep -nE 'deviceName|organization' ~/website/card.yml` prints nothing.
- [ ] `grep -n 'edgible.com' ~/website/card.yml` prints nothing.
- [ ] `grep -nE 'resources:|compose:|changes:' ~/website/card.yml` prints nothing.
- [ ] `grep -n 'place:' ~/website/card.yml` shows `web` for `site`, `analytics` and `umami`, and `monitor` for `status`.
- [ ] `ss -ltnp | grep -E '8080|3000|3001'` shows `127.0.0.1` on each port.
- [ ] `edgible app list` shows `site`, `analytics`, `umami` and `status` again.

## Next

[2. The n8n card](02-n8n-card.md). Series: [README](README.md).
