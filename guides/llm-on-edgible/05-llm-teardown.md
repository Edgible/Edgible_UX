# 5. Tear down the published LLM

**The inference hostname gone, the key revoked, and the Mac back on loopback.**

## 5.0 Why

Of everything in these guides, this is the one worth being careful about. `ollama` is an `api-key` app in front of a GPU. As long as the hostname exists, anyone holding that secret can run inference on your hardware from anywhere, and a secret you pasted into an n8n credential, an OpenClaw config and a shell history is a secret in more places than you can remember.

The Mac also ends this series in a state it did not start in. Chapter 2 set `OLLAMA_HOST` to `0.0.0.0:11434`, so Ollama is listening on every interface the Mac has, not only loopback. That is fine while the virt LAN is the only network reaching it, and it is worth undoing when you are finished.

Three machines are involved, so this chapter is ordered by blast radius: the public hostname first, then the callers that used it, then the local plumbing, then the weights if you want the disk back.

```
delete first    app ollama            the public hostname and its api-key
then            n8n credentials       OpenClaw provider config
then            ollama-forward        socat and its systemd unit on the guest
last            OLLAMA_HOST           the Mac back to loopback, weights optional
```

**Where you run this:** `edgible` on the **Ubuntu guest**, the credential deletes in the **n8n UI**, `openclaw config` on the **OpenClaw VM**, and the last two sections on the **macOS host**.

## 5.1 The job

You delete the `ollama` app, remove the credentials that carried its secret, stop and remove the loopback forwarder, and put the Mac's Ollama back on localhost.

**Done when**

- `edgible app list` no longer shows `ollama`.
- The HTTPS origin fails from a phone on cellular, with the Bearer token that used to work.
- n8n has no Ollama credentials left, and OpenClaw is off `ollama/gpt-oss:20b`.
- `ollama-forward.service` is gone, and nothing is listening on `11434` on the guest.
- The Mac's Ollama is back on `127.0.0.1:11434`.
- `hello-world` still loads, and `edgible device health` is still OK.

**Need first:** nothing beyond having done the series. Skip any step for a chapter you never did.

**Not this chapter:** deleting the Ubuntu VM, tearing down [n8n on Edgible](../n8n-on-edgible/README.md) or [OpenClaw on Edgible](../openclaw-on-edgible/README.md) themselves, or `edgible auth logout`. Those two guides have their own teardown chapters, and both of those machines can stay exactly as they are.

## 5.2 Delete the app and the key

On the Ubuntu guest. The app goes first, because deleting it is what makes the secret worthless everywhere it has been copied to:

```bash
edgible app list
edgible app delete --name ollama
```

Deleting the app removes its API keys with it. If you would rather revoke a key while keeping the app, that is `edgible app api-keys list --app-id <ollama-app-id>` then `api-keys delete` on the id.

**Smoke test.** From a phone on cellular, or any laptop off the LAN, with the secret that worked in 2.5:

```bash
curl -sS -o /dev/null -w '%{http_code}\n' \
  "https://ollama.<org>.edgible.com/api/tags" \
  -H "Authorization: Bearer $EDGIBLE_APP_KEY"
```

You want a failure: a connection error, or a `404` from the gateway. A `200` with tags JSON means the app is still there. Nothing local has changed yet, which is the point of doing this first: Ollama is still serving on the Mac, and it is no longer reachable from the internet.

## 5.3 Remove the callers' credentials

The secret is dead, but leaving it in a credential store means it turns up in a backup later, and a workflow pointed at a hostname that no longer resolves fails in a confusing way.

In n8n, from [chapter 3](03-n8n-uses-ollama.md), on the n8n VM's browser UI: open **Credentials**, delete the Ollama credential used by the chat model node and the OpenAI-compatible credential used by the AI Assistant. Then deactivate or delete the workflow that used them. If you replaced `~/n8n/docker-compose.yml` in 3.4 to add the sandbox and SearXNG, and you do not want those running any more:

```bash
cd ~/n8n && docker compose down
```

Put back the compose file from [n8n on Edgible, chapter 3](../n8n-on-edgible/03-n8n-public-webhook-hostname.md) before `docker compose up -d` again, or the editor loses `WEBHOOK_URL` and your public webhook hostname stops printing the right origin.

In OpenClaw, from [chapter 4](04-openclaw-uses-ollama.md), on the OpenClaw VM:

```bash
openclaw models set google/gemini-2.5-flash
openclaw config delete models.providers.ollama
openclaw gateway restart
openclaw models list --provider ollama
```

Set whichever model you were on before as the primary. The `list` should now print nothing for that provider. If `config delete` is not in your build, empty the values instead: the `apiKey` is the one that matters.

**Smoke test.** `openclaw agent --model … hello` answers on the model you just set, and no chat turn hangs waiting for a hostname that is gone.

## 5.4 Stop the forwarder on the guest

The `socat` unit only forwarded loopback to the Mac, and Edgible is no longer publishing that port, so this is tidying rather than exposure. On the Ubuntu guest:

```bash
sudo systemctl disable --now ollama-forward.service
sudo rm -f /etc/systemd/system/ollama-forward.service /usr/local/bin/ollama-forward.sh
sudo systemctl daemon-reload
```

`sudo apt-get purge -y socat` if nothing else on the guest uses it.

**Smoke test.** On the guest:

```bash
systemctl status ollama-forward.service
ss -ltnp | grep 11434
```

You want `Unit ollama-forward.service could not be found` and no output from `ss`.

## 5.5 Put the Mac back on loopback

macOS host, Terminal.app. This undoes the bind from 2.2:

```bash
launchctl unsetenv OLLAMA_HOST
killall Ollama
open -a Ollama
```

**Smoke test.** On the Mac:

```bash
lsof -nP -iTCP:11434 -sTCP:LISTEN
```

You want `127.0.0.1:11434`, not `*:11434`. Local chats still work; nothing on the LAN can reach the model any more.

If you kept a firewall exception for Ollama when you set this up, remove it in **System Settings → Network → Firewall → Options**.

## 5.6 The weights, if you want the disk back

Models are the largest thing this series put on your machine: a 7B is roughly 4 GB and `gpt-oss:20b` roughly 13 GB. They are also the slowest thing to get back, so this is a separate decision from everything above.

```bash
ollama ls
ollama rm gpt-oss:20b
ollama rm qwen2.5:7b
ollama rm nomic-embed-text
```

Keep any tag you use locally. Removing Ollama itself is dragging **Ollama.app** to the Bin, plus `rm -rf ~/.ollama` for the model store and history.

## Verify

- [ ] `edgible app list` no longer shows `ollama`.
- [ ] The HTTPS origin fails from a phone on cellular with the old Bearer token.
- [ ] n8n has no Ollama credentials left, and OpenClaw is off `ollama/gpt-oss:20b`.
- [ ] `systemctl status ollama-forward.service` reports no such unit, and `ss` shows nothing on `11434`.
- [ ] `lsof` on the Mac shows `127.0.0.1:11434`, not `*:11434`.
- [ ] `hello-world` still loads and `edgible device health` is OK.

## Next

The VM, the serving agent and Hello World are all still there. [Website on Edgible](../website-on-edgible/README.md) publishes a site with self-hosted analytics and monitoring, and [n8n on Edgible](../n8n-on-edgible/README.md) publishes one process on two hostnames with two auth modes. Series: [README](README.md).
