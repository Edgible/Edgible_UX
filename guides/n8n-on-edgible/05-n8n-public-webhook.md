# 5. A webhook a stranger can hit

**This is the Edgible demo: HTTPS in, no port-forward.**

## 5.1 The job

You add a **Webhook** node whose **production** URL is on **n8n-hooks** (None), not the org editor host. You hit it from **cellular** or any machine that is not the VM. n8n responds with JSON. That is what GitHub/Stripe would do next; you do not need them for the smoke test.

**Done when**

- The Webhook node shows a production URL that starts with `https://n8n-hooks.` and has **no** `:5678` and **no** `localhost`.
- The workflow is **Active**.
- A GET in the phone browser (cellular) **or** `curl` off the LAN returns JSON such as `{"ok":true}`.
- The editor URL (`n8n.<org>…`) still requires **org**. Hitting the **editor** host with `/webhook/…` is not the test (org will block strangers).

**Need first:** [3. Public webhook door](03-n8n-webhook-door.md) (`WEBHOOK_URL` set, hooks cert issued) and the canvas from [2](02-n8n-editor-through-edgible.md).

**Not this chapter:** OpenClaw, Telegram bots, or leaving a privileged workflow on a public path.

## 5.2 Build it

In the editor:

1. **Add workflow** (new, not the cron).
2. Add **Webhook**.
3. HTTP method: **GET** (phone browser) — you can also allow POST later.
4. Path: something unguessable, e.g. `edgible-smoke-<random>`.
5. Respond: **Immediately**, JSON body:

```json
{"ok": true, "via": "edgible"}
```

6. **Save**. Copy the **Production** URL (not Test). It must use the **n8n-hooks** host from [chapter 3](03-n8n-webhook-door.md).
7. Toggle **Active**.

If the node still prints `localhost:5678` or `:5678` on the Edgible host, `WEBHOOK_URL` is wrong — go back to [3.3](03-n8n-webhook-door.md#33-point-n8n-at-the-two-origins) and recreate the container.

## 5.3 Hit it from outside the VM

**Phone (cellular):** paste the production URL in the browser. You want the JSON (or a download of it). Wi‑Fi on the same LAN as the VM is **not** this test.

**Or** from a laptop on cellular / another network:

```bash
curl -sS "https://n8n-hooks.YOUR-ORG.edgible.com/webhook/edgible-smoke-YOURPATH"
```

Use the exact production URL from the node. HTTP **200** and `ok` is success.

n8n **Executions** should show the request.

Deactivate the workflow when you are done playing. A public GET that only returns `ok` is still a door; do not attach “delete all my disks” to a None hostname.

### Verify

- [ ] Production URL is `https://n8n-hooks.<org>.edgible.com/webhook/…` (your path).
- [ ] Workflow **Active**.
- [ ] Cellular (or off-LAN curl) returns the JSON.
- [ ] Executions recorded the call.
- [ ] **n8n** app is still **org**. **n8n-hooks** is still **None**.
- [ ] Hello World still loads. Port **5678** not forwarded.
- [ ] You deactivated the smoke webhook (or accept that the path is public).

---

## Next

That's this series. [Index](README.md). Edgible VM setup lives in [OpenClaw chapter 1](../openclaw-on-edgible/01-edgible-on-vm.md). The agent series is [OpenClaw on Edgible](../openclaw-on-edgible/README.md) — do not wire n8n to OpenClaw for this demo.
