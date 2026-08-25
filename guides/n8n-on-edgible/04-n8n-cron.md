# 4. A cron workflow

**n8n can work with no inbound URL. Prove that before webhooks.**

A schedule never needs a public URL. You edit it on the **org** hostname; n8n fires on the box. That is the other half of per-app auth: not every workflow is a door. The second app is only for inbound calls. Cron would work even if you never created **n8n-hooks**.

## 4.1 The job

You add a **Schedule** workflow that writes one **Executions** row. Nothing on the internet calls you. If this fails, the problem is n8n, not Edgible hooks.

**Done when**

- The workflow is **Active**.
- After the next tick (or **Execute workflow** once), **Executions** shows a success.
- You then set the schedule to something sane (or deactivate) so it does not fire every minute forever.

**Need first:** [2. n8n editor through Edgible](02-n8n-editor-through-edgible.md) (canvas on the phone or host browser). [Chapter 3](03-n8n-webhook-door.md) can wait, but you will want it before [5](05-n8n-public-webhook.md).

**Not this chapter:** Webhook nodes, GitHub, Telegram, OpenClaw.

## 4.2 Build it

In the n8n editor (org URL):

1. **Add workflow**.
2. Delete the start stub if n8n added a manual trigger you do not want. Add **Schedule Trigger** (or **Schedule**).
3. Interval: **every 1 minute** for the smoke test (you will change this).
4. Add **Edit Fields** / **Set**. One field, e.g. `at` = `{{ $now }}` (or n8n’s current “current date” expression).
5. **Save**. **Active** (toggle on).

Wait up to a minute, or click **Execute workflow** once to force a run.

Open **Executions**. You want a green row, not a red error.

Then edit the trigger: every **hour**, or **deactivate**, so a trial VM is not ticking all day.

### Verify

- [ ] Executions has at least one success for this workflow.
- [ ] The schedule is no longer every minute (or the workflow is inactive).
- [ ] You did not open a port or change Edgible auth.

---

## Next

[5. A webhook a stranger can hit](05-n8n-public-webhook.md). Series: [README](README.md).
