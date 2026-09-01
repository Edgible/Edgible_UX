# Working in this repo

This repo is documentation only. It is published at
[guides.edgible.com](https://guides.edgible.com). It is not the Edgible CLI and
not the OpenClaw skill; the skill lives in
[openclaw-edgible](https://github.com/Edgible/openclaw-edgible).

## Where the content is

The markdown at the repo root is canonical. `build/` and `site/` are generated
by `scripts/build.sh` and are not checked in, so never edit files there.

- `README.md`: the landing page. What Edgible does, why the guides are worth
  reading, and where to start. The guide list here grows as guides are added.
- `capabilities.md`: each Edgible feature mapped to the chapter that proves it.
- `glossary.md`: every term the guides use, defined once. Chapters do not carry
  their own terms section; add a new term here instead.
- `working-with-ai.md`: the markdown sources, `llms.txt` and how to read these
  guides alongside an AI tool.
- `appendix/for-evaluators.md`: where Edgible sits in the ingress and
  self-hosting landscape, for readers comparing approaches. No pricing, no
  product names.
- `guides/<series>/README.md`: chapter list for that series. Series names carry
  no ordinal: reading order lives in the `nav:` in `mkdocs.yml` and in `GUIDES`
  in `scripts/gen_llms.py`, so inserting a series does not mean renumbering
  prose that nothing validates.
- `guides/start-here/01-edgible-on-vm.md` is the shared prerequisite. Every
  series links to it from its `Need first:` line rather than repeating it.
- `guides/<series>/NN-*.md`: one chapter, one job, one smoke test.

## What the build publishes besides pages

`scripts/build.sh` writes several files that no page links to, and each exists
for a reader that is not a person.

- `robots.txt` and `sitemap.xml`, the second with a date per page from git.
- `llms.txt` and `llms-full.txt`, from `scripts/gen_llms.py`.
- A copy of every page's markdown at the same path as its HTML, served
  `noindex` so the pair does not compete in search results.
- `<key>.txt` at the root, from `static/indexnow.key`, which is how IndexNow
  checks that whoever submits URLs controls the site. The key is public by
  design. The deploy repo submits the sitemap's URLs after each deploy, which
  covers Bing, Yandex, Seznam and Naver; Google takes no part in IndexNow and is
  reached through Search Console instead.
- Per-page structured data and titles come from `overrides/main.html`, and
  `scripts/polish_html.py` fixes the canonical URL of the home page and fills in
  image dimensions. Neither is something MkDocs can do here.

## Chapter structure

Every chapter follows the same shape, and new chapters must match it:

1. `# N. Title`
2. A one-sentence bold hook.
3. `## N.0 Why`: what is missing without this chapter, and a
   `**Where you run this:**` line naming the machine for each step.
4. `## N.1 The job`: what you will do, `Done when`, what you need, what this is
   not.
5. Numbered step sections.
6. `## Verify`: a checklist mirroring `Done when` item for item.
7. `## Next`.

## Writing rules

- Reserve bold for the hook, for literal UI labels, and for the theme phrase that
  leads a series entry in a list of guides. Do not bold for emphasis, and never
  bold negations.
- Avoid em dashes. Use a comma, a full stop, or a colon.
- Use literal, searchable terms over metaphor: `auth mode`, `published
  hostname`, `serving agent`. Not doors, locks, or brains.
- `serving agent` is the daemon on the machine. `serving device` is the
  registered record in the console. They are not interchangeable.
- The agent "connects out" or "opens an outbound connection". Not "dials out":
  that is a modem metaphor, and the point being made is about the direction a
  connection is opened in, which the plain wording says better.
- Auth modes are `org`, `api-key` and `None`, always in code font.
- Ports, hostnames, commands, filenames and env vars go in code font.
- Every claim needs a command whose output a reader can check.
- Say nothing about what Edgible costs. No free tier, no paid plan, no limits on
  devices or published apps, and nothing that implies the answer, such as "the
  only cost is electricity". Third-party services are different: a chapter should
  state plainly what an outside account or key asks of the reader.

## Series themes

Each series has one theme, the answer to "why would I care" that the chapters
themselves never stop to give. It appears as the bold hook on the series
`README.md`, as the bold lead in the guide list on `README.md`, and in the
matching paragraph in `capabilities.md`. Keep those three in step. A theme is
stated as a fact the guide demonstrates, never as an adjective: the test is
whether a chapter in that series proves it.

| Series | Theme | The thing you stop doing |
| --- | --- | --- |
| Start here | A page the internet can load, without touching your router | Forwarding a port |
| Website on Edgible | The whole small-site stack, on hardware you own | Giving three outside services a copy of your traffic |
| n8n on Edgible | The back office workhorse, running at 3am in your own building | Handing your API keys to a hosted automation service |
| OpenClaw on Edgible | The agent everyone is currently trying, with its shell and admin console off the internet | Exposing an admin port to reach the agent from a phone |
| LLM on Edgible | Private AI: prompts, documents and weights never leave hardware you own | Sending the questions you would not type into a hosted model |

The themes are also the art direction. Any illustration added to a series should
come from that row (a machine in a room, a phone on cellular, an invoice at
night, a GPU at home), not from generic cloud or network clip art, and never
from the metaphors the writing rules ban.

## Diagrams

Each series index opens with a topology diagram, and so does each chapter that
had one. Both come from `scripts/gen_diagrams.py`, out of a short spec of
callers, published hostnames with their auth modes, loopback ports and notes.
The build regenerates them, so editing an SVG under `static/images/diagrams/` by
hand achieves nothing. Change the spec. Do not add a new diagram as monospace
art in a fenced block: none are left, and one would now look like a mistake.

`SERIES` holds the index diagrams and `CHAPTERS` the chapter ones, keyed by the
series directory and the chapter number, which is also the SVG basename. A
chapter spec has four things an index never needs: a third item on a hostname
tuple, tagging which chapter published it, an empty `hosts` list plus `empty`
for the chapters where nothing is published yet, `machine2` for a second panel
where the service lives on the Mac and the guest only forwards, and `outbound`
for a third-party box such as Gemini, Telegram or WhatsApp.

Two files per diagram, light and dark, referenced with `#only-light` and
`#only-dark`, because Material's colour scheme is a toggle on the page and an
SVG loaded through `<img>` cannot see it. Put the diagram after the opening
paragraphs, never directly under the title: the first line after the title is
the hook, which becomes the page description and its `llms.txt` entry.

SVG text does not wrap, so a label that is too long runs out over the edge of
its panel. `check()` measures every string against its box and fails the run
rather than emitting that, which is why some labels are terser than the prose
would be. Shorten the label; do not widen the box without looking at all of
them.

A diagram states the same facts as the prose around it, so it is subject to the
same rules. Ports, hostnames and auth modes must match the chapters, and the
`alt` text is where a reader on a screen reader gets them, so it carries the
same facts in a sentence rather than describing shapes.

## Keeping it useful to agents

Retrieval chunks a page by section, so a section that says "use the hostname
from chapter 2" is useless on its own. Restate the parameter (port, hostname,
auth mode, machine) inside the section that uses it, even though that repeats.

## Checks before committing

```bash
docker compose up -d --build      # builds and serves on 127.0.0.1:8088
```

The image build runs `mkdocs --strict`, so a broken internal link fails it. To
check without Docker:

```bash
pip install -r requirements.txt   # once
./scripts/build.sh
```

That local build draws no social cards. The plugin that makes them needs cairo
and pango installed on the machine, and a pin of pillow that has no wheel on the
newest Python, so it is off unless `SOCIAL_CARDS` is set. The Docker image and
the deploy workflow install `requirements-imaging.txt` and set it; a laptop
neither needs to nor should have to. The consequence is that a card only appears
on the deployed site, so check `og:image` there rather than locally.

The build sets `use_directory_urls: false`, so a page becomes `glossary.html`
rather than `glossary/index.html`. Every URL then maps onto a single file, which
keeps the site servable from an object store with no rewrite rule, and puts each
page beside its own `.md` source. A new top-level page also needs a `COPY` line
in the `Dockerfile`.

If you add or rename a chapter, update `nav:` in `mkdocs.yml`, the series
`README.md` table, and any cross-references. `--strict` will catch links that
no longer resolve, but it cannot catch a stale chapter number in prose.

A chapter's number is its position in its own series, so `03-*.md` is chapter 3
and its sections are `3.x`. Every series starts at 1. Refer to a chapter in
another series by its title or its series name, never as "chapter N", because
that number means something different in each series. `Start here` is a
prerequisite of every series, not chapter 1 of any of them.
