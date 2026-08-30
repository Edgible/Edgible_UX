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
- `guides/<series>/README.md`: chapter list for that series.
- `guides/<series>/NN-*.md`: one chapter, one job, one smoke test.

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

- Reserve bold for the hook and for literal UI labels. Do not bold for emphasis,
  and never bold negations.
- Avoid em dashes. Use a comma, a full stop, or a colon.
- Use literal, searchable terms over metaphor: `auth mode`, `published
  hostname`, `serving agent`. Not doors, locks, or brains.
- `serving agent` is the daemon on the machine. `serving device` is the
  registered record in the console. They are not interchangeable.
- Auth modes are `org`, `api-key` and `None`, always in code font.
- Ports, hostnames, commands, filenames and env vars go in code font.
- Every claim needs a command whose output a reader can check.

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

If you add or rename a chapter, update `nav:` in `mkdocs.yml`, the series
`README.md` table, and any cross-references. `--strict` will catch links that
no longer resolve, but it cannot catch a stale chapter number in prose.
