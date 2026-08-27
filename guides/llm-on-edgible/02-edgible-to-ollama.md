# 2. Edgible publishes Ollama

**GPU stays on the Mac. The VM only forwards. Edgible publishes the guest loopback.**

Edgible on the Ubuntu guest can only proxy a **local** port (`127.0.0.1` on **mini-pc**). Ollama is on the Mac, so the guest listens on loopback **11434** and forwards to the host’s Ollama. Then you create an Edgible app on that port with **api-key**. Machines that cannot log into org send `Authorization: Bearer`. Never **None**.

```
Mac     Ollama (Metal)     0.0.0.0:11434
              ↑  UTM NAT / virt LAN (often 192.168.64.1)
Ubuntu  socat              127.0.0.1:11434
              ↑
Edgible agent              app ollama, **api-key**
              ↑
Cellular curl              https://ollama.<org>.edgible.com
```

## 2.1 The job

You open Ollama on the Mac so the VM can reach it, prove `curl` from the guest to the host, install a loopback forwarder, publish **11434** through Edgible as **api-key**, and hit the HTTPS URL from **cellular** with a Bearer token.

**Done when**

- From the VM, `curl http://127.0.0.1:11434/api/tags` returns JSON that includes `qwen2.5:7b` (or your tag).
- `edgible app list` shows **ollama** with **api-key** (not **None**, not **org** alone).
- From a phone on **cellular** (or a laptop off the LAN), `curl` with `Authorization: Bearer` to `https://ollama.<org>.edgible.com/api/tags` returns that JSON — not an Edgible login HTML page.
- Hello World still loads. Port **11434** is not forwarded on the router.

**Need first:** [1. Ollama on bare metal](01-ollama-on-bare-metal.md) and [Edgible on an Ubuntu VM](../openclaw-on-edgible/01-edgible-on-vm.md) (`mini-pc` healthy, Hello World on cellular). Leave the VM, **hello-world**, and Mac Ollama running.

**Not this chapter:** n8n nodes, OpenClaw `models set`, **None** on this app, or installing Ollama in the guest.

## 2.2 Mac — listen on the virt LAN

Ollama defaults to **Mac localhost**. The guest’s `127.0.0.1` is the *guest*. On the **Mac**:

```bash
launchctl setenv OLLAMA_HOST "0.0.0.0:11434"
killall Ollama; open -a Ollama
```

If `ollama ps` is empty, run the one-word hello from [chapter 1](01-ollama-on-bare-metal.md) again.

This bind is reachable from the UTM network. It is **not** an invitation to port-forward **11434** on the home router. After a Mac logout, you may need to run `launchctl setenv` and restart Ollama again.

Allow **Ollama** incoming in the Mac firewall if the next `curl` fails.

## 2.3 VM — reach the Mac, then bind loopback

On the **Ubuntu guest**:

```bash
HOST=$(ip route | awk '/default/ {print $3; exit}')
echo "$HOST"
curl -sS "http://${HOST}:11434/api/tags"
```

You want JSON with your tag, not connection refused. UTM NAT is often `192.168.64.1` if `$HOST` is empty or wrong. Do **not** curl `127.0.0.1` **yet**.

Then install a forwarder so Edgible’s local port is the Mac:

```bash
sudo apt-get update
sudo apt-get install -y socat
sudo tee /usr/local/bin/ollama-forward.sh >/dev/null << 'EOF'
#!/bin/bash
set -euo pipefail
HOST=$(ip route | awk '/default/ {print $3; exit}')
if [ -z "${HOST}" ]; then
  echo "ollama-forward: no default route" >&2
  exit 1
fi
exec /usr/bin/socat TCP-LISTEN:11434,bind=127.0.0.1,fork,reuseaddr TCP:"${HOST}":11434
EOF
sudo chmod +x /usr/local/bin/ollama-forward.sh
sudo tee /etc/systemd/system/ollama-forward.service >/dev/null << 'EOF'
[Unit]
Description=Forward VM loopback 11434 to host Ollama
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/bin/ollama-forward.sh
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now ollama-forward.service
curl -sS http://127.0.0.1:11434/api/tags
ss -ltnp | grep 11434
```

You want the same JSON as the host `curl`, and `ss` showing **`127.0.0.1:11434`**. **`0.0.0.0:11434`** on the guest means the forwarder bound the wrong address — keep loopback.

## 2.4 Create the Edgible app

On the **VM**:

```bash
edgible device list
```

Note the id for **mini-pc**, then:

```bash
edgible app create existing \
  --name ollama \
  --port 11434 \
  --auth-modes api-key \
  --device-id <mini-pc-id>
```

Leave extra hostnames blank. **Allow other organizations?** **No**. Never **None**. Do not use **org** alone — `curl` and n8n cannot complete a browser login.

Wait for the certificate: console → **ollama** → **Certificates**, or `edgible app list` / `edgible app status`. Copy `https://ollama.YOUR-ORG.edgible.com` exactly (no path, no `:11434`).

## 2.5 API key and cellular smoke

Create a key (name it e.g. `laptop-curl`). The secret is shown **once** — store it in a local env var on the machine you curl from. Do **not** paste it into Hello World, chat, or a public gist.

```bash
edgible app list
edgible app api-keys create --app-id <ollama-app-id> --name laptop-curl
```

(`edgible application api-keys create` is the same command.)

From a **phone on cellular** or a laptop **not** on the VM’s LAN:

```bash
curl -sS "https://ollama.YOUR-ORG.edgible.com/api/tags" \
  -H "Authorization: Bearer $EDGIBLE_APP_KEY"
```

You want the tags JSON. An HTML login page means the app is **org**. HTTP **401** means the Bearer is missing or wrong. `localhost` or `:11434` in the URL means you copied the wrong origin.

Optional — prove a completion (slow on a 7B; still GPU on the Mac):

```bash
curl -sS "https://ollama.YOUR-ORG.edgible.com/api/generate" \
  -H "Authorization: Bearer $EDGIBLE_APP_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5:7b","prompt":"Reply with exactly: ok","stream":false}'
```

OpenClaw **on this same VM** can still call `http://$HOST:11434` on the virt LAN and skip Edgible. The published URL is for callers that are **not** on that Mac.

### Verify

- [ ] Mac `OLLAMA_HOST` is `0.0.0.0:11434`; guest `curl` to `$HOST:11434/api/tags` is JSON.
- [ ] `ollama-forward.service` is **active**; guest `curl` to `http://127.0.0.1:11434/api/tags` is the same JSON; `ss` is **127.0.0.1:11434**.
- [ ] App **ollama** is **api-key**, certificate issued.
- [ ] Cellular (or off-LAN) `curl` with Bearer returns `/api/tags` JSON.
- [ ] Hello World still loads. Port **11434** is not forwarded on the router.
- [ ] You did not set this app to **None**.

---

## Next

[3. n8n uses that URL](03-n8n-uses-ollama.md) (not written yet). Series: [README](README.md).
