# 2. The n8n card

**One n8n process, two auth modes, written as one card.**

## 2.0 Why

[n8n on Edgible](../n8n-on-edgible/README.md) publishes one process on port `5678` twice: the editor with `org`, and a webhook hostname with `None`. [Tear down n8n](../n8n-on-edgible/06-n8n-teardown.md) deleted those hostnames and stopped the container. This chapter runs that pattern again from the [n8n card](https://github.com/Edgible/cards/blob/main/n8n/README.md).

Both apps are place `workhorse`. This chapter maps that place to `minipc`.

![The n8n card lists two apps in one place, and no hostnames. Place workhorse is one serving device: n8n is n8n editor on port 5678, org login. n8n-hooks is n8n webhooks, same process as n8n on port 5678, open to anyone. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/n8n/images/card-light.svg#only-light)
![The n8n card lists two apps in one place, and no hostnames. Place workhorse is one serving device: n8n is n8n editor on port 5678, org login. n8n-hooks is n8n webhooks, same process as n8n on port 5678, open to anyone. The card names no device and no organization.](https://raw.githubusercontent.com/Edgible/cards/main/n8n/images/card-dark.svg#only-dark)

**Where you run this:** the **Ubuntu guest**. Follow the [n8n card](https://github.com/Edgible/cards/blob/main/n8n/README.md) in your home directory.

## 2.1 The job

You follow the How on the n8n card.

**Done when**

- `edgible app list` shows `n8n` with `org` and `n8n-hooks` with `None`.

**Need first:** [Tear down n8n](../n8n-on-edgible/06-n8n-teardown.md), including the serving agent still installed. One published app stays, such as `hello-world`, so you can read the org label into `ORG_LABEL`.

**Not this chapter:** the commands, the Compose file, and `card.env`. Those are the [n8n card](https://github.com/Edgible/cards/blob/main/n8n/README.md).

## 2.2 How

The commands are on the [n8n card](https://github.com/Edgible/cards/blob/main/n8n/README.md). In your home directory:

1. Fetch the card.
2. Edit `card.env`. Set `DEVICE` to `minipc`. Set `ORG_LABEL` to the label from a hostname you already have.
3. Start the containers.
4. Create the n8n owner.
5. Publish.

```bash
edgible app list
```

`edgible app list` shows `n8n` with `org` and `n8n-hooks` with `None`.

## 2.3 Getting started

Follow Verify on the [n8n card](https://github.com/Edgible/cards/blob/main/n8n/README.md).

## Verify

- [ ] `edgible app list` shows `n8n` with `org` and `n8n-hooks` with `None`.

## Next

[3. The assistant card](03-assistant-card.md). Series: [README](README.md). The website card is [The website card](01-website-card.md).
