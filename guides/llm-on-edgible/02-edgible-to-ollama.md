# 2. Edgible publishes Ollama

**Publish Ollama over HTTPS with a bearer secret, not a forwarded port.**

## 2.0 Why

After chapter 1 the model answers only to whoever is sitting at the Mac. Nothing else on your network can reach it, let alone n8n or OpenClaw on another computer. Forwarding `11434` on the router hands strangers an unauthenticated inference endpoint on your own hardware. A mesh VPN means every future caller has to enrol first. Installing Ollama inside the 4 GB guest gives up Metal for CPU inference. Handing a remote box the UTM address (`192.168.64.1`) fails for a different reason: that virt LAN only exists between the Mac and its own guest.

Edgible’s serving agent runs on the Ubuntu guest, and it can only proxy a local port (`127.0.0.1` on `mini-pc`). So the shape is: the Mac binds Ollama to the virt LAN, the guest binds loopback `11434` and forwards to the host, and the Edgible app publishes that loopback port. The guest connects out on 443; nothing inbound is opened anywhere.

The auth mode is set per app, and each app is one hostname, so this hostname decides who may use your GPU. It is `api-key`. With `None`, anyone on the internet could run inference on your GPU, and `org` is a human browser login that `curl`, an n8n node and an OpenClaw Gateway cannot complete. Callers send `Authorization: Bearer`, and the weights stay on the Mac.

