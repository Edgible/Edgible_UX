# 3. Publish Control UI through Edgible

**Outcome:** `https://openclaw-ui.<org>.edgible.com` on a **phone (cellular)**, Edgible **org** login, then OpenClaw token + device approve. Gateway stays on loopback. Never **None** on port **18789**.

Prerequisites: [chapter 1](01-invite-through-edgible-on-vm.md) (Hello World) and [chapter 2](02-openclaw-on-the-box.md) (Gateway + local hello).

Series index: [README](README.md). Next: [public page from the agent](04-public-page-from-agent.md) or skip to the [Edgible skill](05-edgible-openclaw-skill.md).

---

## 10. Publish the Control UI through Edgible

**Outcome:** The OpenClaw Control UI on your mini-PC, reachable from the internet (phone on cellular), with Edgible **org** login in front — no Tailscale, no port-forward.

Leave **hello-world** running. Keep the Gateway on **loopback** `127.0.0.1:18789`. Edgible on this same VM proxies to that port. Do **not** bind `0.0.0.0` and do **not** use **None** (public) for this app.

Three locks:

1. **Edgible org** — only someone logged into your organisation can hit the hostname.
2. **OpenClaw gateway token** — first time on this browser (Control UI Settings or `#token=`). Local `openclaw dashboard` does not inject it on the Edgible origin.
3. **Device pairing** — first time on this browser: `openclaw devices approve <requestId>` on the VM. Local dashboard pairing does not cover the Edgible tab.

Prefer the **systemd / `openclaw gateway start`** Gateway, not a terminal you might close.

### 10a. Create the Edgible app

Edgible’s interactive picker looks at **Docker** (and a short list of process names). OpenClaw on loopback **18789** often **does not appear**. That is expected. The app is “this port on `mini-pc`,” not “this Docker name.”

**Preferred — set the port yourself:**

```bash
edgible device list
```

Note the id for **mini-pc**, then:

```bash
edgible app create existing \
  --name openclaw-ui \
  --port 18789 \
  --auth-modes org \
  --device-id <mini-pc-id>
```

Leave extra hostnames blank if asked. **Allow other organizations?** **No**. Never **None**.

**If you already started the wizard** and the list is only **hello-world**:

1. You still have to pick a workload — pick **hello-world** if that is all there is (it only tags the description).
2. When asked for the port, choose **Enter a custom port** → **18789**. Do **not** leave it on **8081**.

Confirm `ss -ltnp | grep 18789` still shows `127.0.0.1:18789` before you continue.

The CLI prints an `openclaw-ui.<org>.edgible.com` URL. Do **not** open it yet — wait for the certificate.

### 10b. Wait for the certificate

