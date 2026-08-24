# OpenClaw on Edgible — Getting started

**OpenClaw is the agent on a box you own. Edgible is the door: a real `https://` URL with authenticated login you can access anywhere — no port-forward, no hole in the router, no Tailscale.**

By the end of this chapter you have an OpenClaw Control UI on a real **`https://openclaw-ui.your-org.edgible.com`** URL (pattern: `<app>.<org>.edgible.com`). You open it from a **phone on cellular** or a **remote browser**, chat with the agent that lives on the mini-PC, and you did **not** port-forward 22, 80, 443, or 18789, and you did **not** install Tailscale. The Gateway stays on **loopback** at home. Edgible is the public door: HTTPS hostname, certificate, and **org login** so a stranger with the URL should not see the dashboard.

**Why Edgible (not Tailscale Serve, not a hole in the router):**

- **Outbound 443 only.** The box dials out; nothing inbound on the home router.
- **A URL you can bookmark.** Same shape as a normal website, not a tailnet IP or a Serve hostname that only signed-in Tailscale clients can use.
- **Org login in front.** You decide who in the organisation can hit the hostname. Tailscale Serve instead trusts whoever is on your tailnet and speaks identity headers OpenClaw already understands — fewer OpenClaw prompts, but every client must run Tailscale.
- **OpenClaw still has its own locks.** First time on a browser you paste the gateway token and approve the device. That is OpenClaw, not Edgible. Later visits on that browser are just the URL and, when the session expired, Edgible login.

The “mini-PC” in this chapter is an **Ubuntu 24.04 LTS** virtual machine on the computer in front of you: **VirtualBox** (Windows or Linux PC) or **UTM** (Mac). You go Hello World on the phone → a **model** → OpenClaw **locally** → Control UI through Edgible → **the public Hello World page rewritten from the phone** → **an hourly “born on this day” page on that same URL** (Gemini) → (optional) **reset to Hello World** and **Cursor rebuilds that same product** → (optional) **WhatsApp**, where `/acp spawn --bind here` lets you tweak the page in ordinary chat. Teardown is a later chapter.

---

## What you should have at the end of this chapter

- An Edgible account from the invite.
- An Ubuntu 24.04 VM that can reach the internet **outbound** on HTTPS (no port forwarding).
- The `edgible` CLI on that VM, logged in as you.
- A serving device registered in your org (we will call it `mini-pc`).
- `edgible device health --name mini-pc` reporting **Health check OK**.
- A public **Hello World** page on a `hello-world.your-org.edgible.com` URL that loads on your **phone** (cellular, not the VM’s Wi‑Fi).
- A **model** for OpenClaw: a Gemini API key (default), or local Ollama if the box is big enough.
- OpenClaw Gateway on the VM, with a **local** `hello` reply in the terminal.
- The OpenClaw Control UI on an `openclaw-ui.your-org.edgible.com` URL, **org auth**, reachable from a **phone** on cellular.
- The public **hello-world** page rewritten from that phone — refresh `hello-world.<org>.edgible.com` and see OpenClaw’s HTML.
- A **born on this day** page on that same public URL (one notable person, Wikipedia-scale public sources) that **rotates every hour** — 24 people in a day.
- (Optional, step 13) Reset **hello-world** to the original Hello World page, drop the Gemini rotation cron, then Cursor implements On this day + rotation infra from that clean slate. Same URL; the contrast is the demo.
- (Optional, step 14) WhatsApp linked as a Gateway device; a `hello` reply that starts with `[OpenClaw]`; then `/acp spawn cursor --bind here` and a normal message that retitles On this day sections — no `/acp steer`.

You do **not** yet have teardown (hello-world, OpenClaw, agent, VM).

---

## What you need on the host computer


