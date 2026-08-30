# 6. Tear down the website stack

**Four hostnames gone, containers stopped, and a deliberate decision about the analytics data.**

## 6.0 Why

Two of the four hostnames this series created are `None`, which means anyone who has the URL can reach them for as long as they exist. A demo left running is a live public endpoint on a box you own, and the Umami login page sits behind one of them.

This is also a shared machine. It may still be running [n8n on Edgible](../n8n-on-edgible/README.md), [OpenClaw on Edgible](../openclaw-on-edgible/README.md) or [LLM on Edgible](../llm-on-edgible/README.md), so the default here is this series only: `hello-world` and the Edgible serving agent stay unless you opt in at the end.

If you built something you actually use, skip this chapter. It is the only series here whose result is worth keeping.

**Where you run this:** `edgible` and Docker on the **Ubuntu guest**, the console in the **host browser** for the final check.

## 6.1 The job

You delete the apps public-first, stop the containers, then decide separately whether the analytics history goes too.

**Done when**

- `edgible app list` no longer shows `site`, `analytics`, `umami` or `status`.
- All four hostnames fail to load from a phone on cellular.
- `docker ps` shows none of `site`, `umami`, `umami-db` or `uptime-kuma`.
- Nothing is listening on `8080`, `3000` or `3001`.
- `hello-world` still loads, and `edgible device health` is still OK, unless you opted out.

**Need first:** nothing beyond having done the series. Doing this out of order is fine, but delete the `None` apps before the `org` ones.

**Not this chapter:** deleting the Ubuntu VM, `edgible auth logout`, or tearing down another series.

## 6.2 Unpublish, public hostnames first

The two `None` apps are the ones a stranger can reach, so they go first:

```bash
edgible app delete --name analytics
edgible app delete --name site
```

Then the two behind `org`:

```bash
edgible app delete --name umami
edgible app delete --name status
```

**Smoke test.** On a phone on cellular, try all four hostnames. Each should fail to load. `edgible app list` on the guest should show neither them nor any leftover certificate entry in the console.

Deleting an app removes the hostname, not the service. Everything is still running locally on the guest, which is the next step and also why unpublishing first is the right order: nothing is reachable from outside while you take the rest down.

## 6.3 Stop the containers

```bash
docker compose -f ~/uptime-kuma/docker-compose.yml down
docker compose -f ~/umami/docker-compose.yml down
docker compose -f ~/site/docker-compose.yml down
```

`down` without `-v` keeps the named volumes, so the Umami database and the Uptime Kuma configuration survive. Bringing any of them back is `docker compose up -d` in that directory, and the history is still there.

**Smoke test.** On the guest:

```bash
docker ps
ss -ltnp | grep -E '8080|3000|3001'
```

None of the four containers, and nothing listening on those ports.

## 6.4 The data, if you want it gone

The volumes hold your analytics history and your monitor configuration. Removing them is separate from everything above because it is the one step that cannot be undone:

```bash
docker volume rm umami_umami-db-data uptime-kuma_uptime-kuma-data
```

Compose prefixes volume names with the project directory, so confirm what you are about to delete with `docker volume ls` first. The site files themselves are just a directory: `rm -rf ~/site` if you want them gone, though your generator source is presumably elsewhere.

Also remove the tracking snippet from your site's source. Leaving it means every visitor's browser tries to fetch a script from a hostname that no longer resolves, which is a failed request on every page load.

## 6.5 What is left, on purpose

`hello-world` is still published, and the Edgible serving agent is still installed and healthy. Both are shared with the other guides, and removing them would break a series you may be part-way through.

If this was the only thing you were doing and you want the machine back:

```bash
edgible app delete --name hello-world
sudo edgible agent uninstall
```

Leave those alone if any other guide is still in progress.

### Verify

- [ ] `edgible app list` shows none of `site`, `analytics`, `umami`, `status`.
- [ ] All four hostnames fail to load on a phone on cellular.
- [ ] `docker ps` shows none of the four containers.
- [ ] Nothing is listening on `8080`, `3000` or `3001`.
- [ ] The tracking snippet is out of your site's source.
- [ ] `hello-world` still loads and `edgible device health` is OK, unless you opted out in 6.5.

## Next

[Start here](../start-here/README.md) still has the VM and the serving agent ready. The other guides go further with the same machine: [n8n on Edgible](../n8n-on-edgible/README.md) publishes one process on two hostnames with two auth modes, [OpenClaw on Edgible](../openclaw-on-edgible/README.md) puts an agent on your phone, and [LLM on Edgible](../llm-on-edgible/README.md) publishes a model on your own hardware. Series: [README](README.md).
