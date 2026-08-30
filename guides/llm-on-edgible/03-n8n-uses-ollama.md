# 3. n8n uses the published Ollama URL

**One published hostname serves both n8n workflow nodes and the AI Assistant.**

## 3.0 Why

n8n is on its own VM on a different home computer, so it has no local model. Do not give it one. Installing Ollama next to n8n means CPU inference on a box with no GPU. Pointing it at the Mac’s UTM address (`192.168.64.1`) cannot work, because that virt LAN exists only between the Mac and its own guest. A mesh VPN would mean enrolling every machine that ever wants a completion. The published `api-key` hostname from [chapter 2](02-edgible-to-ollama.md) already solves it: n8n sends HTTPS plus a Bearer secret, and the weights and the Metal GPU stay on the Mac.

n8n uses that one hostname in two shapes. Workflow nodes speak Ollama’s native API at the bare origin; the built-in **AI Assistant** speaks OpenAI-compatible `/v1`. Same secret, same GPU, two credentials and two models. The Assistant also needs a sandbox and a search backend running beside n8n. Do not mix the two URLs, do not put the Edgible secret on `n8n-hooks`, do not set the `ollama` app to `None`, and do not run n8n or the sandbox on the Mac UTM guest. The Mac serves Ollama (and the website); n8n is the remote self-hosted caller.