| Item                     | Notes                                                                                                                                                                                                                                   |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Invite email             | Link into the Edgible **console**. If you need it again, the login/console is [https://app.prod.edgible.com/](https://app.prod.edgible.com/). Use the **host** browser, not the VM. A **temporary password** arrives in a second email. |
| VM manager               | Software that runs a virtual machine on your PC or Mac. This guide uses **VirtualBox** or **UTM** — see step 2.                                                                                                                         |
| Ubuntu **24.04 LTS** ISO | Downloaded in step 2. Match the CPU: **amd64** on typical PCs; **arm64** on Apple Silicon.                                                                                                                                              |
| Sudo on the guest        | You will install a systemd agent that configures WireGuard, iptables, and Caddy.                                                                                                                                                        |
| A model for OpenClaw     | Default: a free **Gemini** API key (Google account). Or local **Ollama** if the VM/mini-PC has enough RAM. ChatGPT Free on chatgpt.com is not a key. See step 8.                                                                        |
| Cursor (optional)        | Paid **Cursor** plan if you will do steps 13–14. The IDE on the host is not enough — you log the **CLI** in on the VM. Skip 13–14 if you have no plan.                                                                                  |


NAT networking is enough. The VM only needs **outbound TCP 443**. Do not port-forward 22, 80, 443, or 18789 on the host. That is the point of Edgible.

---

## 1. Create account

**Outcome:** An Edgible account and organisation you can sign into at the console.

Do this on your **laptop/desktop browser** (the host), not inside the VM. The Edgible **login and console** live at [https://app.prod.edgible.com/](https://app.prod.edgible.com/) — not the marketing site. You pick a permanent password here; that is what you will type later on the VM for `edgible auth login`.

1. Open the invitation email and follow the signup link. If there is no link, open [https://app.prod.edgible.com/](https://app.prod.edgible.com/) and choose **Create your account** / sign up.
2. On **Create your account**, enter first name, last name, and email (use the address the invite was sent to unless the invite says otherwise). Submit. Edgible does **not** ask for a password yet — it emails you a temporary one.
3. Check that inbox (and spam) for the **temporary password** email. Stay on the **Check your email** page in the browser; it is waiting for that password.
4. Paste the temporary password from the email and continue.
5. You **must change your password** before continuing. Enter a new password (at least 8 characters), confirm it, and save. From this point on, the temporary password is dead — use only the new one.
6. You are then asked to **create an organisation**. Do that now. A default name such as *Your name's organization* is fine for this trial.
  An **organisation** is the workspace that owns your serving devices, applications, and public hostnames. Your **account** is you (email and password). The organisation is the *place* those machines and apps live — so a device registered later is not floating on a personal login, and you could later add another person or another box to the same org. Early trials are one person, one org: create it and keep going.
7. You should land on the **Dashboard** at [https://app.prod.edgible.com/](https://app.prod.edgible.com/). An empty device list is fine.

Keep the **email** and the **new password** somewhere you can paste into the VM. To return later, always use [https://app.prod.edgible.com/](https://app.prod.edgible.com/).

### Verify

- [ ] You can sign in at [https://app.prod.edgible.com/](https://app.prod.edgible.com/) and see the Dashboard.
- [ ] You have created an **organisation**.
- [ ] You know the account **email** and the **new** password (not the temporary one).

---

## 2. Create Virtual Machine

**Outcome:** An Ubuntu 24 virtual machine in a VM manager — a stand-in for the mini-PC.

A **virtual machine (VM)** is a full computer that runs as an app on the laptop or PC in front of you. It stands in for the mini-PC on the shelf: Ubuntu 24 inside, Edgible (and later OpenClaw) on that guest, not on your host OS.

To create one you need a **VM manager** (hypervisor) — the app that hosts the VM. Install that first, then create a virtual machine **based on Ubuntu 24.04 LTS** that runs inside it.


| Your computer       | VM manager                                |
| ------------------- | ----------------------------------------- |
| Windows or Linux PC | [VirtualBox](https://www.virtualbox.org/) |
| Mac                 | [UTM](https://mac.getutm.app/)            |


Use **Ubuntu Server** (not Desktop). You will work in a terminal, like a mini-PC.

**Recommended minimums** for this guide (sized so the same guest can run OpenClaw later, not only the Edgible agent):


| Resource | Recommended minimum | Floor if you are short on host RAM/disk                                                                      |
| -------- | ------------------- | ------------------------------------------------------------------------------------------------------------ |
| Memory   | **4 GB**            | **2 GB** can boot Ubuntu and the Edgible agent; OpenClaw will struggle.                                      |
| Disk     | **40 GB**           | **20 GB** is enough for this chapter only; images and OpenClaw need the rest. Dynamically allocated is fine. |
| CPUs     | **2**               | **1** works; two is the minimum we recommend.                                                                |


Download the ISO from [Ubuntu Server](https://ubuntu.com/download/server): **amd64** for typical VirtualBox on Intel/AMD PCs, **arm64** for UTM **Virtualize** on Apple Silicon.

During the Ubuntu installer:

- Enable the **OpenSSH server**.
- Create a user you will remember (for example `ubuntu`). Give it sudo.
- Skip extra snaps except what the installer requires.

### 2a. VirtualBox (Windows or Linux PC)

1. Install [VirtualBox](https://www.virtualbox.org/) if needed.
2. **New** VM: type Linux, version **Ubuntu (64-bit)**.
3. Set memory, CPUs, and disk to the recommended minimums above (VDI, dynamically allocated is fine).
4. Attach the **amd64** Ubuntu 24.04 Server ISO to the optical drive.
5. Network: **NAT** (default). That is enough for outbound HTTPS.
6. Start the VM and complete the Ubuntu installer. Reboot when asked; remove the ISO if the VM tries to install again.
7. Log in at the VM console with the user you created.

Optional but useful: **Devices → Shared Clipboard → Bidirectional** after Guest Additions, so you can paste the Edgible password. Until then, type it.

### 2b. UTM (Mac)

1. Install [UTM](https://mac.getutm.app/) if needed.
2. **Create a New Virtual Machine** → **Virtualize** (Apple Silicon) or **Virtualize** on Intel Mac with an amd64 ISO. Do **not** use **Emulate** unless you have no other choice (it is slow).
3. Operating System: **Linux**. Boot ISO: Ubuntu 24.04 Server **arm64** on Apple Silicon, **amd64** on Intel.
4. Set memory, CPU cores, and disk to the recommended minimums above.
5. Network: **Shared Network** (NAT). That is enough.
6. Start, complete the Ubuntu installer, reboot, log in at the console.

### Verify

- [ ] You can log into Ubuntu 24.04 in the VM console.
- [ ] `lsb_release -a` shows **24.04**.
- [ ] `sudo -n true` works, or `sudo -v` accepts your password.

---

## 3. Prepare Virtual Machine

**Outcome:** An updated VM with outbound internet and Docker installed.

This step is ordinary Linux housekeeping on the guest: updates, outbound internet, and **Docker** (OpenClaw will need it; Edgible can publish a compose app later). Work **inside the VM** (console is enough).

**SSH from the host (optional).** NAT does not give you a stable guest IP on the LAN. You can stay in the VM window, or in VirtualBox add **Settings → Network → Advanced → Port forwarding** for **host 2222 → guest 22** only, then:

```bash
ssh -p 2222 ubuntu@127.0.0.1
```

Use your VM username if it is not `ubuntu`. Do **not** forward 80, 443, or 18789.

### 3a. Update Ubuntu

```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y ca-certificates curl
```

If the upgrade installed a new kernel, reboot the VM (`sudo reboot`), then log in again.

### 3b. Confirm outbound internet

The VM only needs **outbound** HTTPS. A generic check is enough:

```bash
curl -fsSI https://www.google.com | head -n 5
```

You want a successful TLS response (for example HTTP **200** or **301**), not “Could not resolve host” or a hang. If this fails, fix NAT/shared network in the VM manager before installing anything else.

### 3c. Install Docker

Follow Docker’s current Ubuntu steps if these drift: [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/).

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "${VERSION_CODENAME}") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker "$USER"
```

Log out and back in (or run `newgrp docker`) so the `docker` group applies.

```bash
docker version
docker run --rm hello-world
```

If you see permission denied on `/var/run/docker.sock`, the group is not active yet — `newgrp docker` or a new login, or use `sudo docker` until then.

### Verify

- [ ] `sudo apt-get upgrade` completed (reboot if a new kernel was installed).
- [ ] `curl -fsSI https://www.google.com` succeeds.
- [ ] `docker version` and `docker run --rm hello-world` succeed.
- [ ] You have a durable way to type commands on the VM (console or SSH).

---

## 4. Install the Edgible CLI (on the VM)

**Outcome:** The `edgible` command on the VM.

Still **inside the guest**:

```bash
curl -fsSL https://get.edgible.com/install.sh | bash
```

The CLI needs **Node.js 20+**. The installer offers to install it if it is missing. Accept that.

Reload your PATH if `edgible` is not found (new shell, or `source ~/.bashrc`).

```bash
edgible --version
edgible --help
```

### Verify

- [ ] `edgible --version` prints a version.
- [ ] You did **not** install the CLI on the Mac/PC host for this guide. The serving device is the VM.

---

## 5. Log the CLI into your Edgible account

**Outcome:** The CLI on the VM logged into your organisation.

Use the email and **new** password from **step 1** (not the temporary password from the email). On the VM:

```bash
edgible auth login \
  --user-email you@example.com \
  --user-password 'your-password'
```

Or run `edgible auth login` and follow the prompts.

This writes tokens and the active organization id under your **guest** home directory.

```bash
edgible config list
```

Note the **organization** id. You will need it when you author YAML in a later chapter.

If you belong to more than one org:

```bash
edgible auth select-org
```

### Verify

- [ ] Login completes without error.
- [ ] `edgible config list` shows an organization id.
- [ ] Dashboard still shows your account (refresh). Devices may still be empty.

---

## 6. Install and start the serving agent

**Outcome:** A serving device (`mini-pc`) connected to Edgible, with no inbound ports opened on your router.

The agent must run **on the VM** as systemd. It registers a device named `mini-pc` in your org.

```bash
sudo edgible agent install \
  --type systemd \
  --device-type serving \
  --device-name mini-pc \
  --non-interactive
```

Expect **30–60 seconds**. Then:

```bash
sudo edgible agent start
sudo systemctl status edgible-agent --no-pager
```

The agent connects **outbound** to the control plane (WebSocket over HTTPS). It does not open a port on your router.

Wait a few seconds, then:

```bash
edgible device health --name mini-pc
```

Expect **Health check OK** within about 15 seconds.

If it hangs or fails:

```bash
sudo journalctl -u edgible-agent -n 80 --no-pager
sudo edgible agent status
```

Common causes: login was skipped, no outbound 443, or the device name already exists in the org from a previous attempt (`--device-name` must be unique).

### Verify

- [ ] `systemctl status edgible-agent` shows **active (running)**.
- [ ] `edgible device health --name mini-pc` prints **Health check OK**.
- [ ] Dashboard lists a serving device named **mini-pc**.

---

## 7. Edgible says "Hello World"

**Outcome:** An application hosted on your laptop / mini-PC that is accessible from the internet.

The agent being healthy is not the same as “the internet can reach a process on this VM.” This step is Edgible saying **Hello World**: a throwaway nginx page you open from a **phone**, before you touch OpenClaw.

Choose **None** (public access) when asked how the application should be protected. That is acceptable **only** because this page is a public Hello World. Do not use None for OpenClaw or anything private.

### 7a. Run nginx on the VM

Still on the guest:

```bash
mkdir -p ~/hello-world
cat > ~/hello-world/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Hello World</title></head>
<body>
  <h1>Hello World</h1>
  <p>Served from your Ubuntu VM through Edgible.</p>
</body>
</html>
EOF

docker run -d --name hello-world \
  -p 8081:80 \
  -v ~/hello-world:/usr/share/nginx/html:ro \
  nginx:alpine

curl -s http://127.0.0.1:8081/
```

You should see the Hello World HTML. That is **local only** — your phone cannot reach `8081` on the VM, and you did not port-forward it.

### 7b. Publish it with Edgible

The nginx container is already listening on **8081**. Create an **existing** app — Edgible will discover that port. No YAML file.

```bash
edgible app create existing
```

(`app` is short for `application`.) Answer the prompts like this:

| Prompt | Answer |
|--------|--------|
| Application name | `hello-world` |
| Upgrade protocol from HTTP to HTTPS? | **Yes** (if asked) |
| Custom domains / additional hostnames | leave **blank** (Enter) |
| How should access to this application be protected? | **None** (public access) |
| Use Edgible managed gateway? | **Yes** (if asked — say Yes so you are not asked for a gateway ID) |
| Select serving device | **mini-pc** |
| Select local workload | **hello-world** (the nginx container) |
| Select port | **8081** |

When it succeeds, the CLI prints an application **URL**. Standard shape is `https://<app>.<org>.edgible.com` — for this app, something like `https://hello-world.your-org.edgible.com`. Always copy the exact host the CLI prints. Do **not** open that HTTPS URL yet — the certificate is still being issued.

### 7c. Wait for the certificate (console)

First publish typically takes **30–90 seconds**. Use the console to watch it, rather than hammering the URL.

1. On the **host** browser, open [https://app.prod.edgible.com/](https://app.prod.edgible.com/).
2. Open the **hello-world** application you just created.
3. Find the **Certificates** section. It will move from pending / issuing to **issued** (or equivalent ready state) when TLS is in place.
4. When the certificate looks ready, copy the HTTPS URL from the console (or from `edgible app list` / `edgible app status` on the VM).

Then, from the VM:

```bash
edgible app list
edgible app status
curl -sS https://<the-hostname>/
```

You should see Hello World over **HTTPS**. If curl complains about the certificate, wait and refresh **Certificates** in the console; do not fall back to `http://`.

### 7d. Hit it from your phone

This is the real check: the page must load when you are **not** on the same LAN as the laptop.

1. On the phone, turn **Wi‑Fi off** (use cellular).
2. Open a browser to the **URL** from `edgible app list`.
3. You should see the same **Hello World** as `curl` on the VM.

If it fails at first, wait a minute, re-run `edgible app status`, and retry. You are not opening a port on the router; the VM is still NAT-only.

Leave this app running until the teardown chapter (or `edgible app delete --name hello-world` when you are done with it).

### Verify

- [ ] `curl http://127.0.0.1:8081/` shows Hello World on the VM.
- [ ] `edgible app list` shows **hello-world** with a `hello-world.<org>.edgible.com` URL.
- [ ] In the console, **hello-world** → **Certificates** shows the cert as issued / ready.
- [ ] `curl` to the **https** URL shows Hello World on the VM.
- [ ] The same page loads on a phone on **cellular**.

---

## 8. OpenClaw prerequisites (a model)

**Outcome:** A model OpenClaw can call — a Gemini API key (default), local Ollama if the box is big enough, or a private model URL from someone you trust.

OpenClaw onboarding will not finish until a **real completion** succeeds. **ChatGPT Free** (chatgpt.com) is not that: it is a website, not an API key. Same Google/OpenAI *login* can open a developer console; usage is a separate product.

Leave **hello-world** running. Pick **one** of the options below. You will paste the key (or point at Ollama) in the next step, when OpenClaw is installed.

### 8a. Google Gemini (default, free)

Do this on the **host** browser, not inside the VM. You need a Google account (Gmail is fine).

1. Open [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey) and sign in.
2. If Google shows terms for AI Studio / the Gemini API, accept them.
3. Click **Create API key**.
4. Choose **Create API key in a new project** unless you already know which Google Cloud project to use.
5. Copy the key (it usually starts with `AIza`). Store it like a password — you will type it on the VM in the next step. Do not commit it, paste it into a chat, or put it in Hello World.

The free tier is enough to prove `hello`. It is rate-limited. Outside the EU, Google may use free-tier traffic to improve products; that is Google’s policy, not Edgible’s.

Optional check from the **VM** (proves the key *and* that the guest can reach Google). Paste is hidden:

```bash
read -s GEMINI_API_KEY
export GEMINI_API_KEY
curl -sS "https://generativelanguage.googleapis.com/v1beta/models?key=${GEMINI_API_KEY}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['models'][0]['name'])"
```

You want a model name such as `models/gemini-2.5-flash`, not `API_KEY_INVALID` or a hang. (If you piped the full JSON to `head` instead, `curl: (23) Failure writing output to destination` after that JSON is still success — `head` closed the pipe early.) If the request itself fails on the VM, fix outbound HTTPS before installing OpenClaw.

### 8b. Local Ollama (same machine, enough RAM)

Use this if you want prompts to stay on the mini-PC. OpenClaw will call Ollama at `http://127.0.0.1:11434`. **Do not** publish Ollama through Edgible when it is on the same box.

| RAM on the VM / mini-PC | What to expect |
| ----------------------- | -------------- |
| **4 GB** (this guide’s VM default) | Too small. Use Gemini (8a) or give the guest more RAM. |
| **8 GB** | Floor. Pull a **tiny** model only (about 1B parameters). |
| **16 GB+** | Usable local chat. |

If you have the RAM:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:1b
ollama run llama3.2:1b "Say hello in one word"
```

**Ollama on the Mac, OpenClaw in the VM (32 GB Mac):** Do **not** put the model in the 8 GB guest. Install [Ollama for Mac](https://ollama.com/download). After the VM’s 8 GB, you have on the order of **16 GB** left for a model once macOS and the browser have a share — enough for a real agent, tight for a 27B if Chrome is fat.

On the **Mac**:

```bash
ollama pull gpt-oss:20b
# or, if `ollama run` stays snappy with the VM up: ollama pull qwen3.5:27b
ollama run gpt-oss:20b "Say hello in one word"
```

`gpt-oss:20b` is the safer fit next to an 8 GB VM. Try **Qwen 27B** only if Activity Monitor still has headroom (no swap storm).

Ollama defaults to **Mac localhost only**. The VM’s `127.0.0.1` is the *guest*, so OpenClaw will not see it. Listen on all interfaces on the Mac (home LAN only — do not port-forward **11434** on the router):

```bash
launchctl setenv OLLAMA_HOST "0.0.0.0:11434"
killall Ollama; open -a Ollama
```

On the **VM**, the host is the default gateway (UTM NAT is often `192.168.64.1`; VirtualBox NAT is often `10.0.2.2`):

```bash
HOST=$(ip route | awk '/default/ {print $3; exit}')
curl -sS "http://${HOST}:11434/api/tags"
```

You want JSON with your model name, not connection refused. UTM NAT is often `192.168.64.1` if `$HOST` is wrong. Do **not** test `127.0.0.1` **on the VM** — that is the guest, not the Mac.

Ollama is the **runtime** on the Mac. Qwen / gpt-oss is the **model** you pulled. There is no Google-style API key; OpenClaw still wants a dummy `apiKey` (`ollama-local`).

Do **not** publish Ollama through Edgible on **None**. The VM talking to the Mac on the virtual LAN is enough. After OpenClaw is installed, point it at this host in **9g**.

### 8c. Another cloud provider

Any key OpenClaw onboarding accepts is fine: **OpenAI Platform** (`sk-…` at [platform.openai.com/api-keys](https://platform.openai.com/api-keys), billed separately from ChatGPT), **Groq**, **OpenRouter** (`:free` models, tight daily caps). Set a spend cap if the provider bills.

### 8d. A private model via Edgible (someone you trust)

Someone else (or your other site) runs a model on **their** hardware — Ollama, vLLM, a fine-tune — and publishes that API through Edgible. You point OpenClaw at their `https://<app>.<org>.edgible.com` URL instead of Gemini.

This is a real Edgible job. It is **not** this trial’s path if you already have Gemini (8a).

You need from the operator:

- The **HTTPS URL** of the model API (OpenAI-compatible or Ollama-style).
- A **machine credential** OpenClaw can send on every request (Edgible **API key** protection, or the model’s own key). Browser-only login will not work — OpenClaw is not a browser.
- Confirmation the endpoint is **not** `None` (public). A raw model API on the internet is a gift to strangers.

Trust: they can see your prompts. Treat it like handing them a diary, not like Google’s privacy policy.

When you install OpenClaw, that URL is a **custom / OpenAI-compatible provider**, not “Google” in the wizard. Exact flags wait until the install step.

### Verify

- [ ] If you used Mac Ollama: `curl` from the **VM** to `http://$HOST:11434/api/tags` returns JSON (not `127.0.0.1` on the guest).
- [ ] You did **not** use ChatGPT Free as the model.
- [ ] The key or private URL was not pasted into Slack, git, or the Hello World page.

---

## 9. Install OpenClaw locally

**Outcome:** OpenClaw Gateway running on the VM; you can send `hello` from the guest terminal and get a reply. It is not on the internet yet.

Still **inside the VM**. Leave **hello-world** and the Edgible agent running. Do **not** install OpenClaw on the Mac/PC host for this guide.

This VM is Ubuntu **Server** — there is no desktop browser. Local proof is the CLI, not `openclaw dashboard`.

### 9a. Install the OpenClaw CLI

OpenClaw needs **Node.js 22.22.3+** (the installer can provision it). That is newer than Edgible’s Node 20 floor; let this installer handle it.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

`--no-onboard` skips the long interactive wizard (Telegram and friends). We will onboard with Gemini in the next substep.

Reload PATH if `openclaw` is not found (new shell, or `source ~/.bashrc`):

```bash
openclaw --version
```

Official reference: [Install](https://docs.openclaw.ai/install).

### 9b. Onboard with your model (Gemini default)

If `GEMINI_API_KEY` is empty in this shell, paste it again (hidden):

```bash
read -s GEMINI_API_KEY
export GEMINI_API_KEY
```

Then:

```bash
openclaw onboard --non-interactive --accept-risk \
  --mode local \
  --auth-choice gemini-api-key \
  --gemini-api-key "$GEMINI_API_KEY" \
  --gateway-bind loopback \
  --install-daemon \
  --skip-skills
```

`--accept-risk` is OpenClaw’s required flag for unattended setup (the agent can use tools and a shell). It is not an Edgible setting.

`--gateway-bind loopback` keeps the Control UI on `127.0.0.1:18789` only. Do **not** bind `0.0.0.0` and do **not** port-forward 18789 on the router.

`--skip-skills` keeps this first `hello` about the Gateway + Gemini, not extra downloads. You can add skills later with `openclaw configure`.

If you used **8b / 8c / 8d** instead of Gemini, swap only the auth flags:

| Step 8 choice | Onboard auth |
| ------------- | ------------ |
| 8a Gemini | as above |
| 8b Ollama **in the guest** | `--auth-choice ollama --custom-model-id llama3.2:1b` (tiny; only if the VM has enough RAM) |
| 8b Ollama **on the Mac** | `--auth-choice ollama --custom-base-url "http://$HOST:11434" --custom-model-id gpt-oss:20b` (no `/v1`; `$HOST` from step 8b). Or onboard Gemini first, then **9g**. |
| 8c OpenAI / Groq / … | that provider’s `--auth-choice` and key flag ([CLI automation](https://docs.openclaw.ai/start/wizard-cli-automation)) |
| 8d private Edgible URL | `--auth-choice custom-api-key --custom-base-url 'https://<app>.<org>.edgible.com/v1' --custom-model-id '…' --custom-api-key "$CUSTOM_API_KEY"` |

### 9c. Pin a Flash model (required on Gemini free tier)

OpenClaw’s Google default is often a **Pro / preview** model. Free-tier quota on those is tiny — that is the **429** you hit if you skip this.

Google’s API name from step 8 (`models/gemini-2.5-flash`) is **not** always OpenClaw’s id. Do not guess. List what *this* install knows, then set a **Flash** or **Flash-Lite** row from that list (avoid Pro / preview):

```bash
openclaw models list --provider google
```

Copy an id from the output. Pick in this order (use a row that is **actually listed**):

1. **`flash` in the name, no `pro`, no `preview`** — e.g. `google/gemini-2.5-flash`, `google/gemini-3-flash`, `google/gemini-flash-latest`.
2. If several Flash rows: prefer **latest / highest 2.x or 3.x Flash**, not `-lite`, not `-thinking`.
3. **Flash-Lite** only if you are hitting 429s on Flash and need more RPM (weaker at tools).
4. **Never** Pro, Ultra, or `*-preview` on the AI Studio **free** key — that is the 429.

Then:

```bash
openclaw models set google/<the-flash-id-from-list>
openclaw gateway restart
```

If `set` or the next chat says **model was not found**, you guessed. Run `list` again and set an id that is actually printed.

Skip this substep if you onboarded Ollama (8b) or another cloud provider (8c) whose default already works.

OpenClaw’s **memory search** still defaults to OpenAI embeddings even when chat is Gemini. You will see a warning that no `OPENAI_API_KEY` was found. That is not required for this trial — do **not** add an OpenAI key just to silence it. Disable it:

```bash
openclaw config set agents.defaults.memorySearch.enabled false
openclaw gateway restart
```

To keep semantic memory on the same Gemini key instead: `openclaw config set agents.defaults.memorySearch.provider gemini` (uses extra quota). Verify with `openclaw memory status --deep`.

### 9d. Confirm the Gateway

```bash
openclaw gateway status
openclaw doctor
```

Expect the Gateway **running** on port **18789**, loopback. Confirm the bind with:

```bash
openclaw config get gateway.bind
ss -ltnp | grep 18789
```

You want `bind` = **loopback** (or equivalent), and `ss` showing **`127.0.0.1:18789`** (and maybe `[::1]:18789`). **`0.0.0.0:18789`** or `*:18789` means it is listening on every interface — not what this guide wants. NAT still hides that from the internet, but do not leave it that way.

Linux installs a **systemd user** unit. If you use SSH and then log out, keep it alive:

```bash
sudo loginctl enable-linger "$USER"
```

If status is down:

```bash
openclaw gateway install
openclaw gateway restart
openclaw logs --follow
```

(`Ctrl+C` stops following logs.)

### 9e. Chat from the VM terminal

The Gateway must be up. Do **not** pass `--local` (that fights the running Gateway).

```bash
openclaw agent --agent main --thinking off --message "Say hello in one sentence."
```

You should get a short reply in the terminal. That is local OpenClaw working. Your phone still cannot reach it.

The **first** turn is often OpenClaw’s identity ritual (`Who am I? Who are you?`) instead of a literal hello. That still counts. Answer in one line, for example:

```bash
openclaw agent --agent main --thinking off --message "You are a trial agent on my Ubuntu VM. I am Stefano. Say hello in one sentence."
```

**If the model was not found:** go back to **9c**. You set an id OpenClaw does not have.

**If you see 429 / quota exceeded:** OpenClaw is fine — Google’s free tier said stop. You are still on Pro/preview, or you already used the daily cap. Pin Flash (9c), wait a minute (RPM) or until tomorrow (daily). If logs say **google** is in **cooldown**, wait that out. To keep going now, use 8c (Groq / OpenRouter `:free` / OpenAI Platform) and re-onboard. Usage: [Google AI Studio](https://aistudio.google.com/).

Optional TUI on the VM console:

```bash
openclaw tui
```

### 9f. Control UI in a browser (before Edgible)

If this Ubuntu VM has a **desktop**, do **not** hunt for the token and paste a URL by hand. From a **terminal on the VM desktop** (so it can open Firefox/Chromium):

1. Make sure the Gateway is running. If `openclaw gateway status` is not up:

```bash
openclaw gateway
```

Leave that terminal open (foreground). Or use `openclaw gateway start` if the systemd unit is installed.

2. In a **second** terminal on the same desktop:

```bash
openclaw dashboard
```

That launches the VM browser onto the Control UI (with a short-lived handoff — you should not need to paste `gateway.auth.token`). Send `hello`.

`curl` → **200** only means HTML is served. `openclaw dashboard` is the check that the **browser + WebSocket** path works.

If there is no GUI, there is no in-guest browser — skip to Edgible, or forward host `127.0.0.1:18789` → guest `18789` in UTM/VirtualBox and use the Mac browser. Do not port-forward 18789 on the router.

### 9g. Point OpenClaw at Ollama on the Mac (optional)

**Outcome:** Chat on the VM uses the Mac’s local model (unlimited tokens, no Gemini quota), still via native Ollama — not `/v1`. The dashboard picker lists that model after you register it.

Do this if you already onboarded with **Gemini** (9b) and step **8b** `curl` from the VM already returns JSON. Do **not** re-run full `openclaw onboard` unless you want to redo Gateway setup.

On the **VM**:

```bash
HOST=$(ip route | awk '/default/ {print $3; exit}')
echo "Ollama host: $HOST"
curl -sS -m 5 "http://${HOST}:11434/api/tags"
```

Copy a model **name** from that JSON (example: `gpt-oss:20b` or `qwen3.5:27b`). There is no real Ollama key — `ollama-local` is a dummy.

An explicit `models.providers.ollama` block (`baseUrl`, `api`, `apiKey`) **turns off** auto-discovery. The Control UI picker stays Google-only until you also register the pulled tag in the provider `models` array (use the name from `/api/tags`, not a guess):

```bash
openclaw config set models.providers.ollama.baseUrl "http://${HOST}:11434"
openclaw config set models.providers.ollama.api ollama
openclaw config set models.providers.ollama.apiKey ollama-local
openclaw config set models.providers.ollama.models \
  '[{"id":"gpt-oss:20b","name":"gpt-oss:20b"}]' --strict-json
openclaw gateway restart
openclaw models list --provider ollama
```

`list` must print `ollama/gpt-oss:20b` (or your tag). Then you can pin it as primary if you want local-only chat:

```bash
openclaw models set ollama/gpt-oss:20b
openclaw gateway restart
```

Use the tag you actually pulled (`ollama/qwen3.5:27b` if that is the name). Then:

```bash
openclaw agent --agent main --thinking off --message "Say hello in one sentence."
```

First reply can be slow (Mac loads the weights). If it still behaves like Gemini, `models set` missed — `list` again and set an id that is printed.

To make **Gemini Flash the default** and **gpt-oss only when Gemini has no capacity** (429 / quota / timeout), do **not** leave `models set ollama/…` as primary. After the Ollama provider is configured (the `config set` lines above), on the VM:

```bash
openclaw models list --provider google
openclaw models list --provider ollama
```

Use ids that `list` actually prints (Flash, not Pro; `ollama/gpt-oss:20b` or whatever tag you pulled — **not** a 20 GB-resident Qwen). Then:

```bash
openclaw models set google/<the-flash-id-from-list>
openclaw config set agents.defaults.model.fallbacks '["ollama/gpt-oss:20b"]' --strict-json
openclaw gateway restart
openclaw config get agents.defaults.model
```

You want `primary` = `google/…flash…` and `fallbacks` including `ollama/…`.

**Control UI picker.** Fallbacks do **not** fill the dashboard list. After `gateway restart`, **refresh** the Control UI tab. gpt-oss appears only when `openclaw models list --provider ollama` already prints it (the `models` array above). If `list` omits it, the picker stays Google-only — Ollama often hides models that `/api/show` does not mark as **tool-capable** with **≥16K** context. Fallback can still use `ollama/gpt-oss:20b` from config. To pin local in chat anyway: `/model ollama/gpt-oss:20b`.

Failover applies to the **configured default** and to **cron** (step 12). It does **not** apply if you pick a model in the Control UI picker or `/model` — that choice is strict. Leave the picker on **Default** so Gemini can fail over.

Keep the Ollama model small enough that the Mac does not swap, or the “backup” is slower than waiting for Gemini. Do not publish port **11434** on the router.

### Do not do these yet

- Telegram / Discord — they already dial out; they are not the Edgible job. **WhatsApp** is optional **step 14**.
- Tailscale Serve / Funnel / Cloudflare Tunnel.
- `gateway.auth` set to none.

### Verify

- [ ] `openclaw --version` prints a version on the VM.
- [ ] `openclaw gateway status` shows running on **18789** (loopback).
- [ ] After **9c**, `openclaw models status` shows a **Flash** (not Pro/preview) default if you used Gemini free tier.
- [ ] After **9g** (optional): `openclaw models list --provider ollama` prints `ollama/gpt-oss:…` (or your tag); Control UI picker shows that model after a refresh; leave picker on **Default** if Gemini should fail over. `openclaw models status` and a hello reply still work (Mac Ollama, not `127.0.0.1` on the guest).
- [ ] `openclaw agent --agent main --thinking off --message "Say hello in one sentence."` returns a reply (identity ritual counts).
- [ ] Hello World on the phone still loads (Edgible tunnel unchanged).
- [ ] `curl` to `http://127.0.0.1:18789/` on the VM returns **200**.
- [ ] From a VM **desktop** terminal: Gateway running, then `openclaw dashboard` opens the Control UI and chat works.

---

## 10. Publish the Control UI through Edgible

**Outcome:** The OpenClaw Control UI on your mini-PC, reachable from the internet (phone on cellular), with Edgible **org** login in front — no Tailscale, no port-forward.

Leave **hello-world** running. Keep the Gateway on **loopback** `127.0.0.1:18789`. Edgible on this same VM proxies to that port. Do **not** bind `0.0.0.0` and do **not** use **None** (public) for this app.

Three locks:

1. **Edgible org** — only someone logged into your organisation can hit the hostname.
2. **OpenClaw gateway token** — first time on this browser (Control UI Settings or `#token=`). Local `openclaw dashboard` does not inject it on the Edgible origin.
3. **Device pairing** — first time on this browser: `openclaw devices approve <requestId>` on the VM. Local dashboard pairing does not cover the Edgible tab.

Prefer the **systemd / `openclaw gateway start`** Gateway, not a terminal you might close.

### 10a. Create the Edgible app

Edgible’s interactive picker looks at **Docker** (and a short list of process names). OpenClaw on loopback **18789** often **does not appear**. That is expected. The app is “this port on `mini-pc`,” not “this Docker name.”

**Preferred — set the port yourself:**

```bash
edgible device list
```

Note the id for **mini-pc**, then:

```bash
edgible app create existing \
  --name openclaw-ui \
  --port 18789 \
  --auth-modes org \
  --device-id <mini-pc-id>
```

Leave extra hostnames blank if asked. **Allow other organizations?** **No**. Never **None**.

**If you already started the wizard** and the list is only **hello-world**:

1. You still have to pick a workload — pick **hello-world** if that is all there is (it only tags the description).
2. When asked for the port, choose **Enter a custom port** → **18789**. Do **not** leave it on **8081**.

Confirm `ss -ltnp | grep 18789` still shows `127.0.0.1:18789` before you continue.

The CLI prints an `openclaw-ui.<org>.edgible.com` URL. Do **not** open it yet — wait for the certificate.

### 10b. Wait for the certificate

Same as Hello World. Host browser: [https://app.prod.edgible.com/](https://app.prod.edgible.com/) → **openclaw-ui** → **Certificates** until issued.

```bash
edgible app list
edgible app status
```

Copy the **https://openclaw-ui.<org>.edgible.com** URL (no trailing path). Always copy the exact host from `edgible app list`.

### 10c. Tell OpenClaw that origin is allowed

The landing page loading through Edgible is **not** enough. The Control UI’s JavaScript sends `Origin: https://openclaw-ui.<org>.edgible.com`. Loopback allows `http://127.0.0.1:18789`; Edgible is a **different origin**, so OpenClaw returns **browser origin not allowed**. That is **not** fixed by `openclaw gateway` / `openclaw dashboard` (those are local-only).

On the VM, get the exact hostname (no path):

```bash
edgible app list
```

Allow **both** the local UI and the Edgible origin (replace the host):

```bash
openclaw config set gateway.controlUi.allowedOrigins \
  '["http://127.0.0.1:18789","https://openclaw-ui.YOUR-ORG.edgible.com"]' --strict-json
openclaw gateway restart
```

The Edgible value must be exactly `https://` + hostname from `edgible app list` — pattern `https://<app>.<org>.edgible.com`, no path, no trailing slash, no `www` unless the URL has it.

```bash
openclaw config get gateway.controlUi.allowedOrigins
```

Hard-refresh the Edgible URL. You should get past origin-not-allowed.

Then the Control UI will likely say **gateway token missing (open the dashboard URL and paste the token in Control UI settings)**. That is expected. `openclaw dashboard` injects the token only for the **local** browser (`http://127.0.0.1:18789`). The Edgible page is a different origin; you paste the token yourself.

On the VM, **do not** use `openclaw config get gateway.auth.token`. On 2026.7 that always prints `__OPENCLAW_REDACTED__` — redaction, not a missing token.

`openclaw dashboard --no-open` also **will not** print the token on this build. If clipboard is unavailable it says “Token auto-auth not delivered” and leaves `http://127.0.0.1:18789/` bare. That is expected.

Read the value from disk (stay on the VM; do not paste the token or the whole file into chat):

```bash
python3 -c 'import json, pathlib; p=pathlib.Path.home()/".openclaw"/"openclaw.json"; print(json.load(p.open())["gateway"]["auth"]["token"])'
```

- A long string: that is the token.
- A JSON object (`source`, `id`, …): SecretRef — then `printenv OPENCLAW_GATEWAY_TOKEN` (or the env name in that object).
- Empty / KeyError: `printenv OPENCLAW_GATEWAY_TOKEN`. If still empty, `openclaw doctor --generate-gateway-token` then restart the Gateway and re-run the python line.

`openclaw gateway auth-token --show` is on **newer** docs than 2026.7.1-2; skip it if the subcommand does not exist.

Then either:

- Control UI → **Settings** → gateway token → paste → save, or
- Open `https://openclaw-ui.YOUR-ORG.edgible.com/#token=THEVALUE` (same host as `edgible app list`; fragment, not a query string).

Do **not** set `gateway.auth.mode` to `none` or `trusted-proxy`.

After the token is accepted, the Edgible tab will likely say **device pairing required**. That is expected. Local `openclaw dashboard` auto-pairs that **one** loopback browser; the Edgible origin is a **new** device.

Keep that browser tab open. On the VM:

```bash
openclaw devices list
openclaw devices approve <requestId>
```

Use the `requestId` from **your** page (not an example from this guide). Then reconnect / retry in the same tab. If the browser retried and you get a new id, `devices list` again and approve the current one — do not approve a stale id.

Each new browser (phone, another profile) needs its own one-time approve. Do **not** turn off pairing.

If you **already** pasted the token and still get **token missing**, Edgible’s local proxy may be stripping it. Then:

```bash
openclaw config set gateway.trustedProxies '["127.0.0.1"]' --strict-json
openclaw gateway restart
```

Hard-refresh again and paste the token if Settings was cleared.

**None (public)** was only to prove the tunnel. Switch this app back to **org** when chat works — a public Control UI is an admin shell on the internet. If org auth still fails after that, it is an Edgible bug; do not leave **None** as the real setup.

### Later visits (same browser)

You do **not** repeat origins, `trustedProxies`, token-from-disk, or `devices approve` every time.

| Each visit | First time only (this browser / this phone) | Only if something changed |
| --- | --- | --- |
| Open the same `https://openclaw-ui.<org>.edgible.com` URL | Paste gateway token (or `#token=`) | New hostname → update `allowedOrigins` |
| Edgible **org** login if the session expired | `openclaw devices approve` for this browser | Cleared site data, private window, new browser/profile, or phone → token + pairing again |
| Gateway already running on the mini-PC (`openclaw gateway status`) | — | Token rotated / device revoked → paste + approve again |

Keep a normal (non-private) browser profile. Private windows throw away the device identity on close, so pairing looks “every time.”

### 10d. Phone on cellular

1. Turn **Wi‑Fi off** on the phone.
2. Open the **https** URL. You should get **Edgible org login** first — sign in as the same account as step 1. A stranger with the URL should **not** see OpenClaw.
3. When the Control UI appears, paste the OpenClaw gateway token if asked (same reveal as 10c: python on `~/.openclaw/openclaw.json`, not `config get` and not `dashboard --no-open`). You can also open `https://openclaw-ui.YOUR-ORG.edgible.com/#token=…`. The phone is a **new** device: keep the tab open, `openclaw devices list` on the VM, approve that requestId, then reconnect. `openclaw dashboard` is a **local** handoff; it does not replace this on the phone.
4. Send `hello`. You want a reply, same as in the VM browser.

If **hello-world** still loads on the phone and **openclaw-ui** does not, the tunnel is fine — the failure is OpenClaw (certs, org login, origins, WebSocket, token).

If chat disconnects immediately, Edgible may not be proxying WebSockets yet — stop and note that; do not “fix” it with Tailscale Funnel.

### Verify

- [ ] `edgible app list` shows **openclaw-ui** with an `openclaw-ui.<org>.edgible.com` URL.
- [ ] Console **Certificates** for **openclaw-ui** is issued / ready.
- [ ] Protection is **org**, not None.
- [ ] Phone on **cellular**: Edgible login, then Control UI, then a chat reply.
- [ ] Hello World URL still works (tunnel unchanged).
- [ ] Port **18789** is still not forwarded on the router.

---

## 11. Show OpenClaw actually doing something (from the phone)

**Outcome:** Your public Hello World site changed because the agent on the mini-PC rewrote it — you watched it from the phone.

`hello` only showed the model. A file on disk is proof of tools. The **wow** is Edgible-shaped: you already have a public page at `hello-world.<org>.edgible.com`. OpenClaw lives on the same box. From the Control UI, tell it to replace that page. Refresh the Hello World URL. ChatGPT in a tab cannot change a website on your mini-PC.

Leave the **hello-world** nginx container running (step 7). The HTML is on the **host** at `~/hello-world/index.html` (bind-mounted read-only into nginx — the container cannot write; the agent on the host can).

On the **phone** (cellular, Control UI from step 10), talk like a person — you do not need the path:

```text
Change the hello-world app to say "OpenClaw was here!"
```

That one line is enough on this setup (Gemini Flash + tools). Approve a write if asked.

Then **leave the Control UI**, open `https://hello-world.YOUR-ORG.edgible.com` (same host as step 7, Wi‑Fi still off), and **hard-refresh**. You should see **OpenClaw was here** — not the original Hello World.

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

Wait for the next hour (or **Run now** in Automations), hard-refresh Hello World. A **different** name should be on the page. Gemini free tier has daily caps — if 429s start, pause the job or pin Flash (step 9c). For a long-running box, switch this cron to daily after the demo.

Gemini is enough to *research and dump HTML*. Optional **step 13** is the A/B: wipe back to the step 7 Hello World page, remove that cron, then hire Cursor to rebuild the **same** product (designed On this day + rotation tools). Same public URL. Do not skip 12 — you need to have seen Gemini’s version so Cursor’s looks like an upgrade.

### Verify

- [ ] Hello World names someone **born on this calendar day**, with a short summary.
- [ ] A second run (next hour or Run now) shows a **different** person, not a repeat.
- [ ] Control UI / Automations lists an **hourly** job.
- [ ] No personal mail, files, or calendar in the page source (`cat ~/hello-world/index.html`).
- [ ] Port **18789** is still not forwarded.

---

## 13. Advanced: spawn Cursor Agent for programming (optional)

**Outcome:** You **inspect** the original Hello World page again (step 7 HTML, no Gemini cron). Then Cursor Agent, from that empty folder, builds the **same** On this day product as step 12 — designed site + rotation infra. Hard-refresh the **same** public URL. The contrast is the demo.

Skip this step if you have no Cursor subscription. Gemini/gpt-oss stay the OpenClaw brain. Finish **step 12** first so you have seen Gemini’s dump; this step **wipes** it on purpose.

`openclaw-ui` must stay **org** (step 10). `approve-all` plus this spawn writes the **public** site.

### Approach

Steps 11–12 proved OpenClaw can change a public URL. The HTML is a dump. Step 13 is the specialist A/B: put the **starting** Hello World page back, delete the rotation jobs, look at the folder, then hire Cursor to implement On this day (layout, CSS, updater, state, cron installer) from that slate. Same Edgible hostname. Gemini researched; Cursor engineers.

You do **not** paste a Cursor key into `openclaw models set`. You do **not** make Cursor the default chat model. One-off ACP jobs on `~/hello-world` (nginx bind-mount from step 7 — write on the **host**, not `docker exec`). The hourly tick after install is `python3` via OpenClaw **command** cron, not another ACP spawn.

The job runs on the **Gateway host** (this Ubuntu VM). Cursor.app on the Mac is unused.

**ACP** (Agent Client Protocol) is a small language two programs speak over stdin/stdout: start a session, send a prompt, stream tool calls, finish. OpenClaw is the client. Cursor CLI (`agent acp`) is the server.

**acpx** is OpenClaw’s plugin that owns that client. Until it is installed, **enabled**, and the Gateway **restarted**, `/acp doctor` reports `ACP_BACKEND_MISSING`. On 2026.7 the runtime is **embedded in the plugin**.

| Word | What it is here |
| --- | --- |
| **Harness** | Cursor CLI running as that ACP server. |
| **Session** | One hired job. Key looks like `agent:cursor:acp:<uuid>`. |
| **`/acp doctor`** | Is acpx loaded and can it start `agent acp`? |
| **`/acp spawn`** | Start a session and point it at a directory (`--cwd`). On Control UI this does **not** send the coding task. |
| **`/acp steer`** | Send the actual prompt to that session key. |
| **`/acp close`** | End that Cursor job from OpenClaw’s side (stop the harness process, drop the session key). Does not close the Control UI, uninstall acpx, or log out `agent`. |
| **Bind** | Pin *this chat* so follow-ups go to Cursor. Control UI is **webchat** and **cannot bind** — that is why **this** step uses `/acp spawn` then `/acp steer` with a uuid. **Step 14** (WhatsApp) can `/acp spawn cursor --bind here --cwd …`; after that you type a normal message, no steer. Telegram / Discord stay later. |
| **Oneshot** | Do the task and finish. |
| **`approve-all`** | Headless writes. Applies to **all** ACP jobs on this Gateway until `approve-reads`. |

Once, in order: **reset + inspect Hello World** → CLI + acpx → doctor → spawn → steer the **full** product (site + rotation tools) → run Cursor’s installer → `/acp close` → tighten permissions.

### 13a. Clean slate (Hello World, no rotation cron)

The A/B only works if you can **see** the starting page. Restore step 7’s HTML, delete extra files from 11–12, remove Gemini rotation jobs. nginx stays up; you are not recreating the Edgible app.

On the VM:

```bash
openclaw cron list
```

Remove (or disable) every job that rewrites hello-world / On this day. In Control UI → Automations you can delete them too. Then:

```bash
cd "$HOME/hello-world"
# keep .git if you want history; drop the Gemini/Cursor leftovers
find . -mindepth 1 -maxdepth 1 ! -name '.git' ! -name 'index.html' -exec rm -rf {} +
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Hello World</title></head>
<body>
  <h1>Hello World</h1>
  <p>Served from your Ubuntu VM through Edgible.</p>
</body>
</html>
EOF
ls -la
curl -sS http://127.0.0.1:8081/
```

`ls` should be `index.html` (and maybe `.git`). curl should be **Hello World**, not a biography. On the **phone** (cellular), hard-refresh `https://hello-world.YOUR-ORG.edgible.com`. Same starting page as step 7. That is the before shot.

### 13b. Cursor CLI on the VM

On the **VM** (guest terminal, same user as the Gateway):

```bash
curl https://cursor.com/install -fsS | bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
agent --version
```

You want a version string. The binary is **`agent`**. Some docs say `cursor-agent`; if `which cursor-agent` is empty, that is fine.

Sign in with the **VM desktop browser** (same Cursor account as the Mac is fine):

```bash
agent login
agent status
```

You want a logged-in account, not a prompt to log in. systemd will not see a GUI keychain the way macOS does; Ubuntu file auth from `agent login` as this user is enough.

Do **not** publish Cursor through Edgible. Do **not** put a Cursor API key in Hello World.

echo "$HOME/hello-world" — that path is `--cwd` later. Do **not** spawn against `~/.openclaw`.

### 13c. Install the ACP runtime (acpx plugin)

`ACP_BACKEND_MISSING` / `ACP runtime backend is not configured` means the **Gateway process** has no acpx backend yet. `/acp doctor` in chat cannot fix that — install on the VM, **restart**, then doctor again. Do not `/acp spawn` until doctor is healthy.

On this OpenClaw (**2026.7.x**) the doctor’s own next step is the bare plugin id. On the VM:

```bash
openclaw plugins install acpx
openclaw config set plugins.entries.acpx.enabled true
openclaw config set acp.enabled true
openclaw config set acp.backend acpx
openclaw gateway restart
openclaw plugins list
```

You want `acpx` **enabled** and **loaded** (not only “installed”). If `install acpx` fails or list stays empty:

```bash
openclaw plugins install @openclaw/acpx
openclaw config set plugins.entries.acpx.enabled true
openclaw gateway restart
openclaw plugins list
```

Still missing: `openclaw plugins install clawhub:@openclaw/acpx`, then restart and list again.

If `openclaw config get plugins.allow` prints a JSON list, **`acpx` must be in it**. `plugins install` usually appends it; if not, add `acpx` to that list (keep the other ids) and restart.

`/acp install` in Control UI prints the same enable steps. `acpx --help` is a 2026.7 hint for a **standalone** CLI. Newer acpx is **embedded in the plugin** — if `acpx --help` is “command not found” but `plugins list` shows loaded, ignore the binary and continue. Do not `npm i -g acpx` unless doctor still says backend missing after a loaded plugin + restart.

Then the Cursor harness + a narrow allowlist:

```bash
openclaw config set acp.defaultAgent cursor
openclaw config set acp.allowedAgents '["cursor"]' --strict-json
openclaw config set plugins.entries.acpx.config.probeAgent cursor
```

The Gateway daemon often **does not** have `~/.local/bin` on `PATH`. Point ACP at the real binary (your `$HOME`):

```bash
openclaw config set plugins.entries.acpx.config.agents.cursor.command "$HOME/.local/bin/agent"
openclaw config set plugins.entries.acpx.config.agents.cursor.args '["acp"]' --strict-json
```

If `which cursor-agent` printed a path instead, use that path and args `["acp"]`.

Headless ACP cannot click “allow write.” For **this demo only**:

```bash
openclaw config set plugins.entries.acpx.config.permissionMode approve-all
openclaw gateway restart
```

`approve-all` is for ACP sessions on this Gateway, not only hello-world. Put **org** back on openclaw-ui if you flipped it. After 13e, set `permissionMode` back to `approve-reads`.

Open a **new** Control UI chat (an old tab can still think ACP is missing). Then `/acp doctor`.

### 13d. Doctor, then spawn from the phone

On the VM, Gateway running. In Control UI chat (local dashboard **or** phone on cellular — same as step 10):

```text
/acp doctor
```

Healthy looks like: `configuredBackend: acpx`, `registeredBackend: acpx`, `runtimeDoctor: ok (embedded ACP runtime ready)`, `agent=cursor`, `command=/home/YOURUSER/.local/bin/agent acp`, `healthy: yes`. Doctor’s `cwd` is often `~/.openclaw/workspace` — that is the **probe**, not the site. Spawn still needs `--cwd` from 13b.

`ACP_BACKEND_MISSING` is the failure. Zero sessions / zero turns is normal before the first spawn.

Then spawn (unbound — Control UI cannot `--bind here`; see Approach). Use **your** path from 13b:

```text
/acp spawn cursor --mode oneshot --thread off --cwd /home/YOURUSER/hello-world --label hello-world
```

Success looks like: `Spawned ACP session agent:cursor:acp:<uuid> (oneshot, backend acpx). Session is unbound…` Ignore the hint to `--bind here` on webchat. Copy that **full session key** for steer (do not type the next prompt as a normal chat line — this conversation is still Gemini, not Cursor):

```text
/acp steer --session agent:cursor:acp:YOUR-UUID This folder is the original Hello World page (step 7). Build a phone-friendly On this day mini-site. One notable person born on this calendar date (Wikipedia births). Page structure, every time:
- Name, birth–death years, and a one-line label (what they are known as)
- Who they were
- Why they still matter
- A quirky detail
- Footer at the end: next rotation time in **Australia/Adelaide** (IANA zone), human-readable (include the offset or ACDT/ACST). Compute from “hourly from this run,” e.g. this update + 1 hour, in that zone — not UTC and not the browser’s local zone.
Readable typography and a simple layout (CSS file is fine). Those three sections must be real headings, not a single blob. Public sources only. Nothing about me. Do not docker exec (nginx mount is read-only). Do not touch ~/.openclaw, Edgible config, or openclaw-ui.
```

`--session hello-world` only works if the label stuck; the uuid key always works. `/acp sessions` if you lost it. `/acp status` if it goes quiet. First Cursor run can be slow (login + model). Completions still announce back into this Control UI as a parent task.

Success looks like: `ACP steer sent to…` then a Cursor summary of HTML/CSS/state/script. That write-up is the **harness**, not Gemini describing a change it did not make.

Leave Control UI. On the **phone** (cellular), hard-refresh `https://hello-world.YOUR-ORG.edgible.com`. You want a designed page with **Who they were / Why they still matter / A quirky detail**, and a footer **Next rotation** in Adelaide time — not a single Gemini dump, not “Hello World”, not “OpenClaw was here.”

```bash
cd ~/hello-world
git diff --stat
ls -la
```

You want CSS plus (after 13f) an updater and a way to register hourly **command** cron. Rotation infra is a **second Cursor coding pass**, not a timer that launches Cursor.

When you are done with the visual pass (or after 13f):

```text
/acp close
```

Natural language can work **after** doctor is green. Prefer `/acp spawn` + `/acp steer` for this first run.

### 13f. Rotation infra (Cursor implements it)

**Outcome:** Cursor Agent adds the **tools** for hourly rotation in `~/hello-world`: updater script, already-shown state, midnight rollover, and an installer (or a printed `openclaw cron create …`) that registers a **command** job. You run that installer **once**. After that, the hour belongs to OpenClaw’s scheduler executing Python.

Spawn like 13d (`--cwd` `~/hello-world`). Steer:

```text
/acp steer --session agent:cursor:acp:YOUR-UUID Keep the current visual design. Implement hourly rotation infrastructure in this folder:
1. A Python 3 updater that fetches Wikipedia births for today's month-day, picks one notable person not already shown today, rewrites index.html using the existing CSS and the same sections every time (name + dates, Who they were, Why they still matter, A quirky detail, footer with next rotation in Australia/Adelaide), updates a state file, and starts a new list after local midnight. Print the chosen name to stdout. Next rotation = this run + 1 hour, formatted in IANA Australia/Adelaide (not UTC).
2. A small install script (or README with the exact command) that registers an OpenClaw command cron: every 1h, python3 the updater, cwd this folder. Name the job on-this-day-rotate. Use --command (shell), not an agent prompt and not ACP/Cursor.
3. Tell me the exact commands to run once on the VM.
Do not docker exec. Do not edit ~/.openclaw by hand. Do not schedule Cursor or /acp spawn. Public sources only. Nothing about me.
```

`/acp close` when the summary lists files + the install command. On the VM, run **what Cursor specified** (example only — prefer their output):

```bash
ls -la ~/hello-world
cd ~/hello-world
python3 update.py
```

Hard-refresh the public URL: **different name, same look**. Then run their installer, or if they only printed cron:

```bash
openclaw cron list
openclaw cron create "every 1h" \
  --name "on-this-day-rotate" \
  --command "python3 update.py" \
  --command-cwd "$HOME/hello-world"
```

**Run now** in Automations. Disable the step 12 Gemini job that rewrites HTML in chat — it will overwrite this CSS.

### 13e. Tighten permissions

```bash
openclaw config set plugins.entries.acpx.config.permissionMode approve-reads
openclaw gateway restart
```

Leave ACP **installed** if you will use it again; `allowedAgents: ["cursor"]` stays a narrow door. Do not set `gateway.auth` to none. Do not spawn against `~/.openclaw`.

### Verify

- [ ] `agent status` on the VM shows a logged-in Cursor account.
- [ ] `/acp doctor` in Control UI is healthy.
- [ ] Phone on **cellular**, hard-refresh **hello-world**: designed On this day page with **Who they were**, **Why they still matter**, and **A quirky detail**; footer shows **next rotation** in Australia/Adelaide time; still a person born on this date; still no personal data.
- [ ] `~/hello-world` contains updater + state, and Cursor documented (or installed) **on-this-day-rotate** as an OpenClaw **command** cron. The step 12 Gemini HTML job is disabled or gone.
- [ ] A second run (next hour or Run now) shows a **different** person, not a repeat.
- [ ] `permissionMode` is **approve-reads** again (or you accept the wider ACP blast radius and said so).
- [ ] openclaw-ui protection is still **org**. Port **18789** is still not forwarded.

WhatsApp as the bindable client (same page, retitle sections, no `/acp steer`) is **step 14**.

---

## 14. WhatsApp as the chat client (optional)

**Outcome:** You talk to the mini-PC from **WhatsApp**. `/acp spawn cursor --bind here` pins that chat to Cursor. A normal message retitles the On this day sections. Hard-refresh `hello-world.<org>.edgible.com` — no `/acp steer`, no uuid.

Skip if you have no WhatsApp. Finish **step 13** so the public page already exists. WhatsApp is **not** an Edgible app: the Gateway still owns a **linked device** (WhatsApp Web / Baileys) and dials **out**. Do not publish WhatsApp through Edgible. Do not port-forward. Leave openclaw-ui on **org**.

This is the client that makes ACP feel obvious. Control UI is **webchat** and cannot bind (step 13). WhatsApp can.

### Approach

The phone’s WhatsApp account **links** the Gateway as another device (same idea as WhatsApp Web). Incoming DMs hit OpenClaw on the VM. Gemini is still the dispatcher until you **bind** Cursor. Then this WhatsApp thread *is* the Cursor session until `/acp close`.

A dedicated second number is cleaner (replies arrive as a **different contact**). **Self-chat** on your personal number is supported: `allowFrom` includes you, `selfChatMode` on. WhatsApp has **no bot badge** for a linked device — without a prefix, the first reply looks like you answering yourself. Set `messages.responsePrefix` so replies start with `[OpenClaw]`.

### 14a. Plugin + QR login

On the **VM desktop** terminal (you must **see** the QR; it expires in about a minute). Gateway running:

```bash
openclaw plugins install clawhub:@openclaw/whatsapp
openclaw gateway restart
openclaw channels login --channel whatsapp
```

If install already happened, `channels login` is enough. Phone: **WhatsApp → Settings → Linked devices → Link a device** → scan the terminal QR. You want a linked session, not “can’t link new devices” (remove a stale Web session, or wait if WhatsApp is throttling).

```bash
openclaw channels status --probe
```

WhatsApp should show connected / linked.

Do **not** paste session creds into chat or Hello World.

### 14b. Who may DM

Default is **pairing** (unknown senders wait). Put **your** E.164 in `allowFrom` (example shape only — use your number):

```bash
openclaw config set channels.whatsapp.dmPolicy pairing
openclaw config set channels.whatsapp.allowFrom '["+61XXXXXXXXX"]' --strict-json
openclaw config set channels.whatsapp.selfChatMode true
openclaw config set channels.whatsapp.groupPolicy allowlist
openclaw config set messages.responsePrefix "[OpenClaw] "
openclaw gateway restart
```

### 14c. First WhatsApp `hello`

From the phone, message **yourself** (or a second phone messaging the linked account). If OpenClaw asks to pair:

```bash
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <CODE>
```

That is the same *idea* as `devices approve` for the Control UI — it is **not** the WhatsApp QR. Send `hello`. You want a reply in WhatsApp that **starts with `[OpenClaw]`** (Gemini/gpt-oss behind it). Edgible is unused for this hop.

A bare “Hey Stefano! How can I help you today?” is still the Gateway — it just has no product label. WhatsApp shows it as **your** linked session. Self-chat is *supposed* to default to `[openclaw]` / `[{identity.name}]` when `responsePrefix` is unset; that does not always fire. The explicit prefix from 14b is the check.

### 14d. Bind Cursor — retitle sections (no steer)

If you set `permissionMode` back to `approve-reads` in 13e, headless Cursor cannot write HTML. For this pass:

```bash
openclaw config set plugins.entries.acpx.config.permissionMode approve-all
openclaw gateway restart
```

In the **same** WhatsApp chat (not Control UI):

```text
/acp spawn cursor --bind here --thread off --cwd /home/YOURUSER/hello-world
```

You want a spawn **without** `Conversation bindings are unavailable for webchat`. Then a **normal** message — not `/acp steer`:

```text
Rename the three section headings to: Who this is. Why we remember them. One odd fact.
Keep the body copy, CSS, and the Australia/Adelaide next-rotation footer.
Update the Python updater so the next hourly run uses those headings too.
Do not docker exec. Do not touch ~/.openclaw or Edgible.
```

Wait for Cursor to finish in WhatsApp. `/acp close` when done. Then 13e again (`approve-reads`).

Leave WhatsApp, hard-refresh `https://hello-world.YOUR-ORG.edgible.com` (cellular). You want the **new titles**, same person, same footer.

### Verify

- [ ] `openclaw channels status --probe` shows WhatsApp linked.
- [ ] WhatsApp `hello` gets a reply that starts with **`[OpenClaw]`** (pairing approved if asked).
- [ ] `/acp spawn cursor --bind here …` succeeds in WhatsApp (no webchat bind error).
- [ ] Public On this day page shows **Who this is / Why we remember them / One odd fact** after a hard-refresh.
- [ ] You did not use `/acp steer` for this change.
- [ ] `permissionMode` is **approve-reads** again. openclaw-ui is still **org**. Port **18789** is still not forwarded.

---

## Why this pattern

You just ran OpenClaw on a box you control, with a real `https://<app>.<org>.edgible.com` door, **org login**, and **no hole in the router**. The Gateway stays on loopback. Edgible is outbound 443, a bookmarkable URL, and who in the org can hit it — not Tailscale on every phone, not a Serve hostname only your tailnet can use. First browser still does OpenClaw’s token and device approve; after that it is the URL and, when the session expired, Edgible login.

The agent can think where you choose. Same VM: a local model (Ollama, if the box is big enough) so weights never leave the house. Or point OpenClaw at a **trusted private provider** you published through Edgible — their hardware, your org’s hostname, often **free tokens** from someone you actually trust, not a public chatbot that keeps the conversation. Gemini in this chapter was the cheap on-ramp, not the ceiling.

The VM is the blast radius. OpenClaw can write files and run tools; that happens **inside the guest**, not on the laptop you browse and bank on. You still drive it from anywhere: phone on cellular, Control UI, rewrite the public Hello World page, refresh `hello-world.<org>.edgible.com` and see it. ChatGPT in a tab cannot do that. A stranger with the OpenClaw URL should not see the dashboard. You can — without Tailscale, without port-forward, from wherever you are.

Programming is a **specialist**, not a second chat model. OpenClaw dispatches; Cursor **builds** the public site and the rotation tools. The hourly tick is a command cron on that script. WhatsApp (step 14) is a **bindable** client: spawn `--bind here`, then talk — Control UI still cannot do that.

**Later:** tear down hello-world, OpenClaw, the agent, the CLI, and the VM.