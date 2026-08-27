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

The sandbox is **not** an Edgible app. n8n reaches `sandbox-api` by Compose service name on the **internal** Docker network. Do **not** publish **8080** / **9090** / **9091**, do **not** port-forward them, do **not** create Edgible apps for them. `sandbox-runner-1` is **privileged** Docker-in-Docker — treat it as root on that VM.

Windows host: run Compose **inside** the Linux VM / **WSL2**. Keep the project under `~/n8n`, not `/mnt/c/...`.

In the n8n project directory (`~/n8n` or wherever `docker compose ps` already shows n8n):

1. Create `.env` (own secrets, not `change-me`). `N8N_INSTANCE_AI_SANDBOX_API_KEY` must equal `SANDBOX_API_KEYS`:

```bash
cat >> .env << 'EOF'
SANDBOX_API_KEYS=replace-with-a-long-random-string
SANDBOX_API_RUNNER_REGISTRATION_TOKEN=replace-with-another-long-random-string
SANDBOX_API_RUNNER_API_KEY=replace-with-a-third-long-random-string
N8N_INSTANCE_AI_SANDBOX_API_KEY=replace-with-a-long-random-string
EOF
```

The first and last values must **match**. Do not commit `.env`.

2. Merge the sandbox services into the **existing** Compose file. Keep your current **n8n** image, `n8n_data` volume, and **`127.0.0.1:5678:5678`** if Edgible already publishes the editor. Add a `sandbox-tls` volume and these services (from n8n’s Compose guide): `sandbox-certs`, `sandbox-api`, `sandbox-runner-1`.

3. On the **n8n** service, add `env_file: .env` if it is not there, `depends_on: sandbox-api` (healthy), and:

```yaml
environment:
  N8N_ENABLED_MODULES: instance-ai
  N8N_INSTANCE_AI_SANDBOX_ENABLED: "true"
  N8N_INSTANCE_AI_SANDBOX_PROVIDER: n8n-sandbox
  N8N_INSTANCE_AI_SANDBOX_API_URL: http://sandbox-api:8080
  N8N_INSTANCE_AI_SANDBOX_IMAGE: ghcr.io/n8n-io/n8n-sandbox-service-sandbox:latest
```

Do **not** set `N8N_INSTANCE_AI_MODEL` to Anthropic/OpenAI — you already chose Ollama in the UI. Do **not** give the sandbox containers the Edgible Ollama secret.

Full service YAML: n8n’s [Docker Compose install](https://docs.n8n.io/deploy/host-n8n/install-options/install-using-docker-compose/) (copy `sandbox-certs` / `sandbox-api` / `sandbox-runner-1` from there). Image for n8n can stay `docker.n8n.io/n8nio/n8n`.

4. Start and check:

```bash
docker compose up -d
docker compose ps
docker compose exec n8n wget -qO- http://sandbox-api:8080/healthz
docker compose logs sandbox-api | grep -i runner
```

You want `sandbox-api` **healthy**, healthz `{"status":"ok"}`, and a log line that the runner registered.

5. Back in n8n **AI settings** → sandbox: provider **n8n-sandbox** (not Daytona). **Service URL** = `http://sandbox-api:8080`. **API key** = the same string as `SANDBOX_API_KEYS`. Save. You want a successful test.

Optional later: bundled **SearXNG** for Assistant web search (same n8n page). Not required for Ollama or a first chain.

If `sandbox-api` never goes healthy: `docker compose logs sandbox-certs` then `sandbox-api`. Runner crash-loop: registration token mismatch. n8n sandbox test fails: URL/key not what `sandbox-api` has, or n8n is not on the same Compose network.

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
- [ ] Execute returns text; Mac `ollama ps` is GPU.
- [ ] **ollama** app is still **api-key**. The Mac guest still is not running n8n.

---

## Next

[4. OpenClaw uses that URL](04-openclaw-uses-ollama.md). Series: [README](README.md).
