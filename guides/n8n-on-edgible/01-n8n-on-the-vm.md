# 1. n8n on the VM

**Workflows on your own VM, with no public hostname yet.**

## 1.0 Why

Later chapters (the phone opening the canvas, GitHub firing a webhook) assume there is something on this box worth publishing. Right now there is nothing, so this chapter installs it: n8n as one process on loopback `5678`, with no public hostname.

n8n stays on loopback. Binding it to `0.0.0.0` and forwarding the port would expose a credential store holding every API key you own to anyone scanning that address. Edgible does not need that: the serving agent on this guest dials out on 443 and reaches n8n over loopback, so the process stays private and can still be published later. Later you give this one process two public hostnames with two auth modes: `org` for the editor you log into, `None` for the webhooks GitHub and `curl` must reach without a login.

```
the internet          (nothing: no hostname, no forwarded port, this chapter)

Ubuntu guest          Edgible serving agent ──► 127.0.0.1:5678
                                                      │
                                                     n8n
```

**Where you run this:** Docker and `curl` on the **Ubuntu guest**; the Hello World check on a **phone on cellular**.

## 1.1 The job

You install n8n in Docker on the same Ubuntu guest as Hello World. It listens on loopback port `5678`. Edgible is already running; you do not publish n8n yet.

**Done when**

- `docker compose -f ~/n8n/docker-compose.yml ps` shows the n8n container running.
- `curl` to `http://127.0.0.1:5678/` prints `200` (or a 3xx to `/setup` / `/signin`).
- Hello World on the phone still loads (Edgible unchanged).
- Port `5678` is not forwarded on the router.

**Need first:** [1. Edgible on an Ubuntu VM](../openclaw-on-edgible/01-edgible-on-vm.md). `edgible whoami` works, device `mini-pc` is healthy, `https://hello-world.<org>.edgible.com` loads on cellular. Docker is already on that guest from that chapter.

**Not this chapter:** Edgible apps for n8n, webhooks, cron, OpenClaw, or binding `0.0.0.0:5678`.

## 1.2 Words you’ll use

| Word | Here |
| --- | --- |
| n8n | The workflow runner (canvas + executions). Not OpenClaw. |
| `5678` | n8n’s HTTP port on the guest. |
| Editor | The canvas in a browser. Chapter 2 puts it on Edgible `org`. |
| Webhook | An HTTPS URL other systems POST/GET. Chapter 3–5. Needs a public hostname, not org login. |

## 1.3 Install n8n (loopback)

On the VM, one paste. `127.0.0.1:5678` is deliberate, the same binding OpenClaw uses on `18789`. The Edgible serving agent on this VM can still reach it. Do not publish `5678` on the router.

```bash
mkdir -p ~/n8n
cat > ~/n8n/docker-compose.yml << 'EOF'
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    restart: unless-stopped
    ports:
      - "127.0.0.1:5678:5678"
    environment:
      - N8N_PORT=5678
      - N8N_PROXY_HOPS=1
      - GENERIC_TIMEZONE=Australia/Adelaide
      - TZ=Australia/Adelaide
      - N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
EOF
cd ~/n8n
docker compose pull
docker compose up -d
docker compose ps
curl -sS -o /dev/null -w "%{http_code}\n" http://127.0.0.1:5678/
ss -ltnp | grep 5678
```

**Smoke test.** You want the container up, curl `200` or 3xx, and `ss` showing `127.0.0.1:5678`. `0.0.0.0:5678` means you changed the compose bind. Put loopback back.

You do not need to finish n8n’s owner signup yet. That can wait until the phone can open the editor ([chapter 2](02-n8n-editor-through-edgible.md)). The volume keeps the account if you sign up locally first via an SSH tunnel; not required.

### Verify

- [ ] `docker compose -f ~/n8n/docker-compose.yml ps` shows the n8n container running.
- [ ] `curl` to `http://127.0.0.1:5678/` prints `200` (or a 3xx to `/setup` / `/signin`).
- [ ] Hello World on the phone still loads (Edgible unchanged).
- [ ] Port `5678` is not forwarded on the router.

---

## Next

[2. n8n editor through Edgible](02-n8n-editor-through-edgible.md). Series: [README](README.md).
