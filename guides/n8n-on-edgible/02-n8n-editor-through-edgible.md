# 2. n8n editor through Edgible

**The canvas, from a phone, behind `https://` and org login.**

Edgible auth is per **app** (the hostname), not per path on one URL. This hostname is the privileged door — canvas, credentials, every workflow. Keep it **org**. Stripe and GitHub cannot sit through that login, so they get a **different** hostname in the next chapter. Do not “fix” webhooks by setting this app to **None**.

## 2.1 The job

You publish n8n’s **editor** through Edgible. n8n stays on loopback **5678**. Protection is **org** — never **None** on this hostname. GitHub cannot log into your org; inbound webhooks are a **different** app in [chapter 3](03-n8n-webhook-door.md).

**Done when**

- Phone on **cellular** opens `https://n8n.<org>.edgible.com`.
- Edgible **org** login, then n8n owner signup (first time) or sign-in, then the **canvas**.
- Hello World still loads. Port **5678** is still not forwarded.

**Need first:** [1. n8n on the VM](01-n8n-on-the-vm.md) and [Edgible on an Ubuntu VM](../openclaw-on-edgible/01-edgible-on-vm.md) (`mini-pc`, Hello World). Leave **hello-world** and the n8n container running.

**Not this chapter:** `WEBHOOK_URL`, a public hooks hostname, cron, or OpenClaw.

## 2.2 Create the Edgible app

n8n is Docker, so the picker may list it. Port must be **5678**, auth **org**.

```bash
edgible device list
```

Note the id for **mini-pc**, then:

```bash
edgible app create existing \
  --name n8n \
  --port 5678 \
  --auth-modes org \
  --device-id <mini-pc-id>
```

Leave extra hostnames blank. **Allow other organizations?** **No**. Never **None** on this app.

**Wizard instead:** `edgible app create existing` → name `n8n` → protection **Org** → device **mini-pc** → port **5678** (custom if the list shows 8081).

The CLI prints an `n8n.<org>.edgible.com` URL. Do **not** open it yet — wait for the certificate.

## 2.3 Wait for the certificate

Host browser: [https://app.prod.edgible.com/](https://app.prod.edgible.com/) → **n8n** → **Certificates** until issued.

```bash
edgible app list
edgible app status
```

Copy the **https://n8n.<org>.edgible.com** URL (no path). Always copy the exact host from `edgible app list`.

## 2.4 Open it on the phone

Cellular, not the VM’s Wi‑Fi.

1. Open that HTTPS URL.
2. Sign in to **Edgible** (org).
3. n8n’s own **owner** signup or login (email + password n8n stores on the VM volume). That is not the Edgible password.
4. You want the empty canvas (or the home/workflows list).

If the tab loads a shell but the canvas stays blank, Edgible may not be proxying **WebSockets** yet — stop and note that; do not “fix” it with a mesh VPN or an ingress tunnel.

### Verify

- [ ] `edgible app list` shows **n8n** with an `n8n.<org>.edgible.com` URL.
- [ ] Console **Certificates** for **n8n** is issued.
- [ ] Protection is **org**, not None.
- [ ] Phone on **cellular**: Edgible login, then n8n signup/sign-in, then the canvas.
- [ ] Hello World URL still works.
- [ ] Port **5678** is still not forwarded.

---

## Next

[3. Public webhook door](03-n8n-webhook-door.md). Series: [README](README.md).