![An off-box client calls ollama.<org>.edgible.com with a bearer key. It arrives at the serving agent on the Ubuntu guest, where socat forwards 127.0.0.1:11434 across the virt LAN to Ollama.app on the macOS host, so the weights and the GPU stay there.](../../images/diagrams/llm-on-edgible-02-light.svg#only-light)
![An off-box client calls ollama.<org>.edgible.com with a bearer key. It arrives at the serving agent on the Ubuntu guest, where socat forwards 127.0.0.1:11434 across the virt LAN to Ollama.app on the macOS host, so the weights and the GPU stay there.](../../images/diagrams/llm-on-edgible-02-dark.svg#only-dark)

| Section | Where | macOS-specific? |
| --- | --- | --- |
| 2.2 | macOS host | Yes. `launchctl`, `killall Ollama`, `open -a`, menu bar, `lsof`, `ifconfig`, UTM `192.168.64.1` |
| 2.3 | Ubuntu VM | No. `ip route`, `apt`, `socat`, `systemctl`, `ss` |
| 2.4–2.5 (CLI) | Ubuntu VM | No. `edgible app …` (agent already on the guest) |
| 2.5 (`curl` HTTPS) | Phone cellular or any laptop off the LAN | No |
| 2.6 (optional chat UI) | macOS (or any PC), not the thin Ubuntu guest | Chatbox is a Mac/Windows app. Do not Docker Open WebUI in the 4 GB VM. |

**Where you run this:** both machines, section by section; see the table above. In short: 2.2 on the **macOS host**, 2.3–2.5 (`edgible` CLI) on the **Ubuntu guest**, the HTTPS `curl` from a phone on cellular or any off-LAN laptop, and optional 2.6 on the Mac (or any PC with spare RAM).

## 2.1 The job

You open Ollama on the Mac so the VM can reach it, prove `curl` from the guest to the host, install a loopback forwarder, publish `11434` through Edgible as `api-key`, and hit the HTTPS URL from cellular with a Bearer token.

**Done when**

- Mac `OLLAMA_HOST` is `0.0.0.0:11434`; guest `curl` to `$HOST:11434/api/tags` is JSON.
- `ollama-forward.service` is active; guest `curl` to `http://127.0.0.1:11434/api/tags` returns the same JSON, including `qwen2.5:7b` (or your tag); `ss` is `127.0.0.1:11434`.
- `edgible app list` shows `ollama` with `api-key` (not `None`, not `org` alone), certificate issued.
- You saved the secret from `create` (not the key id from `list`).
- From a phone on cellular (or a laptop off the LAN), `curl` with `Authorization: Bearer` to `https://ollama.<org>.edgible.com/api/tags` returns that JSON, not an Edgible login HTML page.
- Optional: [Chatbox](https://chatboxai.app) on the Mac chats via `https://ollama.<org>…/v1` and the same secret ([2.6](#26-optional-a-real-chat-ui-not-curl)).
- Hello World still loads. Port `11434` is not forwarded on the router.
- You did not set this app to `None`.

**Need first:** [1. Ollama on bare metal](01-ollama-on-bare-metal.md) and [Edgible on an Ubuntu VM](../start-here/01-edgible-on-vm.md) (`mini-pc` healthy, Hello World on cellular). Leave the VM, `hello-world`, and Mac Ollama running.

**Not this chapter:** n8n nodes, OpenClaw `models set`, `None` on this app, or installing Ollama in the guest.

## 2.2 macOS host: listen on the virt LAN

macOS only. Terminal.app on the Mac, not the Ubuntu guest. `launchctl`, `open -a`, and “could not find ollama app” do not exist on Linux.

Ollama.app defaults to Mac localhost. The guest’s `127.0.0.1` is the *guest*.

```bash
launchctl setenv OLLAMA_HOST "0.0.0.0:11434"
killall Ollama
open -a Ollama
```

Wait until the llama icon is in the menu bar (a few seconds). Then:

```bash
ollama ps
```

`Error: ollama server not responding - could not find ollama app` means the app is not running. `open -a Ollama` again, or Finder → **Applications → Ollama**. If your prompt is the VM (`ubuntu@…` / a guest hostname), you are in the wrong place. `ollama` belongs on the Mac.

If `ollama ps` is empty (app is up, no model loaded), run the one-word hello from [chapter 1](01-ollama-on-bare-metal.md) again.

This bind is reachable from the UTM network. It is not an invitation to port-forward `11434` on the home router. After a Mac logout, you may need to run `launchctl setenv` and restart Ollama again.

Allow Ollama incoming in the Mac firewall if the next `curl` fails.

**Smoke test (macOS host).** Localhost `curl` is not this check; that already worked in chapter 1. `lsof` and `ifconfig` are macOS (on Ubuntu you would use `ss` / `ip`).

```bash
lsof -nP -iTCP:11434 -sTCP:LISTEN
```

You want `*:11434` or `0.0.0.0:11434`. `127.0.0.1:11434` means `OLLAMA_HOST` did not stick. Run 2.2 again (menu-bar Ollama must actually quit and reopen).

Then hit the Mac’s UTM/host address, not `127.0.0.1`. On Apple Virtualization that is often `192.168.64.1`:

```bash
curl -sS "http://192.168.64.1:11434/api/tags"
```

JSON with your tags means the bind is on the virt LAN. Connection refused: wrong IP (`ifconfig` and look for `192.168.64.`) or firewall. The guest `curl` in 2.3 is the same proof from the other side.

## 2.3 Ubuntu VM: reach the Mac, then bind loopback

Ubuntu guest only (UTM). `ip route`, `apt`, and `systemctl` are Linux. Do not paste this into macOS Terminal.

```bash
HOST=$(ip route | awk '/default/ {print $3; exit}')
echo "$HOST"
curl -sS "http://${HOST}:11434/api/tags"
```

You want JSON with your tag, not connection refused. UTM NAT is often `192.168.64.1` if `$HOST` is empty or wrong. Do not curl `127.0.0.1` yet.

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

You want the same JSON as the host `curl`, and `ss` showing `127.0.0.1:11434`. `0.0.0.0:11434` on the guest means the forwarder bound the wrong address. Keep loopback.

**Smoke test (Ubuntu VM).** Tags, then a one-shot generate through the forwarder (not `$HOST`, not Edgible):

```bash
curl -sS http://127.0.0.1:11434/api/tags
curl -sS http://127.0.0.1:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5:7b","prompt":"Reply with exactly: ok","stream":false}'
```

First command: JSON listing `qwen2.5:7b`. Second: a `response` that includes `ok` (GPU still on the Mac; this can take a few seconds). Connection refused: `systemctl status ollama-forward`. Empty tags / model not found: chapter 1 pull, then 2.2 bind. `ss` must still be `127.0.0.1:11434`.

## 2.4 Create the Edgible app (Ubuntu VM)

On the Ubuntu guest (Edgible CLI is already there from Hello World). Not macOS.

```bash
edgible device list
```

Note the id for `mini-pc`, then:

```bash
edgible app create existing \
  --name ollama \
  --port 11434 \
  --auth-modes api-key \
  --device-id <mini-pc-id>
```

Leave extra hostnames blank. **Allow other organizations?** **No**. Never `None`. Do not use `org` alone. `curl` and n8n cannot complete a browser login.

Wait for the certificate: console → `ollama` → **Certificates**, or `edgible app list` / `edgible app status`. Copy `https://ollama.YOUR-ORG.edgible.com` exactly (no path, no `:11434`).

## 2.5 API key (Ubuntu VM) and cellular smoke (any off-LAN device)

Create and list keys with `edgible` on the Ubuntu guest. The HTTPS `curl` is not macOS-specific: phone on cellular, or any laptop that is not on the VM’s LAN.

Create a key (name it e.g. `laptop-curl`).

```bash
edgible app list
edgible app api-keys create --app-id <ollama-app-id> --name laptop-curl
```

(`edgible application api-keys create` is the same command.)

The secret (the long token in the `create` output) is printed once. Copy it immediately into a local env var on the machine you will `curl` from, e.g. `export EDGIBLE_APP_KEY='…'`. Do not paste it into Hello World, chat, or a public gist. If you dismiss the output, Edgible will not show that value again. Create a new key.

Then list keys so you can tell id from secret:

```bash
edgible app api-keys list --app-id <ollama-app-id>
```

(`edgible app api-key list` if your CLI uses the singular alias.)

List rows are metadata: name, key id, created / expiry. That id is not the API key. `Authorization: Bearer` must be the secret from `create`, not the id from `list`. Using the id as Bearer returns `401`. Lost secret → `api-keys delete` that id, then `create` again.

**Smoke test (phone on cellular).** From a phone on cellular or a laptop not on the VM’s LAN:

```bash
curl -sS "https://ollama.YOUR-ORG.edgible.com/api/tags" \
  -H "Authorization: Bearer $EDGIBLE_APP_KEY"
```

You want the tags JSON. An HTML login page means the app is `org`. HTTP `401` means the Bearer is missing or wrong. `localhost` or `:11434` in the URL means you copied the wrong origin.

For a chat window instead of `curl`, skip the optional generate below and go to [2.6 Chatbox](#26-optional-a-real-chat-ui-not-curl).

Optional. Prove a completion (slow on a 7B; still GPU on the Mac):

```bash
curl -sS "https://ollama.YOUR-ORG.edgible.com/api/generate" \
  -H "Authorization: Bearer $EDGIBLE_APP_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5:7b","prompt":"Reply with exactly: ok","stream":false}'
```

n8n and OpenClaw run on other VMs (another home computer). They call this HTTPS origin with Bearer. Do not give them UTM `$HOST:11434`. That LAN is only the Mac guest → Mac hop.

## 2.6 Optional: a real chat UI (not curl)

`curl` proves the published hostname works. For a demo, use a desktop client that speaks OpenAI-compatible `/v1` with a Bearer key. GPU stays on the Mac; the app only calls `https://ollama.<org>.edgible.com`.

Do not put Open WebUI (or any other chat server) in the 4 GB Ubuntu guest. That RAM is for Edgible + the website, not another LLM UI.

Local only: the Ollama menu-bar app on the Mac can chat to `localhost`. That does not prove the public HTTPS + `api-key` path.

Published endpoint: [Chatbox](https://chatboxai.app) (Mac/Windows/Linux).

1. **Settings** (bottom left of the sidebar) → **Model Provider**.
2. **Add** → type **OpenAI API compatible** (not Chatbox’s own cloud, not “OpenAI” with `api.openai.com`).
3. **API Key** = the secret from 2.5. **API Host** = `https://ollama.YOUR-ORG.edgible.com` (Chatbox usually appends `/v1/chat/completions` itself; if chat fails, try the same URL with `/v1`).
4. **Add a model.** The id must be exactly what `ollama ls` shows, e.g. `qwen2.5:7b`. Save. Use **Check** if the UI has it. You want connection OK, not 401.
5. Leave Settings. Click the **back** chevron, or click **Chatbox** in the sidebar, until you see the big empty chat pane and an input at the bottom. There is no button labelled “New conversation”.
6. If you still only see Settings: look left for the sidebar. It may be hidden, so use **☰** (top left) or drag the window wider. In the sidebar the button is **New Chat** (sometimes a `+`). You can skip that: if a blank thread is already open, just use the input box at the bottom.
7. In that thread, open the model picker (usually above the input, or at the top of the pane). Pick your custom provider + `qwen2.5:7b`. If it still says GPT-4 / Chatbox AI, you are on their cloud, not Ollama.
8. Type `Say hello in one sentence` and send. First 7B reply can take several seconds (GPU on the Mac).

A 401 is a bad secret; HTML login means `org` hostname; empty models / Check fail means Ollama or the forwarder is down. Streaming then a hang: Mac Ollama quit or the VM slept.

Same idea works in Cherry Studio or any “custom OpenAI endpoint” app. Open WebUI is a browser UI, but it is another Docker stack, so run it on a machine with spare RAM, not this VM. A second Edgible app with `org` in front of Open WebUI is a later pattern (human UI vs `api-key` API), not this chapter.

### Verify

- [ ] Mac `OLLAMA_HOST` is `0.0.0.0:11434`; guest `curl` to `$HOST:11434/api/tags` is JSON.
- [ ] `ollama-forward.service` is active; guest `curl` to `http://127.0.0.1:11434/api/tags` returns the same JSON, including `qwen2.5:7b` (or your tag); `ss` is `127.0.0.1:11434`.
- [ ] `edgible app list` shows `ollama` with `api-key` (not `None`, not `org` alone), certificate issued.
- [ ] You saved the secret from `create` (not the key id from `list`).
- [ ] From a phone on cellular (or a laptop off the LAN), `curl` with `Authorization: Bearer` to `https://ollama.<org>.edgible.com/api/tags` returns that JSON, not an Edgible login HTML page.
- [ ] Optional: [Chatbox](https://chatboxai.app) on the Mac chats via `https://ollama.<org>…/v1` and the same secret ([2.6](#26-optional-a-real-chat-ui-not-curl)).
- [ ] Hello World still loads. Port `11434` is not forwarded on the router.
- [ ] You did not set this app to `None`.

---

## Next

[3. n8n uses that URL](03-n8n-uses-ollama.md). Series: [README](README.md).
