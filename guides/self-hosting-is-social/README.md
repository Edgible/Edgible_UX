# Self Hosting is Social: chapters

**A proven solution can be shared as a pattern, so someone else can reproduce it.**

Self-hosting keeps a service on hardware you own. The data stays there, and so do the passwords and the volumes. That is a private arrangement, which is why calling it social sounds like a contradiction. The contradiction is the point. The service stays private. The pattern of how you published it is what another person can use.

A useful self-hosted setup is a set of decisions: which programs, which images, which ports, which auth mode on each hostname, which files they need, and which of those programs share a serving device. Those decisions are what took the time. They usually live in one person's command history. A screenshot shows that it worked. It does not give the next person a way to stand the same thing up on their own machine.

Edgible is what makes the pattern separable from your machine. Each published app already has its own hostname and its own auth mode, `None`, `org`, or `api-key`, independent of the program behind it. A card writes those decisions down and leaves out what is yours alone: the device name, the hostnames, and the organization id. Whoever receives the card maps each place to a serving device they have, and Edgible publishes the apps on their hostnames.

The card is meant to be complete enough that the person sharing it does not also have to host the programs. An image is named by the registry that already publishes it. A Compose file is named by its public URL. When that file needs a change to be safe to publish this way, such as binding a port to `127.0.0.1`, the card lists the change instead of asking the sharer to rehost the file. Passwords and volume data are still created on the machine that runs the pattern.

What you stop doing is rebuilding a known setup from memory. What you can hand over is the pattern. The chapters after this page are examples of that. The first is a website. The second is n8n, starting from the Compose file n8n publishes.

## The card

[card.schema.json](https://github.com/Edgible/cards/blob/main/tools/card.schema.json) is the source of truth for a card. The cards themselves live in [Edgible/cards](https://github.com/Edgible/cards). An assistant that can run `edgible` reads this section, writes a file that satisfies that schema, and you check it before you share it. The block below is the same shape, with placeholders, so it is not itself a valid card. [1. The website card](01-website-card.md) and [2. The n8n card](02-n8n-card.md) fetch the real files from that repo.

```yaml
apiVersion: v1
kind: Card
metadata:
  name: pattern-name
  description: one line

applications:
  - name: app1
    what: what this program is
    from: registry/image
    database: database-image
    port: 8080
    protocol: https
    subtype: existing
    published: true
    authModes: [none]
    place: place-name
    resources:
      compose: https://<public-gold-compose-url>
      files:
        - https://<public-url-of-a-file-the-compose-expects>
      changes:
        - Bind the host port to 127.0.0.1 only
      env: [SOME_SECRET]
```

`kind: Card` is the shareable file. [card-to-stack.py](https://github.com/Edgible/cards/blob/main/tools/card-to-stack.py) adds your device name and your organization id when you publish, and that output is the stack file.

Every application has `name`, `what`, `from`, `port`, `protocol`, `subtype`, `published`, `authModes`, and `place`. `protocol` is `https`. `subtype` is `existing`. `published` is `true`. `database` is optional, and names a database image in the same Compose file. `files`, `changes`, and `env` are optional.

`authModes` is `none`, `org`, or `api-key`. `none` in the file is the auth mode `None`. An export that says `edgible-login` is written `org` on the card.

`place` is a topology name you choose. It is not a device name and not a device id. Applications with the same `place` run on one serving device. Two applications that are one process share a `place`, a port, a `from`, and the same `resources`.

`from` is the image name, without a device and without your organization. `resources.compose` is a public `https` URL. For an `existing` app, assume the gold Compose file for that image. `changes` lists the edits to make before running that file, such as binding the host port to `127.0.0.1`. Omit `changes` when the URL is already the file to run. When the image has no published Compose file, omit `compose` until you put a public URL there. `env` names variables to generate on the machine that runs the pattern. The card does not carry the values.

Leave these off the card: `deviceName`, `deviceId`, `organization`, hostnames, passwords, volume data, and a timezone. A hostname setting is written as a change, "the hostname of this app" or "the hostname of the `None` app", not as your `<org>.edgible.com` name.

Fill it from the apps you named. On the guest:

```bash
edgible application export app1 --redacted
docker ps --format '{{.Image}} {{.Ports}}'
```

Repeat the export for each app. Copy `metadata.name`, the workload `containerPort`, and the access `modes`. Drop `deviceId`, `organization`, and `hostname` after you have used the device id for one decision: exports that share a device id and a port are one process. Match that port to the `Ports` column of `docker ps` to read `from`. The export of an `existing` app does not record the image.

Check a card against the schema. This needs the `pyyaml` and `jsonschema` packages.

```bash
curl -fsSL https://raw.githubusercontent.com/Edgible/cards/main/tools/card.schema.json -o ~/card.schema.json
python3 -c '
import json, sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator
schema = json.loads(Path.home().joinpath("card.schema.json").read_text())
card = yaml.safe_load(Path(sys.argv[1]).read_text())
Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(card)
print("ok")
' ~/website-card.yml
```

`ok` means the file matches [card.schema.json](https://github.com/Edgible/cards/blob/main/tools/card.schema.json). A file that still has `deviceName`, `organization`, or a placeholder URL fails.

Chapters share a shape: a one-line hook under the title, then **N.0 Why** (what is missing without this chapter, and which machine you run it on), then **N.1 The job** (what you'll do, how you'll know, what you need, what this is not). Steps after that, a **Verify** checklist that mirrors *Done when*, and **Next** at the end.

**Need first:** [Start here](../start-here/README.md), so a serving agent is installed. The website example also needs [Tear down the website stack](../website-on-edgible/06-website-teardown.md). The n8n example also needs [Tear down n8n](../n8n-on-edgible/06-n8n-teardown.md).

| # | Chapter | Smoke test |
| --- | --- | --- |
| 1 | [1. The website card](01-website-card.md) | `edgible app list` shows `site`, `analytics`, `umami` and `status` again |
| 2 | [2. The n8n card](02-n8n-card.md) | `edgible app list` shows `n8n` (`org`) and `n8n-hooks` (`None`) |
