# 1. The website card

**A website others can reproduce: the site, the analytics and the monitor, written as one card.**

## 1.0 Why

[Website on Edgible](../website-on-edgible/README.md) is four apps: a public site, an open tracking script, a locked analytics dashboard, and a locked uptime monitor. [Tear down the website stack](../website-on-edgible/06-website-teardown.md) deleted the hostnames and stopped the containers. This chapter writes that website as a card and publishes the four apps again.

The card for this example has two places. `site`, `analytics`, and `umami` are `web`. `analytics` and `umami` share port `3000`, so they stay on one serving device. `status` is `monitor`, which can be that same device or a second one. This chapter maps both places to `minipc`.

![The website card lists four apps in two places, and no hostnames. Place web is one serving device: site is nginx serving your files on port 8080, open to anyone. analytics is the Umami tracking script on port 3000, open to anyone. umami is the Umami dashboard on that same port, with Postgres, behind an org login. Place monitor may be a second serving device: status is Uptime Kuma on port 3001, behind an org login. The card names no device and no organization.](../../images/diagrams/self-hosting-is-social-01-light.svg#only-light)
![The website card lists four apps in two places, and no hostnames. Place web is one serving device: site is nginx serving your files on port 8080, open to anyone. analytics is the Umami tracking script on port 3000, open to anyone. umami is the Umami dashboard on that same port, with Postgres, behind an org login. Place monitor may be a second serving device: status is Uptime Kuma on port 3001, behind an org login. The card names no device and no organization.](../../images/diagrams/self-hosting-is-social-01-dark.svg#only-dark)

**Where you run this:** the **Ubuntu guest**. The four apps are gone. The Compose files are fetched in 1.3 from the URLs in the card.

## 1.1 The job

You write the website card by hand, start nginx, Umami and Uptime Kuma, generate `~/website.stack.yml` from the card, and deploy it.

**Done when**

- `~/website-card.yml` lists `site` on port `8080` with `none`, `analytics` on port `3000` with `none`, `umami` on port `3000` with `org`, and `status` on port `3001` with `org`.
- Each app has a `what` line and a `from` line. `umami` also names `postgres:15-alpine`. `analytics` names the same Umami image as `umami`. That image is `ghcr.io/umami-software/umami:latest`. `status` names `louislam/uptime-kuma:2`.
- The card has no `deviceName`, no `<org>.edgible.com` hostname, and no organization id. The only `edgible.com` names are `https://guides.edgible.com` URLs.
- Each application has a `resources` section. `site` names the guides Compose URL and has no `changes`. `analytics` and `umami` name the Umami GitHub Compose URL and the same `changes`. `status` names the Uptime Kuma GitHub Compose URL and its `changes`.
- `site`, `analytics` and `umami` have `place: web`. `status` has `place: monitor`.
- `ss` shows `127.0.0.1:8080`, `127.0.0.1:3000` and `127.0.0.1:3001`.
- `edgible stack validate -f ~/website.stack.yml` reports 4 applications: `site`, `analytics`, `umami`, `status`.
- `edgible app list` shows those four apps again.

**Need first:** [Tear down the website stack](../website-on-edgible/06-website-teardown.md), including the serving agent still installed. `hello-world` can stay. 1.3 fetches the Compose files, so those directories do not have to already be on disk.

**Not this chapter:** a tool that writes the card. You write `~/website-card.yml` by hand. [card-to-stack.py](card-to-stack.py) writes the stack file from that card.

## 1.2 Write the website card

You write this file by hand. Later, a tool will generate a card from a setup you already run. Until then you can also ask an AI to draft the YAML from a description of the apps. [Working with an AI tool](../../working-with-ai.md) is how these guides are meant to be read alongside one. However the file is produced, the names, the ports and the auth modes below are what you check before you share it.

On the guest:

```bash
cat > ~/website-card.yml <<'YAML'
apiVersion: v1
kind: Card
metadata:
  name: website
  description: Public site, open tracker, locked dashboard, locked monitor

applications:
  - name: site
    what: your static files, served by nginx
    from: nginx:alpine
    port: 8080
    protocol: https
    subtype: existing
    published: true
    authModes: [none]
    place: web
    resources:
      compose: https://guides.edgible.com/guides/self-hosting-is-social/compose/site/docker-compose.yml
      files:
        - https://guides.edgible.com/guides/self-hosting-is-social/compose/site/public/index.html

  - name: analytics
    what: Umami tracking script, same process as umami
    from: ghcr.io/umami-software/umami:latest
    port: 3000
    protocol: https
    subtype: existing
    published: true
    authModes: [none]
    place: web
    resources:
      compose: https://raw.githubusercontent.com/umami-software/umami/master/docker-compose.yml
      changes:
        - Bind the host port to 127.0.0.1 only
        - Replace the sample database password, APP_SECRET, and TWO_FACTOR_ENCRYPTION_KEY with generated values
      env: [POSTGRES_PASSWORD, APP_SECRET, TWO_FACTOR_ENCRYPTION_KEY]

  - name: umami
    what: Umami dashboard
    from: ghcr.io/umami-software/umami:latest
    database: postgres:15-alpine
    port: 3000
    protocol: https
    subtype: existing
    published: true
    authModes: [org]
    place: web
    resources:
      compose: https://raw.githubusercontent.com/umami-software/umami/master/docker-compose.yml
      changes:
        - Bind the host port to 127.0.0.1 only
        - Replace the sample database password, APP_SECRET, and TWO_FACTOR_ENCRYPTION_KEY with generated values
      env: [POSTGRES_PASSWORD, APP_SECRET, TWO_FACTOR_ENCRYPTION_KEY]

  - name: status
    what: Uptime Kuma
    from: louislam/uptime-kuma:2
    port: 3001
    protocol: https
    subtype: existing
    published: true
    authModes: [org]
    place: monitor
    resources:
      compose: https://raw.githubusercontent.com/louislam/uptime-kuma/master/compose.yaml
      changes:
        - Bind the host port to 127.0.0.1 only
YAML
```

`what` is the software. `from` is the image. `umami` also names its database image, because that dashboard does not run alone. `analytics` is not a second program: it is the tracking script from that same Umami image.

`none` in the file is the auth mode `None`. `org` is the auth mode `org`. `analytics` and `umami` are the split surface from [Publish Umami](../website-on-edgible/04-publish-umami.md): one port, two auth modes.

`place` is the topology. It is not a device name. Applications with the same place run on one serving device, and that device is where the serving agent for those apps runs. `site`, `analytics` and `umami` are `web`, and `analytics` and `umami` have to stay together because they are one process on port `3000`. `status` is `monitor`, so it can live on a second serving device. A monitor on the same machine as the site cannot report that machine going down, which is [What this cannot tell you](../website-on-edgible/05-uptime-kuma.md#55-what-this-cannot-tell-you). This chapter maps both places to `minipc`.

`resources` sits on the application that needs it. `compose` is a public URL. `changes` is the list of edits to make before you run that file, and it is left off when the file is already the one to run. `site` is that case: there is no upstream Compose file for a folder of your pages, so the URL is the file on guides.edgible.com and there is no `changes` list. `files` on `site` is the page nginx serves when `~/site/public` is empty. `analytics` and `umami` list the same Umami URL and the same `changes`, because they are one process. `status` lists the Uptime Kuma URL and the one edit that binds its port to loopback. `env` names the variables to generate into `~/umami/.env`. The card does not carry the values or the volume data.

`subtype: existing` on every app means a process is already listening on that port. The card only records the port. nginx, Umami and Uptime Kuma are still stopped, from [Tear down the website stack](../website-on-edgible/06-website-teardown.md). The next step starts them, so those ports have something listening before you publish.

## 1.3 Start the containers

Fetch each `compose` URL. `site` is ready to run. Apply the `changes` on the Umami and Uptime Kuma files before starting them. The Umami URL is listed twice and downloaded once. An existing `~/site/public/index.html` from [The site on the VM](../website-on-edgible/01-site-on-the-vm.md) is left as it is. The sample page is only downloaded when that file is missing.

On the guest:

```bash
mkdir -p ~/site/public ~/umami ~/uptime-kuma
curl -fsSL https://guides.edgible.com/guides/self-hosting-is-social/compose/site/docker-compose.yml -o ~/site/docker-compose.yml
curl -fsSL https://raw.githubusercontent.com/umami-software/umami/master/docker-compose.yml -o ~/umami/docker-compose.yml
curl -fsSL https://raw.githubusercontent.com/louislam/uptime-kuma/master/compose.yaml -o ~/uptime-kuma/compose.yaml
if [ ! -f ~/site/public/index.html ]; then
  curl -fsSL https://guides.edgible.com/guides/self-hosting-is-social/compose/site/public/index.html -o ~/site/public/index.html
fi
sed -i \
  -e 's/"3000:3000"/"127.0.0.1:3000:3000"/' \
  -e 's#postgresql://umami:umami@#postgresql://umami:${POSTGRES_PASSWORD}@#' \
  -e 's/APP_SECRET: replace-me-with-a-random-string/APP_SECRET: ${APP_SECRET}/' \
  -e 's/TWO_FACTOR_ENCRYPTION_KEY: replace-me-with-a-64-character-hex-string/TWO_FACTOR_ENCRYPTION_KEY: ${TWO_FACTOR_ENCRYPTION_KEY}/' \
  -e 's/POSTGRES_PASSWORD: umami/POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}/' \
  ~/umami/docker-compose.yml
sed -i 's/"3001:3001"/"127.0.0.1:3001:3001"/' ~/uptime-kuma/compose.yaml
```

**Smoke test.** On the guest:

```bash
grep -n '127.0.0.1:3000:3000' ~/umami/docker-compose.yml
grep -nE 'replace-me|POSTGRES_PASSWORD: umami' ~/umami/docker-compose.yml
grep -n '127.0.0.1:3001:3001' ~/uptime-kuma/compose.yaml
```

The first `grep` shows the Umami port bound to loopback. The second prints nothing. The third shows the Uptime Kuma port bound to loopback.

Generate the Umami secrets when `~/umami/.env` does not already have them, then start the three Compose files:

```bash
if [ ! -f ~/umami/.env ]; then
  cat > ~/umami/.env <<EOF
POSTGRES_PASSWORD=$(openssl rand -hex 16)
APP_SECRET=$(openssl rand -base64 32)
TWO_FACTOR_ENCRYPTION_KEY=$(openssl rand -hex 32)
EOF
  chmod 600 ~/umami/.env
elif ! grep -q '^TWO_FACTOR_ENCRYPTION_KEY=' ~/umami/.env; then
  echo "TWO_FACTOR_ENCRYPTION_KEY=$(openssl rand -hex 32)" >> ~/umami/.env
fi
docker compose -f ~/site/docker-compose.yml up -d
docker compose -f ~/umami/docker-compose.yml up -d
docker compose -f ~/uptime-kuma/compose.yaml up -d
ss -ltnp | grep -E '8080|3000|3001'
```

`127.0.0.1:8080`, `127.0.0.1:3000` and `127.0.0.1:3001` are listening. If [Tear down the website stack](../website-on-edgible/06-website-teardown.md) removed the Umami tracking snippet from your pages, put it back from [Publish Umami](../website-on-edgible/04-publish-umami.md) when you want page views again. The hostnames publish either way.

## 1.4 Generate the stack file and deploy it

The ports from 1.3 are listening. `edgible stack deploy` reads a stack file, and each app in it is `pre-existing`, so deploy publishes those ports. [card-to-stack.py](card-to-stack.py) writes that file from the card. It reads `~/website-card.yml`, takes the organization id from `edgible config get organizationId`, and writes one Application document per app. `--device minipc` places all four on the serving device from [Start here](../start-here/01-edgible-on-vm.md). Auth mode `org` in the card is written `edgible-login` in the stack file.

Running the script yourself is the current step. Later, `edgible stack export --card` will write the stack file from the card, and this download goes away.

On the guest:

```bash
curl -fsSL https://guides.edgible.com/guides/self-hosting-is-social/card-to-stack.py -o ~/card-to-stack.py
python3 ~/card-to-stack.py ~/website-card.yml --device minipc > ~/website.stack.yml
```

`python3 --version` prints a version. Ubuntu includes it.

**Smoke test.** On the guest:

```bash
edgible stack validate -f ~/website.stack.yml
```

The report says 4 applications, `site`, `analytics`, `umami` and `status`, each `pre-existing`. That is the card, with your device name and your organization id filled in.

Deploy that file:

```bash
edgible stack deploy -f ~/website.stack.yml
edgible app list
```

Deploy waits until those apps are published. `edgible app list` shows them again: `site` and `analytics` with `None`, `umami` and `status` with `org`.

`--device minipc` puts both places on `minipc`. To put the monitor on a second serving device, pass `--device web=minipc --device monitor=otherbox`. `otherbox` has to be a serving device you already have.

## Verify

- [ ] `grep -nE 'name: (site|analytics|umami|status)|port:|authModes:' ~/website-card.yml` shows the four apps, ports `8080`, `3000`, `3000`, `3001`, and auth modes `none`, `none`, `org`, `org`.
- [ ] `grep -nE 'what:|from:|database:' ~/website-card.yml` shows `nginx:alpine`, `ghcr.io/umami-software/umami:latest` on both `analytics` and `umami`, `postgres:15-alpine`, and `louislam/uptime-kuma:2`.
- [ ] `grep -nE 'deviceName|organization' ~/website-card.yml` prints nothing.
- [ ] `grep -n 'edgible.com' ~/website-card.yml | grep -v 'https://guides.edgible.com/'` prints nothing.
- [ ] `grep -n 'compose:' ~/website-card.yml` shows the guides URL under `site`, `https://raw.githubusercontent.com/umami-software/umami/master/docker-compose.yml` under both `analytics` and `umami`, and `https://raw.githubusercontent.com/louislam/uptime-kuma/master/compose.yaml` under `status`.
- [ ] `grep -n 'Bind the host port' ~/website-card.yml` shows that change under `analytics`, `umami`, and `status`, and not under `site`.
- [ ] `grep -n 'place:' ~/website-card.yml` shows `web` for `site`, `analytics` and `umami`, and `monitor` for `status`.
- [ ] `ss -ltnp | grep -E '8080|3000|3001'` shows `127.0.0.1` on each port.
- [ ] `edgible stack validate -f ~/website.stack.yml` reports 4 applications: `site`, `analytics`, `umami`, `status`.
- [ ] `edgible app list` shows `site`, `analytics`, `umami` and `status` again.

## Next

[Start here](../start-here/README.md) still has the VM and the serving agent ready. The other guides go further with the same machine: [n8n on Edgible](../n8n-on-edgible/README.md) publishes one process on two hostnames with two auth modes, [OpenClaw on Edgible](../openclaw-on-edgible/README.md) puts an agent on your phone, and [LLM on Edgible](../llm-on-edgible/README.md) publishes a model on your own hardware. Series: [README](README.md).