![n8n on another box you own calls ollama.<org>.edgible.com with a bearer key, the Basic LLM Chain node on the bare hostname and the AI Assistant chat on the /v1 path. Both arrive through socat on the Ubuntu guest at Ollama.app on the macOS host.](../../images/diagrams/llm-on-edgible-03-light.svg#only-light)
![n8n on another box you own calls ollama.<org>.edgible.com with a bearer key, the Basic LLM Chain node on the bare hostname and the AI Assistant chat on the /v1 path. Both arrive through socat on the Ubuntu guest at Ollama.app on the macOS host.](../../images/diagrams/llm-on-edgible-03-dark.svg#only-dark)

**Where you run this:** almost everything is on the **n8n VM** (its browser UI and `docker compose` in `~/n8n`); only `ollama show` / `ollama ps` and any missing `ollama pull` run on the **macOS host**.

### Two use cases

| | 1. Invoke the LLM from a workflow | 2. n8n AI Assistant |
| --- | --- | --- |
| What it is | A node on the canvas (e.g. **Basic LLM Chain** + **Ollama Chat Model**). Cron, webhooks, other nodes can call the model. | n8n’s instance chat: it helps build/edit workflows and can run generated code in a sandbox. |
| Edgible URL | `https://ollama.<org>.edgible.com`, no `/v1` (native `/api/chat`) | `https://ollama.<org>.edgible.com/v1`, with `/v1` |
| Also needs | One Ollama credential. **Enable Thinking → off** on the node. Model expression `{{ 'qwen2.5:7b' }}`. | Self-hosted `n8n-sandbox` + SearXNG on the n8n VM, not Daytona. |
| Thinking | Must be off (node option). 7B cannot think. | Must be on in the model. n8n always sends thinking; there is no off switch. Tag must list thinking in `ollama show`. |
| Smoke test | **Execute workflow** → a sentence. Mac `ollama ps` on GPU. | Hello, then: visit edgible.com and summarise using the product with n8n. |
| Model | `qwen2.5:7b`, proven. | `gpt-oss:20b`, proven for real Assistant chat including search, not only Hello. Not `qwen2.5:7b`. |

## 3.1 The job

Do both use cases. Same Edgible secret, two models.

**Done when**

- Assistant: `ollama show` lists thinking; `/v1`; `gpt-oss:20b`; Hello replies; edgible.com + n8n (or similar) uses the web. Workflow: Base URL without `/v1`; `{{ 'qwen2.5:7b' }}`; thinking off. Same Edgible secret.
- Workflow model is not grey llama3.2, not qwen3-coder. Assistant model is not a non-thinking 7B.
- Sandbox on the n8n VM: healthz OK; AI settings test OK; no Edgible app on 8080.
- SearXNG URL `http://searxng:8080` in AI settings; no public SearXNG port.
- Execute returns text; Assistant Hello and a search turn return text; Mac `ollama ps` is GPU.
- `ollama` app is still `api-key`. The Mac guest still is not running n8n.

**Need first:** n8n editor on the n8n VM. [Chapter 2](02-edgible-to-ollama.md). Docker Compose v2. ~4 GB / 2 vCPUs spare on that VM for the sandbox runner. For the **AI Assistant**: a tag with thinking in `ollama show` (this chapter uses `gpt-oss:20b`).

**Not this chapter:** n8n on the Mac guest, `qwen3-coder`, Open WebUI/sandbox on the 4 GB UTM VM, Daytona, OpenClaw.

Official sandbox docs: [Docker Compose](https://docs.n8n.io/deploy/host-n8n/install-options/install-using-docker-compose/) and [AI Assistant](https://docs.n8n.io/deploy/host-n8n/configure-n8n/set-up-ai-assistant/).

## 3.2 Two models: the Assistant must support thinking

Ollama’s n8n page uses `qwen3-coder` as an example. Do not pull it (~19 GB).

The n8n **AI Assistant** always sends thinking. That page has no Think-off control. Compose `N8N_INSTANCE_AI_THINKING_ENABLED=false` does not stop it. A connection test only hits `/v1/models`, so it does not prove the tag can think. Hello is the thinking check. A question that needs current web results is the SearXNG check.

On the Mac:

```bash
ollama show gpt-oss:20b
```

You want `thinking` under capabilities. If that word is missing, do not use the tag for the AI Assistant.

| n8n feature | Tag | Thinking | Why |
| --- | --- | --- | --- |
| Workflow | `qwen2.5:7b` | Off (node option) | Fast 7B. Cannot think, so turn it off on the node. |
| AI Assistant chat | `gpt-oss:20b` | Required (model capability) | n8n sends thinking. This tag can (~13 GB). Proven for Assistant work including web search via SearXNG. |

Cannot use for the AI Assistant (no thinking): `qwen2.5:7b`, `llama3.1:8b`, `llama3.2:*`, `mistral:7b`, `phi*`, `deepseek-coder:*`, `codellama:*`. Those are fine for workflows with thinking off.

Can use for the AI Assistant if `ollama show` lists thinking: `gpt-oss:20b` (this chapter), `qwen3.5:27b` (heavier, ~17 GB).

If `gpt-oss:20b` is missing: `ollama pull gpt-oss:20b` on the Mac, not in the UTM guest. Then `ollama show` until you see thinking.

## 3.3 Two credentials

**AI Assistant**: Settings, self-hosted Ollama. Pick the model before you chat:

1. On the Mac, confirm thinking: `ollama show gpt-oss:20b` lists thinking. If you pick `qwen2.5:7b` here, Hello fails with “doesn’t support thinking” even if the connection test passed.
2. Endpoint = `https://ollama.YOUR-ORG.edgible.com/v1` (with `/v1`). No `?think=`; that does nothing.
3. API Key = the secret from [2.5](02-edgible-to-ollama.md).
4. **Model** = `gpt-oss:20b` (same string as `ollama ls`). Not a 7B. Not any tag whose `ollama show` lacks thinking.
5. Save. Connection test succeeds (this still does not prove thinking).

**Ollama Chat Model** in a workflow needs a separate Ollama credential (do not reuse the Assistant URL):

1. Base URL = `https://ollama.YOUR-ORG.edgible.com` (no `/v1`, no `:11434`).
2. Same secret.
3. Save. Connection test succeeds.

Do not use `localhost:11434` or UTM `192.168.64.1` from this VM.

Leave sandbox until 3.4. Workflow model id is §3.5 (`{{ 'qwen2.5:7b' }}`). Assistant Hello is §3.6.

On the workflow node only: **Options → Enable Thinking → off**. Do not try to turn Assistant thinking off with env or a URL query.

## 3.4 Self-hosted sandbox (n8n VM)

Do this on the n8n VM only. Do not add these containers on the Mac UTM guest.

The sandbox is not an Edgible app. n8n reaches `sandbox-api` on the Compose network. Do not publish `8080` / `9090` / `9091`. `sandbox-runner-1` is privileged Docker-in-Docker, so treat it as root on that VM.

Windows host: Compose inside the Linux VM / WSL2, project under `~/n8n` (not `/mnt/c/...`).

This replaces `~/n8n/docker-compose.yml`. The named volume `n8n_data` keeps existing workflows if you already used that name. Sandbox services match n8n’s [Docker Compose install](https://docs.n8n.io/deploy/host-n8n/install-options/install-using-docker-compose/).

```bash
mkdir -p ~/n8n
cd ~/n8n
```

`.env` has four random strings. `SANDBOX_API_KEYS` and `N8N_INSTANCE_AI_SANDBOX_API_KEY` must be identical:

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

Do not commit `.env`. Save this as `~/n8n/searxng-settings.yml` (stock SearXNG only serves HTML; n8n needs JSON):

```yaml
use_default_settings: true
search:
  formats:
    - html
    - json
```

Save this as `~/n8n/docker-compose.yml` (whole file):

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

You want `sandbox-api` healthy, healthz `{"status":"ok"}`, and a log line that the runner registered. n8n still only binds `127.0.0.1:5678`.

Do not set `N8N_INSTANCE_AI_MODEL` to Anthropic, so that Ollama stays in the UI. Change `GENERIC_TIMEZONE` / `TZ` if you need a different zone. If this n8n already has `n8n-hooks`, keep `WEBHOOK_URL` (and any `N8N_HOST` / `N8N_PROTOCOL`) on the n8n `environment` block from [n8n chapter 3](../n8n-on-edgible/03-n8n-public-webhook-hostname.md). Do not add `N8N_INSTANCE_AI_THINKING_ENABLED=false` to “fix” the 7B. It does not stop Assistant thinking; use `gpt-oss:20b` instead.

Then AI settings → sandbox `n8n-sandbox` (not Daytona). **Service URL** = `http://sandbox-api:8080`. **API key** = `SANDBOX_API_KEYS` from `.env` (`grep SANDBOX_API_KEYS .env`). Save. You want a successful test.

Web search is part of the AI Assistant, not an extra. Provider SearXNG. URL = `http://searxng:8080`. No API key. Same Compose network as n8n, not `localhost`, not Edgible. Leave **Brave** empty unless you buy that. Do not publish SearXNG’s port or create an Edgible app for it. Without this URL, Assistant cannot look anything up; `gpt-oss:20b` will still chat from weights only.

If `sandbox-api` never goes healthy: `docker compose logs sandbox-certs` then `sandbox-api`. Runner crash-loop: token mismatch in `.env`. Sandbox test fails: key/URL mismatch, or n8n not on this Compose file.

If the stack is already up without SearXNG: add `SEARXNG_SECRET` to `.env`, write `searxng-settings.yml`, add the `searxng` service and `N8N_INSTANCE_AI_SEARXNG_URL` as above, then `docker compose up -d`.

### 3.4.1 Health check

On the n8n VM, from `~/n8n`. This is what the UI uses: probes from inside the n8n container, plus n8n on loopback.

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

You want: `sandbox-api` healthy, n8n running, `searxng` running, `sandbox-certs` exited 0 (one-shot). Healthz `{"status":"ok"}`. SearXNG JSON that includes `"results"`. n8n `/healthz` `200`. A log line that the runner registered.

Optional. Ollama from the same container (replace host and secret):

```bash
docker compose exec -T n8n wget -qO- \
  --header="Authorization: Bearer YOUR-EDGIBLE-SECRET" \
  "https://ollama.YOUR-ORG.edgible.com/v1/models" | head -c 400 && echo
```

You want JSON that includes `qwen2.5:7b` and `gpt-oss:20b`. 401 = bad secret. Timeout/HTML = Mac Ollama/forwarder down or wrong host.

Do not publish sandbox or SearXNG ports to prove this. `ss` on the VM should still show `5678` on `127.0.0.1` only.

## 3.5 One chain (workflow)

This is use case 1. You do not need **Chat Trigger**. Assistant Hello is §3.6.

1. **Add workflow.** Search **Manual** → **Manual Trigger** (or keep n8n’s “Execute workflow” start node).
2. Search **LLM Chain** → **Basic LLM Chain**. Connect trigger → chain.
3. On the chain’s **Model** stub, **Ollama Chat Model**. Credential Base URL is the Edgible origin without `/v1` (not the Assistant endpoint).
4. The **Model** dropdown often stays empty and shows grey `llama3.2` (n8n’s placeholder, not your Mac). Open the field **fx** / **Expression** and set exactly:

```text
{{ 'qwen2.5:7b' }}
```

5. **Options → Enable Thinking → off**.
6. Chain prompt: `Say hello in one sentence`. **Save**, then **Execute workflow**.

**Smoke test (n8n VM).** First run can take several seconds (Mac cold load). You want a short sentence in the chain output and Mac `ollama ps` on GPU.

## 3.6 Assistant Hello

This is use case 2. Sandbox from 3.4 must already test OK. The Assistant model must support thinking (§3.2), because n8n will send it. `gpt-oss:20b` over Edgible `/v1`, with sandbox + SearXNG on the n8n VM, is the proven stack, including questions that need a web search, not only Hello.

1. AI settings: endpoint with `/v1`, same Edgible secret, model `gpt-oss:20b` (`ollama show` lists thinking). SearXNG URL `http://searxng:8080`.
2. Open the Assistant chat. Send Hello. You want a reply, not “doesn’t support thinking”.
3. Then a question that needs the public site, not weights. This one is proven:

```text
Visit www.edgible.com and summarise how I can use the product with n8n.
```

**Smoke test (n8n VM).** You want a summary that matches the site (self-host, publish n8n, and similar), not a generic n8n blurb and not a refusal to look anything up. Similar prompts that name a URL and ask for a product summary are the same test. Mac `ollama ps` shows `gpt-oss:20b` on GPU.

First run can take a while (20B cold load). If Hello errors on thinking, the model is wrong, not the URL, the sandbox, or `N8N_INSTANCE_AI_THINKING_ENABLED`. If Hello works but search does not, fix SearXNG (§3.4), not the model.

### Verify

- [ ] Assistant: `ollama show` lists thinking; `/v1`; `gpt-oss:20b`; Hello replies; edgible.com + n8n (or similar) uses the web. Workflow: Base URL without `/v1`; `{{ 'qwen2.5:7b' }}`; thinking off. Same Edgible secret.
- [ ] Workflow model is not grey llama3.2, not qwen3-coder. Assistant model is not a non-thinking 7B.
- [ ] Sandbox on the n8n VM: healthz OK; AI settings test OK; no Edgible app on 8080.
- [ ] SearXNG URL `http://searxng:8080` in AI settings; no public SearXNG port.
- [ ] Execute returns text; Assistant Hello and a search turn return text; Mac `ollama ps` is GPU.
- [ ] `ollama` app is still `api-key`. The Mac guest still is not running n8n.

---

## Next

[4. OpenClaw uses that URL](04-openclaw-uses-ollama.md). Series: [README](README.md).
