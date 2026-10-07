# 2. The n8n card

**One n8n process, two auth modes, written as one card.**

## 2.0 Why

[n8n on Edgible](../n8n-on-edgible/README.md) publishes one process on port `5678` twice: the editor with `org`, and a webhook hostname with `None`. [Tear down n8n](../n8n-on-edgible/06-n8n-teardown.md) deleted those hostnames and stopped the container. This chapter takes that pattern from [cards](https://github.com/Edgible/cards) and publishes the two apps again.

The files are on the [n8n card](https://github.com/Edgible/cards/blob/main/cards/n8n/README.md). Both apps are place `workhorse`. This chapter maps that place to `minipc`.

![The n8n card lists two apps in one place, and no hostnames. Place workhorse is one serving device: n8n is n8n editor on port 5678, org login. n8n-hooks is n8n webhooks, same process as n8n on port 5678, open to anyone. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/cards/n8n/images/card-light.svg#only-light)
![The n8n card lists two apps in one place, and no hostnames. Place workhorse is one serving device: n8n is n8n editor on port 5678, org login. n8n-hooks is n8n webhooks, same process as n8n on port 5678, open to anyone. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/cards/n8n/images/card-dark.svg#only-dark)

**Where you run this:** the **Ubuntu guest**. The n8n hostnames are gone. Follow the [n8n card](https://github.com/Edgible/cards/blob/main/cards/n8n/README.md) in your home directory. The place is `minipc`.

## 2.1 The job

You follow the n8n card: fetch it, edit `card.env`, start the containers, and publish the two apps.

**Done when**

- `~/n8n/card.yml` lists `n8n` on port `5678` with `org`, and `n8n-hooks` on port `5678` with `none`.
- Both name `docker.n8n.io/n8nio/n8n:2.41.4`. `n8n` also names `postgres:18`.
- The card has no `deviceName`, no `<org>.edgible.com` hostname, and no organization id.
- The card has no `resources` section. The Compose file and `init-data.sh` sit in the card directory.
- Both have `place: workhorse`.
- `ss` shows `127.0.0.1:5678`, and nothing is listening on `5432`.
- `edgible app list` shows `n8n` with `org` and `n8n-hooks` with `None`.

**Need first:** [Tear down n8n](../n8n-on-edgible/06-n8n-teardown.md), including the serving agent still installed. One published app stays, such as `hello-world`, so you can read the org label into `ORG_LABEL`. The card fetches into `n8n/`.

**Not this chapter:** a second copy of the card, a cron workflow, or a webhook workflow. The file is [cards/n8n/card.yml](https://github.com/Edgible/cards/blob/main/cards/n8n/card.yml). The timezone in [n8n on the VM](../n8n-on-edgible/01-n8n-on-the-vm.md) stays off the card.

## 2.2 Fetch the n8n card

The field meanings are the same as [The website card](01-website-card.md). The files are on the [n8n card](https://github.com/Edgible/cards/blob/main/cards/n8n/README.md).

On the guest, in your home directory, follow step 1 of the [n8n card](https://github.com/Edgible/cards/blob/main/cards/n8n/README.md). Running that step again replaces `card.env`. The file is `~/n8n/card.yml`.

`n8n-hooks` is not a second program. It is the webhook hostname on the same process as `n8n`, the split from [Public webhook hostname](../n8n-on-edgible/03-n8n-public-webhook-hostname.md). `none` in the file is the auth mode `None`. `org` is the auth mode `org`.

`from` is the image name. `place` is `workhorse` on both apps because they are one process, so they stay on one serving device. Workflows in an older `n8n_data` volume stay on disk. This card uses the volume `n8n_storage`.

## 2.3 Edit card.env and start

Follow steps 2, 3, and 4 of the [n8n card](https://github.com/Edgible/cards/blob/main/cards/n8n/README.md). Set `DEVICE` to `minipc`. Set `ORG_LABEL` to the label from a hostname you already have.

```bash
docker compose -f ~/n8n/docker-compose.yml ps
ss -ltnp | grep 5678
ss -ltnp | grep 5432
curl -sS -o /dev/null -w "%{http_code}\n" http://127.0.0.1:5678/
```

`127.0.0.1:5678` is listening. `5432` is not. `curl` prints `200` or a 3xx. The Compose process list shows `n8n`, `postgres`, and `n8n-runner`.

## 2.4 Publish

The port from 2.3 is listening. Follow step 5 of the [n8n card](https://github.com/Edgible/cards/blob/main/cards/n8n/README.md). The organization id comes from the logged-in CLI.

```bash
edgible app list
```

`edgible app list` shows `n8n` with `org` and `n8n-hooks` with `None`, both on port `5678`.

## 2.5 Getting started

Follow Getting Started on the [n8n card](https://github.com/Edgible/cards/blob/main/cards/n8n/README.md). The editor hostname asks for an org login. The webhook hostname is open.

## Verify

- [ ] `grep -nE 'name: (n8n|n8n-hooks)|port:|authModes:' ~/n8n/card.yml` shows the two apps, port `5678` twice, and auth modes `org` and `none`.
- [ ] `grep -nE 'from:|database:' ~/n8n/card.yml` shows `docker.n8n.io/n8nio/n8n` twice and `postgres:18` once.
- [ ] `grep -nE 'deviceName|organization' ~/n8n/card.yml` prints nothing.
- [ ] `grep -n 'edgible.com' ~/n8n/card.yml` prints nothing.
- [ ] `grep -nE 'resources:|compose:|changes:' ~/n8n/card.yml` prints nothing.
- [ ] `grep -n 'place:' ~/n8n/card.yml` shows `workhorse` for both.
- [ ] `ss -ltnp | grep 5678` shows `127.0.0.1:5678`. `ss -ltnp | grep 5432` prints nothing.
- [ ] `edgible app list` shows `n8n` with `org` and `n8n-hooks` with `None`.

## Next

[3. The assistant card](03-assistant-card.md). Series: [README](README.md). The website card is [The website card](01-website-card.md).
