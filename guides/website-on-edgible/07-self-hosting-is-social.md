# 7. Self Hosting is Social

**One card is the website pattern you can hand to someone else, and the file that puts those four apps back.**

## 7.0 Why

Chapters 1 to 5 created the website as four prompt answers: `site`, `analytics`, `umami` and `status`. Chapter 6 deleted the hostnames and stopped the containers. The pattern is still those four answers. A hostname such as `site.<org>.edgible.com` and the serving device name `minipc` were yours. They do not belong in the file you hand over.

A card is the four apps written down once: the Edgible name, what the software is, the image it comes from, the port, and the auth mode. The copy you share leaves the device name, the hostnames and the organization id out. This chapter writes that card, starts the containers again, and deploys the stack file the card becomes, so the four hostnames exist again.

![The website card lists four apps and no hostnames. site is nginx serving your files on port 8080, open to anyone. analytics is the Umami tracking script on port 3000, open to anyone. umami is the Umami dashboard on that same port, with Postgres, behind an org login. status is Uptime Kuma on port 3001, behind an org login. The card names no device and no organization.](../../images/diagrams/website-on-edgible-07-light.svg#only-light)
![The website card lists four apps and no hostnames. site is nginx serving your files on port 8080, open to anyone. analytics is the Umami tracking script on port 3000, open to anyone. umami is the Umami dashboard on that same port, with Postgres, behind an org login. status is Uptime Kuma on port 3001, behind an org login. The card names no device and no organization.](../../images/diagrams/website-on-edgible-07-dark.svg#only-dark)

**Where you run this:** the **Ubuntu guest**. The four apps are gone. The Compose files from chapters 1, 3 and 5 are still on disk.

## 7.1 The job

You write `~/website-card.yml`, start nginx, Umami and Uptime Kuma, generate `~/website.stack.yml`, and deploy it.

**Done when**

- `~/website-card.yml` lists `site` on port `8080` with `none`, `analytics` on port `3000` with `none`, `umami` on port `3000` with `org`, and `status` on port `3001` with `org`.
- Each app has a `what` line and a `from` line. `umami` also names `postgres:15-alpine`. `analytics` names the same Umami image as `umami`.
- The card has no `deviceName`, no `edgible.com` hostname, and no organization id.
- `ss` shows `127.0.0.1:8080`, `127.0.0.1:3000` and `127.0.0.1:3001`.
- `edgible stack validate -f ~/website.stack.yml` reports 4 applications: `site`, `analytics`, `umami`, `status`.
- `edgible app list` shows those four apps again.

**Need first:** [6. Tear down the website stack](06-website-teardown.md), including the serving agent still installed. If you removed `~/site`, `~/umami` or `~/uptime-kuma`, put those Compose files back from chapters 1, 3 and 5 before 7.3. `hello-world` can stay.

**Not this chapter:** a command that writes the card for you. [card-to-stack.py](card-to-stack.py) writes the stack file. The card itself you write here.

## 7.2 Write the website card

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

  - name: analytics
    what: Umami tracking script, same process as umami
    from: ghcr.io/umami-software/umami:postgresql-latest
    port: 3000
    protocol: https
    subtype: existing
    published: true
    authModes: [none]

  - name: umami
    what: Umami dashboard
    from: ghcr.io/umami-software/umami:postgresql-latest
    database: postgres:15-alpine
    port: 3000
    protocol: https
    subtype: existing
    published: true
    authModes: [org]

  - name: status
    what: Uptime Kuma
    from: louislam/uptime-kuma:1
    port: 3001
    protocol: https
    subtype: existing
    published: true
    authModes: [org]
YAML
```

`what` is the software. `from` is the image. `umami` also names its database image, because that dashboard does not run alone. `analytics` is not a second program: it is the tracking script from that same Umami image.

`none` in the file is the auth mode `None`. `org` is the auth mode `org`. `analytics` and `umami` are the split surface from chapter 4: one port, two auth modes. `subtype: existing` means the process is already listening. The Compose files hold the volumes and the passwords. The card names the images and leaves those secrets out.

**Smoke test.** On the guest:

```bash
grep -nE 'name: (site|analytics|umami|status)|port:|authModes:' ~/website-card.yml
grep -nE 'deviceName|edgible\.com|organization' ~/website-card.yml
```

Four names, ports `8080`, `3000`, `3000` and `3001`, and the four `authModes` lines. The second `grep` prints nothing.

## 7.3 Start the containers

The stack file publishes ports that are already listening. It does not pull the images or start them. On the guest:

```bash
docker compose -f ~/site/docker-compose.yml up -d
docker compose -f ~/umami/docker-compose.yml up -d
docker compose -f ~/uptime-kuma/docker-compose.yml up -d
ss -ltnp | grep -E '8080|3000|3001'
```

`127.0.0.1:8080`, `127.0.0.1:3000` and `127.0.0.1:3001` are listening. If chapter 6 removed the Umami tracking snippet from your pages, put it back from [4. Publish Umami](04-publish-umami.md) when you want page views again. The hostnames publish either way.

## 7.4 Generate the stack file and deploy it

`edgible stack validate` reads a deploy document. Run it on the card:

```bash
edgible stack validate -f ~/website-card.yml
```

The command exits with an error. The report says it expected `apiVersion: v3` and `kind: Application`. That is the document `edgible stack deploy` accepts. The card stays as written.

[card-to-stack.py](card-to-stack.py) is the stand-in for a later `edgible stack export --card`. It reads the card, takes the organization id from `edgible config get organizationId`, and writes one Application document per app. `--device minipc` places all four on the serving device from [Start here](../start-here/01-edgible-on-vm.md). Auth mode `org` is written `edgible-login`.

On the guest:

```bash
curl -fsSL https://guides.edgible.com/guides/website-on-edgible/card-to-stack.py -o ~/card-to-stack.py
python3 ~/card-to-stack.py ~/website-card.yml --device minipc > ~/website.stack.yml
edgible stack validate -f ~/website.stack.yml
edgible stack deploy -f ~/website.stack.yml
edgible app list
```

`python3 --version` prints a version. Ubuntu includes it. Validate reports 4 applications, `site`, `analytics`, `umami` and `status`, each `pre-existing`. Deploy waits until those apps are published. `edgible app list` shows them again: `site` and `analytics` with `None`, `umami` and `status` with `org`.

A different device for one app is `--device status=monitor` alongside `--device minipc` for the rest.

## Verify

- [ ] `grep -nE 'name: (site|analytics|umami|status)|port:|authModes:' ~/website-card.yml` shows the four apps, ports `8080`, `3000`, `3000`, `3001`, and auth modes `none`, `none`, `org`, `org`.
- [ ] `grep -nE 'what:|from:|database:' ~/website-card.yml` shows `nginx:alpine`, the Umami image on both `analytics` and `umami`, `postgres:15-alpine`, and `louislam/uptime-kuma:1`.
- [ ] `grep -nE 'deviceName|edgible\.com|organization' ~/website-card.yml` prints nothing.
- [ ] `ss -ltnp | grep -E '8080|3000|3001'` shows `127.0.0.1` on each port.
- [ ] `edgible stack validate -f ~/website-card.yml` exits with an error that names `v3` and `Application`.
- [ ] `edgible stack validate -f ~/website.stack.yml` reports 4 applications: `site`, `analytics`, `umami`, `status`.
- [ ] `edgible app list` shows `site`, `analytics`, `umami` and `status` again.

## Next

[Start here](../start-here/README.md) still has the VM and the serving agent ready. The other guides go further with the same machine: [n8n on Edgible](../n8n-on-edgible/README.md) publishes one process on two hostnames with two auth modes, [OpenClaw on Edgible](../openclaw-on-edgible/README.md) puts an agent on your phone, and [LLM on Edgible](../llm-on-edgible/README.md) publishes a model on your own hardware. Series: [README](README.md).
