# edgible-app-list (OpenClaw skill)

List Edgible apps. **Default: the serving device OpenClaw is sitting on**, not every box in the org. `--all` lists the organisation.

That default matches this walk: the same org has `macbookairubuntu2404vm` (this VM) and `awsubuntu24`. Chat with the VM should not imply AWS apps unless you ask.

## Install

Copy onto the Gateway with the other skills:

```bash
cp -R /path/to/Edgible_UX/skills/edgible-app-list ~/.openclaw/workspace/skills/
openclaw skills list
openclaw gateway restart
```

## Helper

This box:

```bash
python3 -u ~/.openclaw/workspace/skills/edgible-app-list/scripts/list.py \
  --device-name macbookairubuntu2404vm
```

Whole org:

```bash
python3 -u ~/.openclaw/workspace/skills/edgible-app-list/scripts/list.py --all
```

You want `SCOPE=device` (or `org`), `COUNT=`, then `NAME=… URL=…` lines, then `STATUS=ok` or `STATUS=empty`.

## Test (Control UI)

```text
/skill edgible-app-list List Edgible apps on this machine, device macbookairubuntu2404vm.
```

Success is those `NAME=` / `URL=` lines in the bubble (or in activity if the model skips the follow-up). Compare with `edgible app list`.
