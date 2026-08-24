# 4. Public page from the agent

**Outcome:** The agent on the mini-PC rewrites the **Hello World** site you already published. You watch it from the phone. Optional hourly **On this day** (public sources only).

Prerequisites: [chapter 3](03-publish-control-ui.md) — Control UI on cellular.

This is the “wow”: ChatGPT in a tab cannot change a website on your box. Cursor as a specialist is [chapter 8](08-cursor-agent.md).

Series index: [README](README.md).

---

## 11. Show OpenClaw actually doing something (from the phone)

**Outcome:** Your public Hello World site changed because the agent on the mini-PC rewrote it — you watched it from the phone.

`hello` only showed the model. A file on disk is proof of tools. The **wow** is Edgible-shaped: you already have a public page at `hello-world.<org>.edgible.com`. OpenClaw lives on the same box. From the Control UI, tell it to replace that page. Refresh the Hello World URL. ChatGPT in a tab cannot change a website on your mini-PC.

Leave the **hello-world** nginx container running ([chapter 1](01-invite-through-edgible-on-vm.md)). The HTML is on the **host** at `~/hello-world/index.html` (bind-mounted read-only into nginx — the container cannot write; the agent on the host can).

On the **phone** (cellular, Control UI from [chapter 3](03-publish-control-ui.md)), talk like a person — you do not need the path:

```text
Change the hello-world app to say "OpenClaw was here!"
```

That one line is enough on this setup (Gemini Flash + tools). Approve a write if asked.

Then **leave the Control UI**, open `https://hello-world.YOUR-ORG.edgible.com` (same host as [chapter 1](01-invite-through-edgible-on-vm.md), Wi‑Fi still off), and **hard-refresh**. You should see **OpenClaw was here** — not the original Hello World.

If it only *describes* the change, or the public page is unchanged, it guessed (docker exec into a read-only mount, wrong path, or no tool call). Then be explicit:

```text
Overwrite ~/hello-world/index.html on the host (nginx bind-mount). Do not docker exec.
Put a heading "OpenClaw was here" and the current UTC time. Use the write or exec tool.
```

On the VM, `cat ~/hello-world/index.html` is the ground truth. New file, old page → wait a second and hard-refresh again.

Do **not** ask it to open ports, install packages, or edit OpenClaw/Edgible config.

### Verify

- [ ] Phone Control UI says it wrote the page.
- [ ] Phone browser on **hello-world** (cellular) shows **OpenClaw was here**, not the original Hello World.
- [ ] `cat ~/hello-world/index.html` on the VM matches what you see.
- [ ] Port **18789** is still not forwarded.

---

## 12. A repeating public brief (no personal data)

**Outcome:** Hello World becomes an **On this day** page: one important person **born on this calendar day**, rotating **every hour** so a day shows **24 different people**. Public sources only.

Inbox and calendar demos are the wrong story here: they need your mail, and this Hello World URL is **public**. Use the open web. The job OpenClaw is good at: **the same research, on a schedule, reported somewhere you will actually look.**

On the **phone**, Control UI — talk like a person:

```text
Turn the hello-world app into an On this day page.
Pick one important historical figure born on this date (any year).
Use three headings: Who they were. Why they still matter. A quirky detail.
Public sources only (Wikipedia is fine). Nothing about me. Simple HTML.
```

Hard-refresh `https://hello-world.YOUR-ORG.edgible.com`. You want a name, dates, a few paragraphs — not “OpenClaw was here.”

If it guesses from memory with no fetch, say: use Wikipedia’s “On this day” **births** for today’s month and day, then rewrite hello-world.

Then make it **rotate every hour** (24 people per calendar day):

```text
Every hour, update hello-world with a different person born on this calendar date.
Do not repeat someone already shown today. Aim for 24 distinct people in 24 hours.
After local midnight, start the next date's births.
Keep a short list of who you've already shown (a file next to the HTML is fine).
Use a cron/automation job. Confirm the schedule. Public sources only. Nothing about me.
```

Wait for the next hour (or **Run now** in Automations), hard-refresh Hello World. A **different** name should be on the page. Gemini free tier has daily caps — if 429s start, pause the job or pin Flash ([chapter 2](02-openclaw-on-the-box.md) §9c). For a long-running box, switch this cron to daily after the demo.

Gemini is enough to *research and dump HTML*. Optional [chapter 8](08-cursor-agent.md) is the A/B: wipe back to the [chapter 1](01-invite-through-edgible-on-vm.md) Hello World page, remove that cron, then hire Cursor to rebuild the **same** product. Same public URL. Do not skip this chapter — you need to have seen Gemini’s version so Cursor’s looks like an upgrade.

### Verify

- [ ] Hello World names someone **born on this calendar day**, with a short summary.
- [ ] A second run (next hour or Run now) shows a **different** person, not a repeat.
- [ ] Control UI / Automations lists an **hourly** job.
- [ ] No personal mail, files, or calendar in the page source (`cat ~/hello-world/index.html`).
- [ ] Port **18789** is still not forwarded.

---
