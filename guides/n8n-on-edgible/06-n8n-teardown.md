# 6. Tear down n8n

**Remove both public hostnames before you stop watching the VM.**

## 6.0 Why

A demo webhook left active is a live public endpoint on a box you own, and an active schedule keeps firing after you stop watching the VM. This is also a shared box: it may still be running [OpenClaw on Edgible](../openclaw-on-edgible/README.md) and [LLM on Edgible](../llm-on-edgible/README.md), so the default here is n8n only. The order matters: the `None` hostname comes down before the `org` one. Leave `openclaw-ui`, `ollama` and `hello-world` alone, and leave the Edgible serving agent installed.

**Where you run this:** unpublishing in the **n8n editor** on the `org` hostname; `edgible` and Docker on the **Ubuntu guest**; the final dead-URL check on a **phone on cellular**.

## 6.1 The job

You stop production schedules and public webhooks, remove the two n8n hostnames, and stop the Docker process on loopback `5678`. Cellular n8n / `n8n-hooks` should fail. OpenClaw and Hello World still work if you left them.

**Done when**

- `edgible app list` has no n8n and no `n8n-hooks`.
- `ss -ltnp | grep 5678` is empty; nothing listens on `5678`.
- The `n8n-hooks` `/webhook/…` URL on cellular does not return the smoke JSON (no app, or the connection fails).
- `openclaw-ui` / `ollama` / `hello-world` are unchanged if you had created them (unless you chose 6.5).
- Port `5678` is still not forwarded.

**Need first:** You finished enough of this series that n8n exists (at least [chapter 1](01-n8n-on-the-vm.md)). Skip apps you never created.

**Not this chapter:** deleting the Ubuntu VM, OpenClaw teardown ([OpenClaw chapter 9](../openclaw-on-edgible/09-openclaw-teardown.md)), or `edgible auth logout`.

## 6.2 Unpublish workflows (org editor)

Do this before deleting the editor app, while you can still open `https://n8n.<org>.edgible.com`.

In n8n 2.x: open each workflow → **⋯** → **Unpublish** (cron from [chapter 4](04-n8n-cron.md), webhook from [chapter 5](05-n8n-public-webhook.md)). Overview → **Workflows** → **⋯** on the row does the same. Older 1.x: turn **Active** off.

Unpublish stops production ticks and the public path. It does not delete the workflow. If the editor is already gone, skip this. Deleting `n8n-hooks` is what removes the public endpoint.

## 6.3 Delete the Edgible apps

`n8n-hooks` first (the `None` hostname), then n8n (`org`). One process, two auth modes. Delete the `None` hostname first.

```bash
edgible app list
edgible app delete --name n8n-hooks
edgible app delete --name n8n
edgible app list
```

Skip a name if `delete` says it does not exist. You want neither n8n nor `n8n-hooks`. Do not delete `hello-world`, `openclaw-ui`, or `ollama`.

## 6.4 Stop the container (Ubuntu VM)

```bash
cd ~/n8n
docker compose down
ss -ltnp | grep 5678
```

**Smoke test.** Empty `ss` is success, and the `n8n-hooks` URL on cellular should no longer return your JSON.

The compose file in `~/n8n` can stay on disk.

Optional: wipe n8n’s volume (owner account, credentials, workflow JSON on this VM):

```bash
cd ~/n8n
docker compose down -v
```

That does not remove the Edgible apps; do 6.3 first (or the hostnames 404 onto nothing).

## 6.5 Optional — Hello World too

Only if you also want the shared public page gone. Skip this if OpenClaw or LLM-on-Edgible still uses this VM.

```bash
edgible app delete --name hello-world
docker stop hello-world && docker rm hello-world
```

Do not `edgible agent uninstall` here.

### Verify

- [ ] `edgible app list` has no n8n and no `n8n-hooks`.
- [ ] `ss -ltnp | grep 5678` is empty; nothing listens on `5678`.
- [ ] The `n8n-hooks` `/webhook/…` URL on cellular does not return the smoke JSON (no app, or the connection fails).
- [ ] `openclaw-ui` / `ollama` / `hello-world` are unchanged if you had created them (unless you chose 6.5).
- [ ] Port `5678` is still not forwarded.

---

## Next

Series index: [README](README.md). Control UI: [OpenClaw on Edgible](../openclaw-on-edgible/README.md). Published model: [LLM on Edgible](../llm-on-edgible/README.md).