Same as Hello World. Host browser: [https://app.prod.edgible.com/](https://app.prod.edgible.com/) → **openclaw-ui** → **Certificates** until issued.

```bash
edgible app list
edgible app status
```

Copy the **https://openclaw-ui.<org>.edgible.com** URL (no trailing path). Always copy the exact host from `edgible app list`.

### 10c. Tell OpenClaw that origin is allowed

The landing page loading through Edgible is **not** enough. The Control UI’s JavaScript sends `Origin: https://openclaw-ui.<org>.edgible.com`. Loopback allows `http://127.0.0.1:18789`; Edgible is a **different origin**, so OpenClaw returns **browser origin not allowed**. That is **not** fixed by `openclaw gateway` / `openclaw dashboard` (those are local-only).

On the VM, get the exact hostname (no path):

```bash
edgible app list
```

Allow **both** the local UI and the Edgible origin (replace the host):

```bash
openclaw config set gateway.controlUi.allowedOrigins \
  '["http://127.0.0.1:18789","https://openclaw-ui.YOUR-ORG.edgible.com"]' --strict-json
openclaw gateway restart
```

The Edgible value must be exactly `https://` + hostname from `edgible app list` — pattern `https://<app>.<org>.edgible.com`, no path, no trailing slash, no `www` unless the URL has it.

```bash
openclaw config get gateway.controlUi.allowedOrigins
```

Hard-refresh the Edgible URL. You should get past origin-not-allowed.

Then the Control UI will likely say **gateway token missing (open the dashboard URL and paste the token in Control UI settings)**. That is expected. `openclaw dashboard` injects the token only for the **local** browser (`http://127.0.0.1:18789`). The Edgible page is a different origin; you paste the token yourself.

On the VM, **do not** use `openclaw config get gateway.auth.token`. On 2026.7 that always prints `__OPENCLAW_REDACTED__` — redaction, not a missing token.

`openclaw dashboard --no-open` also **will not** print the token on this build. If clipboard is unavailable it says “Token auto-auth not delivered” and leaves `http://127.0.0.1:18789/` bare. That is expected.

Read the value from disk (stay on the VM; do not paste the token or the whole file into chat):

```bash
python3 -c 'import json, pathlib; p=pathlib.Path.home()/".openclaw"/"openclaw.json"; print(json.load(p.open())["gateway"]["auth"]["token"])'
```

- A long string: that is the token.
- A JSON object (`source`, `id`, …): SecretRef — then `printenv OPENCLAW_GATEWAY_TOKEN` (or the env name in that object).
- Empty / KeyError: `printenv OPENCLAW_GATEWAY_TOKEN`. If still empty, `openclaw doctor --generate-gateway-token` then restart the Gateway and re-run the python line.

`openclaw gateway auth-token --show` is on **newer** docs than 2026.7.1-2; skip it if the subcommand does not exist.

Then either:

- Control UI → **Settings** → gateway token → paste → save, or
- Open `https://openclaw-ui.YOUR-ORG.edgible.com/#token=THEVALUE` (same host as `edgible app list`; fragment, not a query string).

Do **not** set `gateway.auth.mode` to `none` or `trusted-proxy`.

After the token is accepted, the Edgible tab will likely say **device pairing required**. That is expected. Local `openclaw dashboard` auto-pairs that **one** loopback browser; the Edgible origin is a **new** device.

Keep that browser tab open. On the VM:

```bash
openclaw devices list
openclaw devices approve <requestId>
```

Use the `requestId` from **your** page (not an example from this guide). Then reconnect / retry in the same tab. If the browser retried and you get a new id, `devices list` again and approve the current one — do not approve a stale id.

Each new browser (phone, another profile) needs its own one-time approve. Do **not** turn off pairing.

If you **already** pasted the token and still get **token missing**, Edgible’s local proxy may be stripping it. Then:

```bash
openclaw config set gateway.trustedProxies '["127.0.0.1"]' --strict-json
openclaw gateway restart
```

Hard-refresh again and paste the token if Settings was cleared.

**None (public)** was only to prove the tunnel. Switch this app back to **org** when chat works — a public Control UI is an admin shell on the internet. If org auth still fails after that, it is an Edgible bug; do not leave **None** as the real setup.

### Later visits (same browser)

You do **not** repeat origins, `trustedProxies`, token-from-disk, or `devices approve` every time.

| Each visit | First time only (this browser / this phone) | Only if something changed |
| --- | --- | --- |
| Open the same `https://openclaw-ui.<org>.edgible.com` URL | Paste gateway token (or `#token=`) | New hostname → update `allowedOrigins` |
| Edgible **org** login if the session expired | `openclaw devices approve` for this browser | Cleared site data, private window, new browser/profile, or phone → token + pairing again |
| Gateway already running on the mini-PC (`openclaw gateway status`) | — | Token rotated / device revoked → paste + approve again |

Keep a normal (non-private) browser profile. Private windows throw away the device identity on close, so pairing looks “every time.”

### 10d. Phone on cellular

1. Turn **Wi‑Fi off** on the phone.
2. Open the **https** URL. You should get **Edgible org login** first — sign in as the same account as step 1. A stranger with the URL should **not** see OpenClaw.
3. When the Control UI appears, paste the OpenClaw gateway token if asked (same reveal as 10c: python on `~/.openclaw/openclaw.json`, not `config get` and not `dashboard --no-open`). You can also open `https://openclaw-ui.YOUR-ORG.edgible.com/#token=…`. The phone is a **new** device: keep the tab open, `openclaw devices list` on the VM, approve that requestId, then reconnect. `openclaw dashboard` is a **local** handoff; it does not replace this on the phone.
4. Send `hello`. You want a reply, same as in the VM browser.

If **hello-world** still loads on the phone and **openclaw-ui** does not, the tunnel is fine — the failure is OpenClaw (certs, org login, origins, WebSocket, token).

If chat disconnects immediately, Edgible may not be proxying WebSockets yet — stop and note that; do not “fix” it with Tailscale Funnel.

### Verify

- [ ] `edgible app list` shows **openclaw-ui** with an `openclaw-ui.<org>.edgible.com` URL.
- [ ] Console **Certificates** for **openclaw-ui** is issued / ready.
- [ ] Protection is **org**, not None.
- [ ] Phone on **cellular**: Edgible login, then Control UI, then a chat reply.
- [ ] Hello World URL still works (tunnel unchanged).
- [ ] Port **18789** is still not forwarded on the router.

---
