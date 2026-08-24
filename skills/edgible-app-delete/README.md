# edgible-app-delete (OpenClaw skill)

Delete an Edgible application by name (`edgible app delete`). Inverse of [edgible-app-create](../edgible-app-create/). Does **not** stop the nginx test container unless you do that yourself.

## Install

Same as create: copy this folder to `~/.openclaw/workspace/skills/` on the Gateway host. See [edgible-app-create README](../edgible-app-create/README.md).

## Helper (optional)

```bash
python3 -u ~/.openclaw/workspace/skills/edgible-app-delete/scripts/delete.py \
  --name skill-test
```

You want `STATUS=deleted` or `STATUS=missing`.

## Test

After **skill-test** exists:

```text
/skill edgible-app-delete Delete the Edgible app named skill-test.
```

Success is `STATUS=deleted`. `edgible app list` no longer shows **skill-test**. The Docker container `edgible-skill-test` may still be running — that is expected.
