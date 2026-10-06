# 2. The n8n card

**One n8n process, two auth modes, written as a card that starts from n8n's own Compose file.**

## 2.0 Why

[n8n on Edgible](../n8n-on-edgible/README.md) publishes one process on port `5678` twice: the editor with `org`, and a webhook hostname with `None`. [Tear down n8n](../n8n-on-edgible/06-n8n-teardown.md) deleted those hostnames and stopped the container. This chapter takes that pattern from [cards](https://github.com/Edgible/cards) and publishes the two apps again.

The card starts from the Compose file n8n publishes. The files and the edits are on the [n8n card](https://github.com/Edgible/cards/blob/main/cards/n8n/README.md). Both apps are place `workhorse`. This chapter maps that place to `minipc`.

![The n8n card lists two apps in one place, and no hostnames. Place workhorse is one serving device: n8n is n8n editor on port 5678, org login. n8n-hooks is n8n webhooks, same process as n8n on port 5678, open to anyone. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/cards/n8n/images/card-light.svg#only-light)
![The n8n card lists two apps in one place, and no hostnames. Place workhorse is one serving device: n8n is n8n editor on port 5678, org login. n8n-hooks is n8n webhooks, same process as n8n on port 5678, open to anyone. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/cards/n8n/images/card-dark.svg#only-dark)

**Where you run this:** the **Ubuntu guest**. The n8n hostnames are gone. The [n8n card](https://github.com/Edgible/cards/blob/main/cards/n8n/README.md) fetches the Compose file.

## 2.1 The job

You fetch the n8n card, follow its README, generate `~/n8n.stack.yml` from the card, and deploy it.

**Done when**

- `~/n8n-card.yml` lists `n8n` on port `5678` with `org`, and `n8n-hooks` on port `5678` with `none`.
- Both name `docker.n8n.io/n8nio/n8n`. `n8n` also names `postgres:18`.
- The card has no `deviceName`, no `<org>.edgible.com` hostname, and no organization id.
- The card has no `resources` section. The Compose file and `init-data.sh` sit in the card directory.
- Both have `place: workhorse`.
- `ss` shows `127.0.0.1:5678`, and nothing is listening on `5432`.
- `edgible stack validate -f ~/n8n.stack.yml` reports 2 applications: `n8n`, `n8n-hooks`.
- `edgible app list` shows `n8n` with `org` and `n8n-hooks` with `None`.

**Need first:** [Tear down n8n](../n8n-on-edgible/06-n8n-teardown.md), including the serving agent still installed. One published app stays, such as `hello-world`, so the [n8n card](https://github.com/Edgible/cards/blob/main/cards/n8n/README.md) can read your org label. That page fetches the Compose file, so `~/n8n` does not have to already be the gold file.

**Not this chapter:** a second copy of the card, a cron workflow, or a webhook workflow. The file is [cards/n8n/card.yml](https://github.com/Edgible/cards/blob/main/cards/n8n/card.yml). [card-to-stack.py](https://github.com/Edgible/cards/blob/main/tools/card-to-stack.py) writes the stack file from that card. The timezone in [n8n on the VM](../n8n-on-edgible/01-n8n-on-the-vm.md) stays off the card.

## 2.2 Fetch the n8n card

The field meanings are the same as [The website card](01-website-card.md). The files and the edits are on the [n8n card](https://github.com/Edgible/cards/blob/main/cards/n8n/README.md). If a setup you already run uses a different file, edit the card in [cards](https://github.com/Edgible/cards).

On the guest:

```bash
curl -fsSL https://raw.githubusercontent.com/Edgible/cards/main/cards/n8n/card.yml -o ~/n8n-card.yml
```

`n8n-hooks` is not a second program. It is the webhook hostname on the same process as `n8n`, the split from [Public webhook hostname](../n8n-on-edgible/03-n8n-public-webhook-hostname.md). `none` in the file is the auth mode `None`. `org` is the auth mode `org`.

`from` is the image name. `place` is `workhorse` on both apps because they are one process, so they stay on one serving device. Workflows in an older `n8n_data` volume stay on disk. This card uses the volume `n8n_storage`.

## 2.3 Start the container

The Compose file and the edits are on the [n8n card](https://github.com/Edgible/cards/blob/main/cards/n8n/README.md). Follow that page. It fetches the files and runs `tailor.sh`. An existing `~/n8n/docker-compose.yml` from [n8n on the VM](../n8n-on-edgible/01-n8n-on-the-vm.md) is replaced.

Start it:

```bash
docker compose -f ~/n8n/docker-compose.yml up -d
docker compose -f ~/n8n/docker-compose.yml ps
ss -ltnp | grep 5678
ss -ltnp | grep 5432
curl -sS -o /dev/null -w "%{http_code}\n" http://127.0.0.1:5678/
```

`127.0.0.1:5678` is listening. `5432` is not. `curl` prints `200` or a 3xx. The Compose process list shows `n8n`, `postgres`, and `n8n-runner`.

## 2.4 Generate the stack file and deploy it

The port from 2.3 is listening. `edgible stack deploy` reads a stack file, and each app in it is `pre-existing`, so deploy publishes that port twice. [card-to-stack.py](https://github.com/Edgible/cards/blob/main/tools/card-to-stack.py) writes that file from the card. It reads `~/n8n-card.yml`, takes the organization id from `edgible config get organizationId`, and writes one Application document per app. `--device minipc` places both on the serving device from [Start here](../start-here/01-edgible-on-vm.md). Auth mode `org` in the card is written `edgible-login` in the stack file.

On the guest:

```bash
curl -fsSL https://raw.githubusercontent.com/Edgible/cards/main/tools/card-to-stack.py -o ~/card-to-stack.py
python3 ~/card-to-stack.py ~/n8n-card.yml --device minipc > ~/n8n.stack.yml
edgible stack validate -f ~/n8n.stack.yml
edgible stack deploy -f ~/n8n.stack.yml
edgible app list
```

The report says 2 applications, `n8n` and `n8n-hooks`, each `pre-existing`. `edgible app list` shows `n8n` with `org` and `n8n-hooks` with `None`, both on port `5678`.

## Verify

- [ ] `grep -nE 'name: (n8n|n8n-hooks)|port:|authModes:' ~/n8n-card.yml` shows the two apps, port `5678` twice, and auth modes `org` and `none`.
- [ ] `grep -nE 'from:|database:' ~/n8n-card.yml` shows `docker.n8n.io/n8nio/n8n` twice and `postgres:18` once.
- [ ] `grep -nE 'deviceName|organization' ~/n8n-card.yml` prints nothing.
- [ ] `grep -n 'edgible.com' ~/n8n-card.yml` prints nothing.
- [ ] `grep -nE 'resources:|compose:|changes:' ~/n8n-card.yml` prints nothing.
- [ ] `grep -n 'place:' ~/n8n-card.yml` shows `workhorse` for both.
- [ ] `ss -ltnp | grep 5678` shows `127.0.0.1:5678`. `ss -ltnp | grep 5432` prints nothing.
- [ ] `edgible stack validate -f ~/n8n.stack.yml` reports 2 applications: `n8n`, `n8n-hooks`.
- [ ] `edgible app list` shows `n8n` with `org` and `n8n-hooks` with `None`.

## Next

[3. The assistant card](03-assistant-card.md). Series: [README](README.md). The website card is [The website card](01-website-card.md).
