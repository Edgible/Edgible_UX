# 3. n8n uses the published Ollama URL

**n8n is a remote self-hosted caller.** It uses `https://ollama.<org>.edgible.com/v1` with Bearer — not the Mac’s LAN. The AI settings **sandbox** stays on **this** n8n VM (your Docker), not Daytona.

The Mac (and its Ubuntu guest) only **serve** Ollama and the website. n8n runs on a **different** self-hosted VM (for example on a Windows host). That is the use case: workflow box → published LLM, GPU stays on the Mac. n8n’s **Ollama self-hosted** endpoint speaks Ollama’s **OpenAI-compatible** API (`/v1/models`, `/v1/chat/completions`). Origin + **`/v1`** + the secret. Do not put that secret on a public webhook. Do not set the **ollama** app to **None**.

The wizard’s next step after a successful Ollama test is a **sandbox**. That is n8n’s **AI Assistant** (it writes workflows and runs the code it generated). Self-hosting it is the same Edgible idea: isolation on **your** box, no extra SaaS. Official steps: [Install using Docker Compose](https://docs.n8n.io/deploy/host-n8n/install-options/install-using-docker-compose/) and [Set up AI Assistant](https://docs.n8n.io/deploy/host-n8n/configure-n8n/set-up-ai-assistant/).

## 3.1 The job

You point n8n at the published URL, pick **`qwen2.5:7b`**, add n8n’s **own** sandbox stack on the **n8n** VM, and run one chain. GPU stays on the Mac.

**Done when**

- The Ollama endpoint **tests successfully**.
- The model is **`qwen2.5:7b`** (or your `ollama ls` tag), not **qwen3-coder**.
- `sandbox-api` is **healthy**; from the n8n container, `http://sandbox-api:8080/healthz` is `{"status":"ok"}`.
- One **Execute** of a chain returns a sentence. Mac `ollama ps` shows GPU.

**Need first:** n8n’s editor on **this** VM (or its Edgible **org** URL). [Chapter 2](02-edgible-to-ollama.md) — cellular `curl` to `/api/tags` with Bearer already works. Docker Compose v2. About **4 GB RAM / 2 vCPUs** spare on the **n8n** VM (the runner is Docker-in-Docker).

**Not this chapter:** installing n8n on the Mac guest, pulling **qwen3-coder**, Open WebUI or this sandbox on the 4 GB UTM VM, Daytona, publishing sandbox ports on Edgible, or OpenClaw.

## 3.2 n8n does not require qwen3-coder

Ollama’s n8n page uses **`qwen3-coder`** as an example. Use **`qwen2.5:7b`** from `ollama ls` on the Mac. Do **not** pull `qwen3-coder` (~**19 GB**).

## 3.3 Credential (Edgible + `/v1`)

In **your** n8n editor (n8n VM — not the Mac):

1. Add an **Ollama** credential / **self-hosted** endpoint.
2. **Endpoint / Base URL** = `https://ollama.YOUR-ORG.edgible.com/v1`  
   Copy the host from `edgible app list` on the **Mac guest**. **Include `/v1`.** No `:11434`. No `/api`.
3. **API Key** = the **secret** from [2.5](02-edgible-to-ollama.md) (not the key **id**).
4. **Save.** Connection test succeeds.

`/v1` is required: this form calls `/v1/models`, not `/api/tags`.

Do **not** use `localhost:11434` or a UTM `192.168.64.1` from this VM — those are the Mac’s loopback / virt LAN.

Then set the **model** to **`qwen2.5:7b`**. Leave the sandbox fields until 3.4.

### Classic Ollama Chat Model (no `/v1`)

Some n8n builds still have a credential that GETs `/api/tags`. That one must **not** have `/v1`. Prefer **3.3** when the UI is “self-hosted” and the test only passed with `/v1`.

## 3.4 Self-hosted sandbox (n8n VM)

Do this on the **n8n** VM only. Do **not** add these containers on the Mac UTM guest.

The sandbox is **not** an Edgible app. n8n reaches `sandbox-api` on the Compose network. Do **not** publish **8080** / **9090** / **9091**. `sandbox-runner-1` is **privileged** Docker-in-Docker — treat it as root on that VM.

Windows host: Compose **inside** the Linux VM / **WSL2**, project under `~/n8n` (not `/mnt/c/...`).

This **replaces** `~/n8n/docker-compose.yml`. The named volume `n8n_data` keeps existing workflows if you already used that name. Sandbox services match n8n’s [Docker Compose install](https://docs.n8n.io/deploy/host-n8n/install-options/install-using-docker-compose/).

```bash
mkdir -p ~/n8n
cd ~/n8n
```

`.env` — four random strings; **`SANDBOX_API_KEYS` and `N8N_INSTANCE_AI_SANDBOX_API_KEY` must be identical**:

```bash
A=$(openssl rand -hex 24)
B=$(openssl rand -hex 24)
C=$(openssl rand -hex 24)
D=$(openssl rand -hex 24)
cat > .env << EOF
SANDBOX_API_KEYS=${A}
SANDBOX_API_RUNNER_REGISTRATION_TOKEN=${B}
SANDBOX_API_RUNNER_API_KEY=${C}
N8N_INSTANCE_AI_SANDBOX_API_KEY=${A}
SEARXNG_SECRET=${D}
EOF
```

Do not commit `.env`. Save this as **`~/n8n/searxng-settings.yml`** (stock SearXNG only serves HTML; n8n needs JSON):

```yaml
use_default_settings: true
search:
  formats:
    - html
    - json
```

Save this as **`~/n8n/docker-compose.yml`** (whole file):

```yaml
volumes:
  n8n_data:
  sandbox-tls:

services:
  sandbox-certs:
    image: ghcr.io/n8n-io/n8n-sandbox-service-api:latest
    user: "0:0"
    entrypoint: ["sh", "-c"]
    command:
      - >
        bootstrap-mtls.sh --out-dir /tls --api-san sandbox-api
        --control-san-prefix sandbox-runner &&
        chown -R sandbox-api:sandbox-api /tls/api
    environment:
      NUM_RUNNERS: "1"
    volumes:
      - sandbox-tls:/tls

  sandbox-api:
    image: ghcr.io/n8n-io/n8n-sandbox-service-api:latest
    depends_on:
      sandbox-certs:
        condition: service_completed_successfully
    environment:
      SANDBOX_API_KEYS: ${SANDBOX_API_KEYS}
      SANDBOX_API_RUNNER_REGISTRATION_TOKEN: ${SANDBOX_API_RUNNER_REGISTRATION_TOKEN}
      SANDBOX_API_RUNNER_API_KEY: ${SANDBOX_API_RUNNER_API_KEY}
      SANDBOX_API_GRPC_TLS_CERT_FILE: /tls/api/grpc-server.crt
      SANDBOX_API_GRPC_TLS_KEY_FILE: /tls/api/grpc-server.key
      SANDBOX_API_GRPC_TLS_CLIENT_CA_FILE: /tls/api/ca.crt
      SANDBOX_API_RUNNER_CONTROL_GRPC_TLS_CA_FILE: /tls/api/ca.crt
      SANDBOX_API_RUNNER_CONTROL_GRPC_TLS_CERT_FILE: /tls/api/control-grpc-api-client.crt
      SANDBOX_API_RUNNER_CONTROL_GRPC_TLS_KEY_FILE: /tls/api/control-grpc-api-client.key
      SANDBOX_API_RUNNER_CONTROL_GRPC_TLS_SERVER_NAME: sandbox-runner-1
    volumes:
      - sandbox-tls:/tls:ro
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:8080/healthz"]
      interval: 5s
      timeout: 3s
      retries: 5
      start_period: 10s

  sandbox-runner-1:
    image: ghcr.io/n8n-io/n8n-sandbox-service-runner-dind:latest
    privileged: true
    depends_on:
      sandbox-api:
        condition: service_healthy
    environment:
      SANDBOX_RUNNER_API_KEYS: ${SANDBOX_API_RUNNER_API_KEY}
      SANDBOX_RUNNER_REGISTRATION_TOKEN: ${SANDBOX_API_RUNNER_REGISTRATION_TOKEN}
      SANDBOX_RUNNER_API_GRPC_ADDR: sandbox-api:9090
      SANDBOX_RUNNER_HTTP_BASE_URL: http://sandbox-runner-1:8080
      SANDBOX_RUNNER_CONTROL_GRPC_LISTEN_ADDR: ":9091"
      SANDBOX_RUNNER_CONTROL_GRPC_ADVERTISE_ADDR: sandbox-runner-1:9091
      SANDBOX_RUNNER_ID: runner-1
      SANDBOX_RUNNER_DOCKER_SANDBOX_IMAGE: ghcr.io/n8n-io/n8n-sandbox-service-sandbox:latest
      SANDBOX_RUNNER_REGISTRATION_GRPC_CA_FILE: /tls/runner/ca.crt
      SANDBOX_RUNNER_REGISTRATION_GRPC_CERT_FILE: /tls/runner/grpc-client.crt
      SANDBOX_RUNNER_REGISTRATION_GRPC_KEY_FILE: /tls/runner/grpc-client.key
      SANDBOX_RUNNER_REGISTRATION_GRPC_SERVER_NAME: sandbox-api
      SANDBOX_RUNNER_CONTROL_GRPC_TLS_CERT_FILE: /tls/runner/control-grpc-server.crt
      SANDBOX_RUNNER_CONTROL_GRPC_TLS_KEY_FILE: /tls/runner/control-grpc-server.key
      SANDBOX_RUNNER_CONTROL_GRPC_TLS_CLIENT_CA_FILE: /tls/runner/ca.crt
    volumes:
      - sandbox-tls:/tls:ro

  searxng:
    image: ghcr.io/searxng/searxng:latest
    environment:
      SEARXNG_SECRET: ${SEARXNG_SECRET}
    volumes:
      - ./searxng-settings.yml:/etc/searxng/settings.yml:ro

  n8n:
    image: docker.n8n.io/n8nio/n8n
    restart: unless-stopped
    depends_on:
      sandbox-api:
        condition: service_healthy
    ports:
      - "127.0.0.1:5678:5678"
    env_file: .env
    environment:
      N8N_PORT: "5678"
      N8N_PROXY_HOPS: "1"
      GENERIC_TIMEZONE: Australia/Adelaide
      TZ: Australia/Adelaide
      N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS: "true"
      N8N_ENABLED_MODULES: instance-ai
      N8N_INSTANCE_AI_SANDBOX_ENABLED: "true"
      N8N_INSTANCE_AI_SANDBOX_PROVIDER: n8n-sandbox
      N8N_INSTANCE_AI_SANDBOX_API_URL: http://sandbox-api:8080
      N8N_INSTANCE_AI_SANDBOX_IMAGE: ghcr.io/n8n-io/n8n-sandbox-service-sandbox:latest
      N8N_INSTANCE_AI_SEARXNG_URL: http://searxng:8080
    volumes:
      - n8n_data:/home/node/.n8n
```

`${SANDBOX_API_KEYS}` and the other `${…}` lines are Compose substituting from `.env`, not shell.

```bash
cd ~/n8n
docker compose up -d
docker compose ps
docker compose exec n8n wget -qO- http://sandbox-api:8080/healthz
docker compose logs sandbox-api | grep -i runner
```

You want `sandbox-api` **healthy**, healthz `{"status":"ok"}`, and a log line that the runner registered. n8n still only binds **127.0.0.1:5678**.

Do **not** set `N8N_INSTANCE_AI_MODEL` to Anthropic — Ollama stays in the UI. Change `GENERIC_TIMEZONE` / `TZ` if you need a different zone. If this n8n already has **n8n-hooks**, keep `WEBHOOK_URL` (and any `N8N_HOST` / `N8N_PROTOCOL`) on the **n8n** `environment` block from [n8n chapter 3](../n8n-on-edgible/03-n8n-webhook-door.md).

Then AI settings → sandbox **n8n-sandbox** (not Daytona). **Service URL** = `http://sandbox-api:8080`. **API key** = `SANDBOX_API_KEYS` from `.env` (`grep SANDBOX_API_KEYS .env`). Save. You want a successful test.

Web search: provider **SearXNG**. **URL** = `http://searxng:8080`. No API key. Same Compose network as n8n — not `localhost`, not Edgible. Leave **Brave** empty unless you buy that. Do **not** publish SearXNG’s port or create an Edgible app for it.

If `sandbox-api` never goes healthy: `docker compose logs sandbox-certs` then `sandbox-api`. Runner crash-loop: token mismatch in `.env`. Sandbox test fails: key/URL mismatch, or n8n not on this Compose file.

If the stack is **already up** without SearXNG: add `SEARXNG_SECRET` to `.env`, write `searxng-settings.yml`, add the `searxng` service and `N8N_INSTANCE_AI_SEARXNG_URL` as above, then `docker compose up -d`.

### 3.4.1 Health check

On the **n8n** VM, from `~/n8n`. This is what the UI uses: probes from **inside** the n8n container, plus n8n on loopback.

```bash
cd ~/n8n
echo "=== compose ==="
docker compose ps -a
echo
echo "=== from n8n container ==="
docker compose exec -T n8n wget -qO- http://sandbox-api:8080/healthz && echo
docker compose exec -T n8n wget -qO- "http://searxng:8080/search?q=n8n&format=json" | head -c 200 && echo
echo
echo "=== n8n on this VM ==="
curl -sf http://127.0.0.1:5678/healthz && echo
echo
echo "=== runner registered ==="
docker compose logs sandbox-api 2>/dev/null | grep -i runner | tail -3
```

You want: `sandbox-api` **healthy**, n8n **running**, `searxng` **running**, `sandbox-certs` **exited 0** (one-shot). Healthz `{"status":"ok"}`. SearXNG JSON that includes `"results"`. n8n `/healthz` **200**. A log line that the runner registered.

Optional — Ollama from the **same** container (replace host and secret):

```bash
docker compose exec -T n8n wget -qO- \
  --header="Authorization: Bearer YOUR-EDGIBLE-SECRET" \
  "https://ollama.YOUR-ORG.edgible.com/v1/models" | head -c 400 && echo
```

You want JSON listing **`qwen2.5:7b`**. 401 = bad secret. Timeout/HTML = Mac Ollama/forwarder down or wrong host.

Do **not** publish sandbox or SearXNG ports to prove this. `ss` on the VM should still show **5678** on **127.0.0.1** only.

## 3.5 One chain

Assistant can wait until 3.4 is green. A workflow does not need the sandbox.

1. **Add workflow.** **Manual Trigger**.
2. Add **Basic LLM Chain** (or **AI Agent**).
3. Attach the chat model that uses the credential from 3.3.
4. **Model:** **`qwen2.5:7b`**. Turn **Enable Thinking** **off** if the 7B has no thinking mode.
5. Prompt: `Say hello in one sentence`. **Save.** **Execute workflow.**

First run can take several seconds (Mac cold load). You want a short sentence and Mac `ollama ps` on **GPU**.

### Verify

- [ ] Endpoint is `https://ollama.<org>.edgible.com/v1` and the **secret**, test OK.
- [ ] Model is **`qwen2.5:7b`**, not qwen3-coder.
- [ ] Sandbox on the **n8n** VM: healthz OK; AI settings test OK; **no** Edgible app on 8080.
- [ ] Optional: SearXNG URL `http://searxng:8080` in AI settings; **no** public SearXNG port.
- [ ] Execute returns text; Mac `ollama ps` is GPU.
- [ ] **ollama** app is still **api-key**. The Mac guest still is not running n8n.

---

## Next

[4. OpenClaw uses that URL](04-openclaw-uses-ollama.md). Series: [README](README.md).
