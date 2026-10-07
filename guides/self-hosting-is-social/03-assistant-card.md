# 3. The assistant card

**A chat over your own documents, and the model that answers, written as one card.**

## 3.0 Why

A hosted chat answers from files you upload to someone else. This chapter publishes the other arrangement: Open WebUI and Ollama on a machine you own. The chat is `org`. The model is `api-key`. There is no earlier series to tear down first.

Both apps are place `desk`. This chapter maps that place to `minipc`.

![The assistant card lists two apps in one place, and no hostnames. Place desk is one serving device: assistant is chat over your documents on port 8088, org login. ollama is chat and embedding models on port 11434, bearer key. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/cards/assistant/images/card-light.svg#only-light)
![The assistant card lists two apps in one place, and no hostnames. Place desk is one serving device: assistant is chat over your documents on port 8088, org login. ollama is chat and embedding models on port 11434, bearer key. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/cards/assistant/images/card-dark.svg#only-dark)

**Where you run this:** the serving device that will hold the model. A 4 GB guest cannot. `qwen2.5:7b` needs room on the order of 8 GB free, with Open WebUI beside it. Follow the [assistant card](https://github.com/Edgible/cards/blob/main/cards/assistant/README.md) in your home directory.

## 3.1 The job

You follow the How on the assistant card, then ask one question of the sample document.

**Done when**

- `edgible app list` shows `assistant` with `org` and `ollama` with `api-key`.

**Need first:** [Start here](../start-here/README.md), so a serving agent is installed on the machine that will hold the model. `hello-world` can stay. Port `8088` is free. The website card's site uses `8080`, so the two can run on one machine.

**Not this chapter:** the commands, the Compose file, and `card.env`. Those are the [assistant card](https://github.com/Edgible/cards/blob/main/cards/assistant/README.md).

## 3.2 How

The commands are on the [assistant card](https://github.com/Edgible/cards/blob/main/cards/assistant/README.md). In your home directory:

1. Fetch the card.
2. Edit `card.env`. Set `DEVICE` to `minipc`.
3. Start the containers.
4. Pull the models.
5. Publish.

```bash
edgible app list
```

`edgible app list` shows `assistant` with `org` and `ollama` with `api-key`.

## 3.3 Getting started

Follow Getting Started on the [assistant card](https://github.com/Edgible/cards/blob/main/cards/assistant/README.md).

## Verify

- [ ] `edgible app list` shows `assistant` with `org` and `ollama` with `api-key`.

## Next

[Self Hosting is Social](README.md). The website card is [The website card](01-website-card.md). The n8n card is [The n8n card](02-n8n-card.md).
