# 4. A cron workflow

**Your first working automation, and nobody on the internet can trigger it.**

## 4.0 Why

Before you open a public door in the next chapter, it is worth proving that n8n itself runs — and the cleanest way to do that is a workflow nothing outside can reach. A schedule needs no inbound URL at all: you edit it over the **org** hostname, and n8n fires it on the box on its own clock. If this run fails, you know the problem is n8n or your workflow, not an Edgible hostname or a lock.

That is the quieter half of per-app auth: not every workflow is a door. The **n8n-hooks** app exists only for calls that arrive from outside, and this chapter would work exactly the same if you had never created it. Reaching for a public hostname or a forwarded port to make a timer fire is effort spent widening your attack surface for nothing.

**Where you run this:** the **n8n editor in a browser** on the **org** hostname — phone or host browser, either is fine. No shell, no Edgible console.

## 4.1 The job

You add a **Schedule** workflow that writes one **Executions** row. Nothing on the internet calls you. If this fails, the problem is n8n, not Edgible hooks.

**Done when**

- The workflow is **Active**.
- After the next tick (or **Execute workflow** once), **Executions** shows at least one success.
- You then set the schedule to something sane (or deactivated the workflow) so it does not fire every minute forever.
- You did not open a port or change Edgible auth.

**Need first:** [2. n8n editor through Edgible](02-n8n-editor-through-edgible.md) (canvas on the phone or host browser). [Chapter 3](03-n8n-webhook-door.md) can wait, but you will want it before [5](05-n8n-public-webhook.md).

**Not this chapter:** Webhook nodes, GitHub, Telegram, OpenClaw.

## 4.2 Build it

In the n8n editor (org URL):

1. **Add workflow**.
2. Delete the start stub if n8n added a manual trigger you do not want. Add **Schedule Trigger** (or **Schedule**).
3. Interval: **every 1 minute** for the smoke test (you will change this).
4. Add **Edit Fields** / **Set**. One field, e.g. `at` = `{{ $now }}` (or n8n’s current “current date” expression).
5. **Save**. **Active** (toggle on).

**Smoke test.** Wait up to a minute, or click **Execute workflow** once to force a run.

Open **Executions**. You want a green row, not a red error.

Then edit the trigger: every **hour**, or **deactivate**, so a trial VM is not ticking all day.

### Verify

- [ ] The workflow is **Active**.
- [ ] After the next tick (or **Execute workflow** once), **Executions** shows at least one success.
- [ ] You then set the schedule to something sane (or deactivated the workflow) so it does not fire every minute forever.
- [ ] You did not open a port or change Edgible auth.

---

## Next

[5. A webhook a stranger can hit](05-n8n-public-webhook.md). Series: [README](README.md).
