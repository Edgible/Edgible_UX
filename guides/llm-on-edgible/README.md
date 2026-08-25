# LLM on Edgible — chapters

**Guide 3. Not written yet.** Do [1. n8n on Edgible](../n8n-on-edgible/README.md) and [2. OpenClaw on Edgible](../openclaw-on-edgible/README.md) first. Do **not** publish a model API in those series.

Both products can call a local or remote LLM you control. This series is that hook-up — one Edgible-published inference URL, then n8n **and** OpenClaw pointed at it. It waits until that model is actually answering on the box that will serve weights.

**The Edgible story here:** a securely consumable HTTPS endpoint for inference on hardware you own (**api-key** for machines, **org** for a human UI). Never **None**. Same VM / serving-device idea as [Edgible on an Ubuntu VM](../openclaw-on-edgible/01-edgible-on-vm.md). OpenClaw on the same LAN as the weights still uses loopback or LAN HTTP until this series says otherwise.

**Planned jobs** (titles will move when the model is up)

| # | Job | Smoke test (draft) |
| --- | --- | --- |
| 1 | Publish the model through Edgible | Cellular `curl` with Bearer returns the model server, not a login page. Port **11434** (or vLLM’s port) not forwarded. Auth is **api-key**, not **None**. |
| 2 | n8n uses that URL | An n8n AI / HTTP node on the **org** editor completes against the same origin |
| 3 | OpenClaw uses that URL | `openclaw agent --model … hello` on the VM talks to `https://<app>.<org>.edgible.com`, not a cloud key |

OpenClaw chapter 9 stays cloud keys plus a **small** same-LAN Ollama failover. n8n stays editor **org** and webhook **None**. The big local/remote model lives here.
