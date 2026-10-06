# 3. The assistant card

**A chat over your own documents, and the model that answers, written as one card.**

## 3.0 Why

A hosted chat answers from files you upload to someone else. This chapter publishes the other arrangement: Open WebUI and Ollama on a machine you own. The chat is `org`. The model is `api-key`. [The assistant card](https://github.com/Edgible/cards/blob/main/cards/assistant/README.md) is that pattern. There is no earlier series to tear down first.

Both apps are place `desk`. This chapter maps that place to `minipc`. Open WebUI calls Ollama on the machine. The sample document stays a file you upload after the chat is published.

![The assistant card lists two apps in one place, and no hostnames. Place desk is one serving device: assistant is chat over your documents on port 8088, org login. ollama is chat and embedding models on port 11434, bearer key. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/cards/assistant/card-light.svg#only-light)
![The assistant card lists two apps in one place, and no hostnames. Place desk is one serving device: assistant is chat over your documents on port 8088, org login. ollama is chat and embedding models on port 11434, bearer key. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/cards/assistant/card-dark.svg#only-dark)

**Where you run this:** the serving device that will hold the model. A 4 GB guest cannot. `qwen2.5:7b` needs room on the order of 8 GB free, with Open WebUI beside it. The [assistant card](https://github.com/Edgible/cards/blob/main/cards/assistant/README.md) fetches the Compose file and pulls the models.

## 3.1 The job

You fetch the assistant card, follow its README, generate `~/assistant.stack.yml` from the card, deploy it, and ask one question of the sample document.

**Done when**

- `~/assistant-card.yml` lists `assistant` on port `8088` with `org`, and `ollama` on port `11434` with `api-key`.
- `assistant` names `ghcr.io/open-webui/open-webui:main`. `ollama` names `ollama/ollama:latest`.
- The card has no `deviceName`, no `<org>.edgible.com` hostname, and no organization id.
- Both applications name the assistant Compose file in the cards repo.
- Both have `place: desk`.
- `ss` shows `127.0.0.1:8088` and `127.0.0.1:11434`.
- `edgible stack validate -f ~/assistant.stack.yml` reports 2 applications: `assistant`, `ollama`.
- `edgible app list` shows `assistant` with `org` and `ollama` with `api-key`.
- In the assistant, "what are the support hours?" is answered with weekdays 9 to 5.

**Need first:** [Start here](../start-here/README.md), so a serving agent is installed on the machine that will hold the model. `hello-world` can stay. Port `8088` is free. The website card's site uses `8080`, so the two can run on one machine.

**Not this chapter:** a second copy of the card, a public chat with no login, or a separate vector database. The file is [cards/assistant/card.yml](https://github.com/Edgible/cards/blob/main/cards/assistant/card.yml). [card-to-stack.py](https://github.com/Edgible/cards/blob/main/tools/card-to-stack.py) writes the stack file from that card. Your own PDFs are the same upload, after the sample works.

## 3.2 Fetch the assistant card

The field meanings are the same as [The website card](01-website-card.md). The files and the model pulls are on the [assistant card](https://github.com/Edgible/cards/blob/main/cards/assistant/README.md).

On the serving device:

```bash
curl -fsSL https://raw.githubusercontent.com/Edgible/cards/main/cards/assistant/card.yml -o ~/assistant-card.yml
```

`org` in the file is the auth mode `org`. `api-key` is the auth mode `api-key`. `from` is the image name. `place` is `desk` on both apps, so they stay on one serving device. The Compose file is already bound to `127.0.0.1`. This card has no `tailor.sh`.

## 3.3 Start the containers

Follow the [assistant card](https://github.com/Edgible/cards/blob/main/cards/assistant/README.md). It fetches `docker-compose.yml` and `sample-help.pdf`, starts the containers, and pulls `qwen2.5:7b` and `nomic-embed-text`. The pulls are large.

Then:

```bash
ss -ltnp | grep 8088
ss -ltnp | grep 11434
docker exec ollama ollama ls
```

`127.0.0.1:8088` and `127.0.0.1:11434` are listening. `ollama ls` lists `qwen2.5:7b` and `nomic-embed-text`.

## 3.4 Generate the stack file and deploy it

The ports from 3.3 are listening. `edgible stack deploy` reads a stack file, and each app in it is `pre-existing`, so deploy publishes those ports. [card-to-stack.py](https://github.com/Edgible/cards/blob/main/tools/card-to-stack.py) writes that file from the card. It reads `~/assistant-card.yml`, takes the organization id from `edgible config get organizationId`, and writes one Application document per app. `--device minipc` places both on the serving device from [Start here](../start-here/01-edgible-on-vm.md). Auth mode `org` in the card is written `edgible-login` in the stack file. Auth mode `api-key` stays `api-key`.

```bash
curl -fsSL https://raw.githubusercontent.com/Edgible/cards/main/tools/card-to-stack.py -o ~/card-to-stack.py
python3 ~/card-to-stack.py ~/assistant-card.yml --device minipc > ~/assistant.stack.yml
edgible stack validate -f ~/assistant.stack.yml
edgible stack deploy -f ~/assistant.stack.yml
edgible app list
```

The report says 2 applications, `assistant` and `ollama`, each `pre-existing`. `edgible app list` shows `assistant` with `org` and `ollama` with `api-key`.

## 3.5 Ask the sample document

The hostname exists now. The [assistant card](https://github.com/Edgible/cards/blob/main/cards/assistant/README.md) is the rest: sign in with `org`, create the Open WebUI admin, set the embedding model to `nomic-embed-text`, upload `sample-help.pdf`, and attach that collection to the chat model.

Ask: what are the support hours? The answer is the sentence in the sample. Support hours are weekdays 9 to 5.

## Verify

- [ ] `grep -nE 'name: (assistant|ollama)|port:|authModes:' ~/assistant-card.yml` shows `assistant` on port `8088` with `org`, and `ollama` on port `11434` with `api-key`.
- [ ] `grep -n 'from:' ~/assistant-card.yml` shows `ghcr.io/open-webui/open-webui:main` and `ollama/ollama:latest`.
- [ ] `grep -nE 'deviceName|organization' ~/assistant-card.yml` prints nothing.
- [ ] `grep -n 'edgible.com' ~/assistant-card.yml` prints nothing.
- [ ] `grep -n 'compose:' ~/assistant-card.yml` shows `https://raw.githubusercontent.com/Edgible/cards/main/cards/assistant/docker-compose.yml` under both apps.
- [ ] `grep -n 'place:' ~/assistant-card.yml` shows `desk` for both.
- [ ] `ss -ltnp | grep 8088` shows `127.0.0.1:8088`. `ss -ltnp | grep 11434` shows `127.0.0.1:11434`.
- [ ] `edgible stack validate -f ~/assistant.stack.yml` reports 2 applications: `assistant`, `ollama`.
- [ ] `edgible app list` shows `assistant` with `org` and `ollama` with `api-key`.
- [ ] In the assistant, "what are the support hours?" is answered with weekdays 9 to 5.

## Next

[Self Hosting is Social](README.md). The website card is [The website card](01-website-card.md). The n8n card is [The n8n card](02-n8n-card.md).
