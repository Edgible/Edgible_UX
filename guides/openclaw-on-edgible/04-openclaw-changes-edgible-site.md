# 4. OpenClaw changes the public Edgible site

**Ask for a change, and a second later the whole internet sees it.**

## 4.0 Why

So far the two halves of this series have only proved themselves separately: Edgible publishes a page, OpenClaw answers a question. Neither has touched the other. A chatbot in a browser tab can describe an edit beautifully and change nothing, and you would have no way to tell the difference — which is exactly why the proof here has to be something a stranger could load.

The demo everyone reaches for first is the inbox or the calendar, and it is the wrong one twice over: it needs your private mail to be interesting, and the page it would end up on is a **None** hostname open to the world. Rewriting the public Hello World page instead is verifiable by anyone with the URL, and there is nothing on it to leak. Edgible’s role stays deliberately small — it is still only the door; the HTML is written by an agent on a box you own, which is the part no hosted chatbot can do.

**Where you run this:** the chat in **Control UI on a phone on cellular**; the refresh in the **phone browser**; ground truth with `cat` on the **Ubuntu guest**.

## 4.1 The job

From Control UI on the phone, you tell **OpenClaw** to rewrite the Hello World site that already lives at `hello-world.<org>.edgible.com`. Edgible is still only the public door — it does not write the HTML. Optional: an hourly **On this day** brief (public sources only — this URL is public). Cursor as a specialist is [8. Cursor Agent from OpenClaw on the Edgible site](08-cursor-agent.md); do this chapter first so that A/B has a Gemini dump to beat.

**Done when**

- Phone Control UI says it wrote the page.
- Phone browser on **hello-world** (cellular) shows **OpenClaw was here**, not the original Hello World.
- `cat ~/hello-world/index.html` on the VM matches what you see.
- Optional: Hello World names someone **born on this calendar day**, with a short summary.
- Optional: a second run (next hour or Run now) shows a **different** person, not a repeat.
- Optional: Control UI / Automations lists an **hourly** job.
- Optional: no personal mail, files, or calendar in the page source (`cat ~/hello-world/index.html`).
- Port **18789** is still not forwarded.

**Need first:** [3. OpenClaw Control UI through Edgible](03-publish-openclaw-control-ui.md) on cellular. Leave the **hello-world** nginx container running ([1.9](01-edgible-on-vm.md)).

**Not this chapter:** inbox/calendar demos (personal data on a public URL), opening ports, or editing OpenClaw/Edgible config.

## 4.2 Rewrite Hello World from the phone

Leave the **hello-world** nginx container running. The HTML is on the **host** at `~/hello-world/index.html` (bind-mounted read-only into nginx — the container cannot write; OpenClaw on the host can).

On the **phone** (cellular, Control UI from [chapter 3](03-publish-openclaw-control-ui.md)), talk like a person — you do not need the path:

```text
Change the hello-world app to say "OpenClaw was here!"
```

That one line is enough on this setup (Gemini Flash + tools). Approve a write if asked.

**Smoke test.** Now **leave the Control UI**, open `https://hello-world.YOUR-ORG.edgible.com` (same host as [chapter 1](01-edgible-on-vm.md), Wi‑Fi still off), and **hard-refresh**. You should see **OpenClaw was here** — not the original Hello World.

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

## 4.3 A repeating public brief (no personal data)

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

Wait for the next hour (or **Run now** in Automations), hard-refresh Hello World. A **different** name should be on the page. Gemini free tier has daily caps — if 429s start, pause the job or pin Flash ([chapter 2](02-openclaw-on-the-box.md) 2.3.3), or switch the chat brain in [9. Models beyond free Gemini](09-models-beyond-free-gemini.md). For a long-running box, switch this cron to daily after the demo.

Gemini is enough to *research and dump HTML*. Optional [chapter 8](08-cursor-agent.md) is the A/B: wipe back to the [chapter 1](01-edgible-on-vm.md) Hello World page, remove that cron, then hire Cursor to rebuild the **same** product. Same public URL. Do not skip this chapter — you need to have seen Gemini’s version so Cursor’s looks like an upgrade.

### Verify

- [ ] Optional: Hello World names someone **born on this calendar day**, with a short summary.
- [ ] Optional: a second run (next hour or Run now) shows a **different** person, not a repeat.
- [ ] Optional: Control UI / Automations lists an **hourly** job.
- [ ] Optional: no personal mail, files, or calendar in the page source (`cat ~/hello-world/index.html`).
- [ ] Port **18789** is still not forwarded.

---

## Next

[5. OpenClaw skill for the Edgible CLI](05-edgible-openclaw-skill.md). Optional later: [8. Cursor Agent from OpenClaw on the Edgible site](08-cursor-agent.md), [9. Models beyond free Gemini](09-models-beyond-free-gemini.md). Series: [README](README.md).
