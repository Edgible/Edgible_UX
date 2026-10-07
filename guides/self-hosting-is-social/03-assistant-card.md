# 3. The assistant card

**A chat over your own documents, and the model that answers, written as one card.**

## 3.0 Why

A hosted chat answers from files you upload to someone else. This chapter publishes the other arrangement: Open WebUI and Ollama on a machine you own. The chat is `org`. The model is `api-key`. [The assistant card](https://github.com/Edgible/cards/blob/main/cards/assistant/README.md) is that pattern. There is no earlier series to tear down first.

Both apps are place `desk`. This chapter maps that place to `minipc`. Open WebUI calls Ollama on the machine. The sample document stays a file you upload after the chat is published.

![The assistant card lists two apps in one place, and no hostnames. Place desk is one serving device: assistant is chat over your documents on port 8088, org login. ollama is chat and embedding models on port 11434, bearer key. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/cards/assistant/images/card-light.svg#only-light)
![The assistant card lists two apps in one place, and no hostnames. Place desk is one serving device: assistant is chat over your documents on port 8088, org login. ollama is chat and embedding models on port 11434, bearer key. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/cards/assistant/images/card-dark.svg#only-dark)

**Where you run this:** the serving device that will hold the model. A 4 GB guest cannot. `qwen2.5:7b` needs room on the order of 8 GB free, with Open WebUI beside it. Follow the [assistant card](https://github.com/Edgible/cards/blob/main/cards/assistant/README.md) in your home directory. The place is `minipc`.

## 3.1 The job

You follow the assistant card: fetch it, edit `card.env`, start the containers, pull the models, publish the two apps, and ask one question of the sample document.

**Done when**

- `~/assistant/card.yml` lists `assistant` on port `8088` with `org`, and `ollama` on port `11434` with `api-key`.
- `assistant` names `ghcr.io/open-webui/open-webui:latest`. `ollama` names `ollama/ollama:latest`.
- The card has no `deviceName`, no `<org>.edgible.com` hostname, and no organization id.
- The card has no `resources` section. The Compose file sits in the card directory.
- Both have `place: desk`.
- `ss` shows `127.0.0.1:8088` and `127.0.0.1:11434`.
- `edgible app list` shows `assistant` with `org` and `ollama` with `api-key`.
- In the assistant, "what are the support hours?" is answered with weekdays 9 to 5.

**Need first:** [Start here](../start-here/README.md), so a serving agent is installed on the machine that will hold the model. `hello-world` can stay. Port `8088` is free. The website card's site uses `8080`, so the two can run on one machine.

**Not this chapter:** a second copy of the card, a public chat with no login, or a separate vector database. The file is [cards/assistant/card.yml](https://github.com/Edgible/cards/blob/main/cards/assistant/card.yml). Your own PDFs are the same upload, after the sample works.

## 3.2 Fetch the assistant card

The field meanings are the same as [The website card](01-website-card.md). The files and the model pulls are on the [assistant card](https://github.com/Edgible/cards/blob/main/cards/assistant/README.md).

On the serving device, in your home directory, follow step 1 of the [assistant card](https://github.com/Edgible/cards/blob/main/cards/assistant/README.md). Running that step again replaces `card.env`. The file is `~/assistant/card.yml`.

`org` in the file is the auth mode `org`. `api-key` is the auth mode `api-key`. `from` is the image name. `place` is `desk` on both apps, so they stay on one serving device. The Compose file sits in the card directory. `card.yml` does not name it.

## 3.3 Edit card.env and start

Follow steps 2, 3, and 4 of the [assistant card](https://github.com/Edgible/cards/blob/main/cards/assistant/README.md). Set `DEVICE` to `minipc`.

```bash
ss -ltnp | grep 8088
ss -ltnp | grep 11434
docker exec ollama ollama ls
```

`127.0.0.1:8088` and `127.0.0.1:11434` are listening. `ollama ls` lists `qwen2.5:7b` and `nomic-embed-text`.

## 3.4 Publish

The ports from 3.3 are listening. Follow step 5 of the [assistant card](https://github.com/Edgible/cards/blob/main/cards/assistant/README.md). The organization id comes from the logged-in CLI.

```bash
edgible app list
```

`edgible app list` shows `assistant` with `org` and `ollama` with `api-key`.

## 3.5 Getting started

Follow Getting Started on the [assistant card](https://github.com/Edgible/cards/blob/main/cards/assistant/README.md).

Ask: what are the support hours? The answer is the sentence in the sample. Support hours are weekdays 9 to 5.

## Verify

- [ ] `grep -nE 'name: (assistant|ollama)|port:|authModes:' ~/assistant/card.yml` shows `assistant` on port `8088` with `org`, and `ollama` on port `11434` with `api-key`.
- [ ] `grep -n 'from:' ~/assistant/card.yml` shows `ghcr.io/open-webui/open-webui:latest` and `ollama/ollama:latest`.
- [ ] `grep -nE 'deviceName|organization' ~/assistant/card.yml` prints nothing.
- [ ] `grep -n 'edgible.com' ~/assistant/card.yml` prints nothing.
- [ ] `grep -nE 'resources:|compose:|changes:' ~/assistant/card.yml` prints nothing.
- [ ] `grep -n 'place:' ~/assistant/card.yml` shows `desk` for both.
- [ ] `ss -ltnp | grep 8088` shows `127.0.0.1:8088`. `ss -ltnp | grep 11434` shows `127.0.0.1:11434`.
- [ ] `edgible app list` shows `assistant` with `org` and `ollama` with `api-key`.
- [ ] In the assistant, "what are the support hours?" is answered with weekdays 9 to 5.

## Next

[Self Hosting is Social](README.md). The website card is [The website card](01-website-card.md). The n8n card is [The n8n card](02-n8n-card.md).
