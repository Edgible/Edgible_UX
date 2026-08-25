# 3. Public webhook door

**Same n8n process. Second hostname. Callers that cannot log into your org.**

This is the Edgible trick. One container, port **5678**, two apps: **n8n** stays **org**; **n8n-hooks** is **None**. GitHub never sees a login page; you never put the editor on the public internet. If you only have one hostname, you either lock the webhooks or unlock the canvas. `WEBHOOK_URL` only tells n8n which origin to print — traffic still lands on the same process.

## 3.1 The job

Stripe, GitHub, and `curl` from a café will not pass **Edgible org**. You add a second application on the **same** port **5678**, named **n8n-hooks**, with **None**. Then you tell n8n that webhook URLs are that origin (`WEBHOOK_URL`). The editor stays `n8n.<org>…` with **org**.

Anyone who learns a workflow’s webhook path can hit it. Use a throwaway path, deactivate when done, do not put secrets in the JSON you return.

**Done when**

- `edgible app list` shows **n8n** (**org**) and **n8n-hooks** (**None**), both port **5678**.
- `~/n8n/docker-compose.yml` has `WEBHOOK_URL=https://n8n-hooks.<org>.edgible.com/` (trailing slash, **no** `:5678`).
- `docker compose up -d` has been run again. n8n still opens on the **org** URL.

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
      - GENERIC_TIMEZONE=Europe/London
      - TZ=Europe/London
      - N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true
```

Replace `YOUR-ORG` with the labels from `edgible app list`. Trailing slashes on the two `https://` URLs. **No** `:5678` on those URLs.

```bash
cd ~/n8n
docker compose up -d
docker compose ps
```

Hard-refresh the **org** editor on the phone. Canvas should still load. Webhook nodes will still be empty until [chapter 5](05-n8n-public-webhook.md); you are only setting the base URL.

### Verify

- [ ] **n8n** is **org**; **n8n-hooks** is **None**.
- [ ] Both certificates issued.
- [ ] Compose `WEBHOOK_URL` is the **hooks** origin with a trailing slash.
- [ ] `N8N_EDITOR_BASE_URL` / `N8N_HOST` are the **editor** host.
- [ ] Phone can still open the org editor.
- [ ] Hello World still loads. Port **5678** not forwarded.

---

## Next

[4. A cron workflow](04-n8n-cron.md). Series: [README](README.md).
