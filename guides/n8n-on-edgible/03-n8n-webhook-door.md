# 3. Public webhook door

**One n8n, two front doors — and only one of them has a lock.**

## 3.0 Why

A robot cannot log in. Stripe, GitHub and a `curl` from a café have no browser, no password and no patience for your organisation’s sign-in page, so on the **org** hostname from chapter 2 every one of them stops at the login screen. That is the lock doing its job, not a bug — but it also means you have no inbound door at all yet.

There are two tempting ways out and both are wrong. Setting the editor app to **None** does open the door, and it opens it onto your canvas, your credentials and every workflow you will ever write — this is the cardinal sin the series exists to prevent. Carving out one public path on the org hostname is not on offer either: Edgible auth is a property of the **app**, that is the hostname, not of a path inside it. So with a single hostname you can only choose which side to break: locked webhooks, or an unlocked canvas.

Edgible’s answer is that hostnames are cheap and locks are per hostname. You point a **second** app at the very same container on port **5678**, name it **n8n-hooks**, and give it **None**. One process, two doors, two different locks. All `WEBHOOK_URL` does after that is tell n8n which origin to *print* on its webhook nodes; the traffic still lands on the same process either way.

```
you, on cellular       https://n8n.<org>.edgible.com        ← org login
                                 │
Ubuntu guest           Edgible serving agent ──► 127.0.0.1:5678
                                 │
                       n8n  (one process · canvas · credentials · workflows)
                                 ▲
Stripe / GitHub        https://n8n-hooks.<org>.edgible.com  ← None   (this chapter)
```

**Where you run this:** `edgible` and the compose edit on the **Ubuntu guest**; the certificate check in the **host browser**; the editor re-check on your **phone**.

## 3.1 The job

Stripe, GitHub, and `curl` from a café will not pass **Edgible org**. You add a second application on the **same** port **5678**, named **n8n-hooks**, with **None**. Then you tell n8n that webhook URLs are that origin (`WEBHOOK_URL`). The editor stays `n8n.<org>…` with **org**.

Anyone who learns a workflow’s webhook path can hit it. Use a throwaway path, deactivate when done, do not put secrets in the JSON you return.

**Done when**

- `edgible app list` shows **n8n** (**org**) and **n8n-hooks** (**None**), both port **5678**.
- Both certificates are issued.
- `~/n8n/docker-compose.yml` has `WEBHOOK_URL=https://n8n-hooks.<org>.edgible.com/` (trailing slash, **no** `:5678`).
- `N8N_EDITOR_BASE_URL` / `N8N_HOST` are the **editor** host.
- `docker compose up -d` has been run again, and the phone still opens the **org** editor.
- Hello World still loads. Port **5678** not forwarded.

**Need first:** [2. n8n editor through Edgible](02-n8n-editor-through-edgible.md). Leave both n8n Docker and **hello-world** running.

**Not this chapter:** building a workflow (that is [4](04-n8n-cron.md) and [5](05-n8n-public-webhook.md)), OpenClaw, or putting the **editor** on None.

## 3.2 Create n8n-hooks

Same device, same port, different name and auth:

```bash
edgible device list
edgible app create existing \
  --name n8n-hooks \
  --port 5678 \
  --auth-modes none \
  --device-id <mini-pc-id>
```

Wait for the certificate (console → **n8n-hooks**), same as Hello World.

```bash
edgible app list
```

Copy **https://n8n-hooks.YOUR-ORG.edgible.com** exactly (no path). If the CLI refuses a second app on **5678**, stop — this series needs two hostnames; do not “fix” it by setting the **n8n** editor app to None.

## 3.3 Point n8n at the two origins

On the VM, edit `~/n8n/docker-compose.yml`. Keep the loopback publish. Add/set:

```yaml
    environment:
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - N8N_PROXY_HOPS=1
      - N8N_HOST=n8n.YOUR-ORG.edgible.com
      - N8N_EDITOR_BASE_URL=https://n8n.YOUR-ORG.edgible.com/
      - WEBHOOK_URL=https://n8n-hooks.YOUR-ORG.edgible.com/
      - GENERIC_TIMEZONE=Australia/Adelaide
      - TZ=Australia/Adelaide
      - N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true
```

Replace `YOUR-ORG` with the labels from `edgible app list`. Trailing slashes on the two `https://` URLs. **No** `:5678` on those URLs.

```bash
cd ~/n8n
docker compose up -d
docker compose ps
```

**Smoke test.** Hard-refresh the **org** editor on the phone. Canvas should still load. Webhook nodes will still be empty until [chapter 5](05-n8n-public-webhook.md); you are only setting the base URL.

### Verify

- [ ] `edgible app list` shows **n8n** (**org**) and **n8n-hooks** (**None**), both port **5678**.
- [ ] Both certificates are issued.
- [ ] `~/n8n/docker-compose.yml` has `WEBHOOK_URL=https://n8n-hooks.<org>.edgible.com/` (trailing slash, **no** `:5678`).
- [ ] `N8N_EDITOR_BASE_URL` / `N8N_HOST` are the **editor** host.
- [ ] `docker compose up -d` has been run again, and the phone still opens the **org** editor.
- [ ] Hello World still loads. Port **5678** not forwarded.

---

## Next

[4. A cron workflow](04-n8n-cron.md). Series: [README](README.md).
