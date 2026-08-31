# 3. OpenClaw changes the public Edgible site

**Ask for a change in chat, and the public page updates.**

## 3.0 Why

So far Edgible publishes a page and OpenClaw answers a question, separately. A chatbot in a browser tab can describe an edit and change nothing, so the check in this chapter is a page a stranger could load.

Inbox and calendar demos are the wrong choice twice over: they need your private mail to be interesting, and the page they end up on is a `None` hostname open to the world. Rewriting the public Hello World page is verifiable by anyone with the URL, and there is nothing on it to leak. Edgible stays the published hostname. The HTML is written by an agent on a box you own.

**Where you run this:** the chat in **Control UI on a phone on cellular**; the refresh in the **phone browser**; ground truth with `cat` on the **Ubuntu guest**.

## 3.1 The job

From Control UI on the phone, you tell OpenClaw to rewrite the Hello World site that already lives at `hello-world.<org>.edgible.com`. Edgible is still only the published hostname; it does not write the HTML. Optional: an hourly On this day brief (public sources only, since this URL is public). Cursor as a specialist is [7. Cursor Agent from OpenClaw on the Edgible site](07-cursor-agent.md); do this chapter first so that comparison has a Gemini page to beat.

**Done when**

- Phone Control UI says it wrote the page.
- Phone browser on `hello-world` (cellular) shows “OpenClaw was here”, not the original Hello World.
- `cat ~/hello-world/index.html` on the VM matches what you see.
- Optional: Hello World names someone born on this calendar day, with a short summary.
- Optional: a second run (next hour or Run now) shows a different person, not a repeat.
- Optional: Control UI / **Automations** lists an hourly job.
- Optional: no personal mail, files, or calendar in the page source (`cat ~/hello-world/index.html`).
- Port `18789` is still not forwarded.

**Need first:** [2. OpenClaw Control UI through Edgible](02-publish-openclaw-control-ui.md) on cellular. Leave the `hello-world` nginx container running ([Start here 1.9](../start-here/01-edgible-on-vm.md#19-hello-world)).

**Not this chapter:** inbox/calendar demos (personal data on a public URL), opening ports, or editing OpenClaw/Edgible config.

## 3.2 Rewrite Hello World from the phone

Leave the `hello-world` nginx container running. The HTML is on the host at `~/hello-world/index.html` (bind-mounted read-only into nginx; the container cannot write, OpenClaw on the host can).

On the phone (cellular, Control UI from [chapter 2](02-publish-openclaw-control-ui.md)), talk like a person. You do not need the path:

```text
Change the hello-world app to say "OpenClaw was here!"
```

That one line is enough on this setup (Gemini Flash + tools). Approve a write if asked.

**Smoke test.** Leave the Control UI, open `https://hello-world.<org>.edgible.com` (same host as [Start here](../start-here/01-edgible-on-vm.md), Wi‑Fi still off), and hard-refresh. You should see “OpenClaw was here”, not the original Hello World.

If it only *describes* the change, or the public page is unchanged, it guessed (docker exec into a read-only mount, wrong path, or no tool call). Then be explicit:

```text
Overwrite ~/hello-world/index.html on the host (nginx bind-mount). Do not docker exec.
Put a heading "OpenClaw was here" and the current UTC time. Use the write or exec tool.
```

On the VM, `cat ~/hello-world/index.html` is the ground truth. New file, old page → wait a second and hard-refresh again.

Do not ask it to open ports, install packages, or edit OpenClaw/Edgible config.

### Verify

- [ ] Phone Control UI says it wrote the page.
- [ ] Phone browser on `hello-world` (cellular) shows “OpenClaw was here”, not the original Hello World.
- [ ] `cat ~/hello-world/index.html` on the VM matches what you see.
- [ ] Port `18789` is still not forwarded.

---

## 3.3 A repeating public brief (no personal data)

**Outcome:** Hello World becomes an On this day page: one important person born on this calendar day, rotating every hour so a day shows 24 different people. Public sources only.

Inbox and calendar demos need your mail, and this Hello World URL is public. Use the open web instead. This is the same research on a schedule, published somewhere you will see it.

On the phone, in Control UI, talk like a person:

```text
Turn the hello-world app into an On this day page.
Pick one important historical figure born on this date (any year).
Use three headings: Who they were. Why they still matter. A quirky detail.
Public sources only (Wikipedia is fine). Nothing about me. Simple HTML.
```

Hard-refresh `https://hello-world.<org>.edgible.com`. You want a name, dates, a few paragraphs, not “OpenClaw was here.”

If it guesses from memory with no fetch, say: use Wikipedia’s “On this day” births for today’s month and day, then rewrite hello-world.

Then make it rotate every hour (24 people per calendar day):

```text
Every hour, update hello-world with a different person born on this calendar date.
Do not repeat someone already shown today. Aim for 24 distinct people in 24 hours.
After local midnight, start the next date's births.
Keep a short list of who you've already shown (a file next to the HTML is fine).
Use a cron/automation job. Confirm the schedule. Public sources only. Nothing about me.
```

Wait for the next hour (or **Run now** in **Automations**), hard-refresh Hello World. A different name should be on the page. Gemini free tier has daily caps. If 429s start, pause the job or pin Flash ([chapter 1](01-openclaw-on-the-box.md) 1.3.3), or switch the chat model in [8. Models beyond free Gemini](08-models-beyond-free-gemini.md). For a long-running box, switch this cron to daily after the demo.

Gemini is enough to research and write HTML in one pass. Optional [chapter 7](07-cursor-agent.md) is the comparison: wipe back to the [Start here](../start-here/01-edgible-on-vm.md) Hello World page, remove that cron, then hire Cursor to rebuild the same product on the same public URL. Do not skip this chapter; chapter 7 is compared against the page Gemini produced here.

### Verify

- [ ] Optional: Hello World names someone born on this calendar day, with a short summary.
- [ ] Optional: a second run (next hour or Run now) shows a different person, not a repeat.
- [ ] Optional: Control UI / **Automations** lists an hourly job.
- [ ] Optional: no personal mail, files, or calendar in the page source (`cat ~/hello-world/index.html`).
- [ ] Port `18789` is still not forwarded.

---

## Next

[4. OpenClaw skill for the Edgible CLI](04-edgible-openclaw-skill.md). Optional later: [7. Cursor Agent from OpenClaw on the Edgible site](07-cursor-agent.md), [8. Models beyond free Gemini](08-models-beyond-free-gemini.md). Series: [README](README.md).
