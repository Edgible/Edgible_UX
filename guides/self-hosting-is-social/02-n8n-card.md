# 2. The n8n card

**One n8n process, two auth modes, written as a card that starts from n8n's own Compose file.**

## 2.0 Why

[n8n on Edgible](../n8n-on-edgible/README.md) publishes one process on port `5678` twice: the editor with `org`, and a webhook hostname with `None`. [Tear down n8n](../n8n-on-edgible/06-n8n-teardown.md) deleted those hostnames and stopped the container. This chapter takes that pattern from [cards](https://github.com/Edgible/cards) and publishes the two apps again.

The card assumes the Compose file n8n publishes, not the shorter file those chapters pasted by hand. That published file runs Postgres and a task runner, and it binds port `5678` on every interface. The `changes` list is the edit that makes it this pattern: loopback only, generated secrets, and the editor hostname kept apart from the webhook hostname. Both apps are place `workhorse`. This chapter maps that place to `minipc`.

![The n8n card lists two apps in one place, and no hostnames. Place workhorse is one serving device: n8n is n8n editor on port 5678, org login. n8n-hooks is n8n webhooks, same process as n8n on port 5678, open to anyone. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/cards/n8n/card-light.svg#only-light)
![The n8n card lists two apps in one place, and no hostnames. Place workhorse is one serving device: n8n is n8n editor on port 5678, org login. n8n-hooks is n8n webhooks, same process as n8n on port 5678, open to anyone. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/cards/n8n/card-dark.svg#only-dark)

**Where you run this:** the **Ubuntu guest**. The n8n hostnames are gone. The Compose file is fetched in 2.3 from the URL in the card.

## 2.1 The job

You fetch the n8n card, fetch n8n's Compose file and apply its `changes`, generate `~/n8n.stack.yml` from the card, and deploy it.

**Done when**

- `~/n8n-card.yml` lists `n8n` on port `5678` with `org`, and `n8n-hooks` on port `5678` with `none`.
- Both name `docker.n8n.io/n8nio/n8n`. `n8n` also names `postgres:18`.
- The card has no `deviceName`, no `<org>.edgible.com` hostname, and no organization id.
- Both applications name the same GitHub Compose URL, the same `.env` and `init-data.sh` URLs, and the same `changes`.
- Both have `place: workhorse`.
- `ss` shows `127.0.0.1:5678`, and nothing is listening on `5432`.
- `edgible stack validate -f ~/n8n.stack.yml` reports 2 applications: `n8n`, `n8n-hooks`.
- `edgible app list` shows `n8n` with `org` and `n8n-hooks` with `None`.

**Need first:** [Tear down n8n](../n8n-on-edgible/06-n8n-teardown.md), including the serving agent still installed. One published app stays, such as `hello-world`, so 2.3 can read your org label. 2.3 fetches the Compose file, so `~/n8n` does not have to already be the gold file.

**Not this chapter:** a second copy of the card, a cron workflow, or a webhook workflow. The file is [cards/n8n/card.yml](https://github.com/Edgible/cards/blob/main/cards/n8n/card.yml). [card-to-stack.py](https://github.com/Edgible/cards/blob/main/tools/card-to-stack.py) writes the stack file from that card. The timezone in [n8n on the VM](../n8n-on-edgible/01-n8n-on-the-vm.md) stays off the card.

## 2.2 Fetch the n8n card

The field meanings are the same as [The website card](01-website-card.md). This card is the gold-file assumption for an `existing` app: `compose` is the public file for the image, and `changes` is what you edit before you run it. If a setup you already run uses a different file, edit the card in [cards](https://github.com/Edgible/cards). Point `compose` at that file and drop `changes`, or keep this URL and add a line.

On the guest:

```bash
curl -fsSL https://raw.githubusercontent.com/Edgible/cards/main/cards/n8n/card.yml -o ~/n8n-card.yml
```

`n8n-hooks` is not a second program. It is the webhook hostname on the same process as `n8n`, the split from [Public webhook hostname](../n8n-on-edgible/03-n8n-public-webhook-hostname.md). `none` in the file is the auth mode `None`. `org` is the auth mode `org`.

`from` is the image name. The tag is the `N8N_VERSION` line in the gold `.env`, left as n8n published it. `database` matches the `postgres` image in that same Compose file. The file also starts `n8nio/runners`. `place` is `workhorse` on both apps because they are one process, so they stay on one serving device.

The Compose URL is listed twice and downloaded once. `files` are the `.env` and `init-data.sh` that file expects beside it. `env` names the values to generate. The card does not carry those values, the org label, or the volume data. Workflows in an older `n8n_data` volume stay on disk. This file uses the volume `n8n_storage`.

## 2.3 Start the container

Fetch the gold file and the two files it mounts, then apply the `changes`. An existing `~/n8n/docker-compose.yml` from [n8n on the VM](../n8n-on-edgible/01-n8n-on-the-vm.md) is replaced. The org label comes from a hostname you already have.

On the guest:

```bash
mkdir -p ~/n8n
curl -fsSL https://raw.githubusercontent.com/n8n-io/n8n-hosting/main/docker-compose/withPostgres/docker-compose.yml -o ~/n8n/docker-compose.yml
curl -fsSL https://raw.githubusercontent.com/n8n-io/n8n-hosting/main/docker-compose/withPostgres/.env -o ~/n8n/.env
curl -fsSL https://raw.githubusercontent.com/n8n-io/n8n-hosting/main/docker-compose/withPostgres/init-data.sh -o ~/n8n/init-data.sh
chmod +x ~/n8n/init-data.sh
sed -i 's/- 5678:5678/- 127.0.0.1:5678:5678/' ~/n8n/docker-compose.yml
if grep -qE 'changePassword|changeRunnerAuthToken' ~/n8n/.env; then
  postgres_password=$(openssl rand -hex 16)
  postgres_non_root_password=$(openssl rand -hex 16)
  runners_auth_token=$(openssl rand -hex 32)
  sed -i \
    -e "s/^POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=${postgres_password}/" \
    -e "s/^POSTGRES_NON_ROOT_PASSWORD=.*/POSTGRES_NON_ROOT_PASSWORD=${postgres_non_root_password}/" \
    -e "s/^RUNNERS_AUTH_TOKEN=.*/RUNNERS_AUTH_TOKEN=${runners_auth_token}/" \
    ~/n8n/.env
  chmod 600 ~/n8n/.env
fi
org=$(edgible app list --json | python3 -c '
import json, sys
apps = json.load(sys.stdin)
hosts = [h for app in apps for h in (app.get("hostnames") or [])]
if not hosts:
    sys.exit("need one published app so the org label is known")
print(hosts[0].split(".", 1)[1].removesuffix(".edgible.com"))
')
if ! grep -q '^      - WEBHOOK_URL=' ~/n8n/docker-compose.yml; then
  sed -i "/N8N_RUNNERS_BROKER_LISTEN_ADDRESS=0.0.0.0/a\\
      - N8N_PROXY_HOPS=1\\
      - N8N_PROTOCOL=https\\
      - N8N_HOST=n8n.${org}.edgible.com\\
      - N8N_EDITOR_BASE_URL=https://n8n.${org}.edgible.com/\\
      - WEBHOOK_URL=https://n8n-hooks.${org}.edgible.com/" ~/n8n/docker-compose.yml
fi
```

**Smoke test.** On the guest:

```bash
echo "$org"
grep -n '127.0.0.1:5678:5678' ~/n8n/docker-compose.yml
grep -nE 'changePassword|changeRunnerAuthToken' ~/n8n/.env
grep -nE 'N8N_HOST=|N8N_EDITOR_BASE_URL=|WEBHOOK_URL=' ~/n8n/docker-compose.yml
```

`echo` prints one label, not a hostname. The port line is bound to loopback. The password `grep` prints nothing. `N8N_HOST` and `N8N_EDITOR_BASE_URL` use `n8n.<org>.edgible.com`. `WEBHOOK_URL` uses `n8n-hooks.<org>.edgible.com`, with a trailing slash and no `:5678`.

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
- [ ] `grep -n 'compose:' ~/n8n-card.yml` shows `https://raw.githubusercontent.com/n8n-io/n8n-hosting/main/docker-compose/withPostgres/docker-compose.yml` under both apps.
- [ ] `grep -n 'place:' ~/n8n-card.yml` shows `workhorse` for both.
- [ ] `ss -ltnp | grep 5678` shows `127.0.0.1:5678`. `ss -ltnp | grep 5432` prints nothing.
- [ ] `edgible stack validate -f ~/n8n.stack.yml` reports 2 applications: `n8n`, `n8n-hooks`.
- [ ] `edgible app list` shows `n8n` with `org` and `n8n-hooks` with `None`.

## Next

[Self Hosting is Social](README.md). The website card is [The website card](01-website-card.md).
