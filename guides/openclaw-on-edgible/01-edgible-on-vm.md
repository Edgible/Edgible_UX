# 1. Edgible on an Ubuntu VM

**A public HTTPS page on a box you own — cellular, no port-forward, no mesh VPN.**

## 1.1 The job

You stand up an Ubuntu 24 VM, log the Edgible CLI into your org, register a serving device, and publish Hello World. The “mini-PC” is that guest: **VirtualBox** (Windows/Linux) or **UTM** (Mac). OpenClaw is the next chapter.

**Done when**

- An Edgible account and organisation from the invite.
- Ubuntu 24.04 on the VM, outbound HTTPS only (no port forwarding).
- `edgible whoami` on the VM prints Profile / Environment / Account / Organization.
- Serving device `mini-pc` with **Health check OK**.
- `https://hello-world.<org>.edgible.com` loads on a **phone (cellular)**.

**Need first:** the invite email. Host kit is 1.2. NAT is enough — outbound TCP 443 only.

**Not this chapter:** OpenClaw, Control UI on the internet, Telegram, or the Edgible skill.

## 1.2 What you need on the host computer

| Item | Notes |
| --- | --- |
| Invite email | Console: [https://app.prod.edgible.com/](https://app.prod.edgible.com/). Host browser, not the VM. A **temporary password** arrives in a second email. |
| VM manager | **VirtualBox** or **UTM** — see 1.4. |
| Ubuntu **24.04 LTS** ISO | Match the CPU: **amd64** on typical PCs; **arm64** on Apple Silicon. |
| Sudo on the guest | You will install the **Edgible serving agent** (systemd). It configures WireGuard, iptables, and Caddy. That is not OpenClaw. |

NAT is enough. The VM only needs **outbound TCP 443**. Do not port-forward 22, 80, 443, or 18789. A **Gemini** key and Cursor are later chapters.

---

## 1.3 Create account

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

## 1.4 Create the virtual machine

**Outcome:** An Ubuntu 24 virtual machine in a VM manager — a stand-in for the mini-PC.

A **virtual machine (VM)** is a full computer that runs as an app on the laptop or PC in front of you. It stands in for the mini-PC on the shelf: Ubuntu 24 inside, Edgible (and later OpenClaw) on that guest, not on your host OS.

To create one you need a **VM manager** (hypervisor) — the app that hosts the VM. Install that first, then create a virtual machine **based on Ubuntu 24.04 LTS** that runs inside it.


| Your computer       | VM manager                                |
| ------------------- | ----------------------------------------- |
| Windows or Linux PC | [VirtualBox](https://www.virtualbox.org/) |
| Mac                 | [UTM](https://mac.getutm.app/)            |


Use **Ubuntu Server** (not Desktop). You will work in a terminal, like a mini-PC.

**Recommended minimums** for this guide (sized so the same guest can run OpenClaw later, not only the Edgible serving agent):


| Resource | Recommended minimum | Floor if you are short on host RAM/disk                                                                      |
| -------- | ------------------- | ------------------------------------------------------------------------------------------------------------ |
| Memory   | **4 GB**            | **2 GB** can boot Ubuntu and the Edgible serving agent; OpenClaw will struggle.                                      |
| Disk     | **40 GB**           | **20 GB** is enough for this chapter only; images and OpenClaw need the rest. Dynamically allocated is fine. |
| CPUs     | **2**               | **1** works; two is the minimum we recommend.                                                                |


Download the ISO from [Ubuntu Server](https://ubuntu.com/download/server): **amd64** for typical VirtualBox on Intel/AMD PCs, **arm64** for UTM **Virtualize** on Apple Silicon.

During the Ubuntu installer:

- Enable the **OpenSSH server**.
- Create a user you will remember (for example `ubuntu`). Give it sudo.
- Skip extra snaps except what the installer requires.

### 1.4.1 VirtualBox (Windows or Linux PC)

1. Install [VirtualBox](https://www.virtualbox.org/) if needed.
2. **New** VM: type Linux, version **Ubuntu (64-bit)**.
3. Set memory, CPUs, and disk to the recommended minimums above (VDI, dynamically allocated is fine).
4. Attach the **amd64** Ubuntu 24.04 Server ISO to the optical drive.
5. Network: **NAT** (default). That is enough for outbound HTTPS.
6. Start the VM and complete the Ubuntu installer. Reboot when asked; remove the ISO if the VM tries to install again.
7. Log in at the VM console with the user you created.

Optional but useful: **Devices → Shared Clipboard → Bidirectional** after Guest Additions, so you can paste the Edgible password. Until then, type it.

### 1.4.2 UTM (Mac)

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

## 1.5 Prepare the virtual machine

**Outcome:** An updated VM with outbound internet and Docker installed.

This step is ordinary Linux housekeeping on the guest: updates, outbound internet, and **Docker** (OpenClaw will need it; Edgible can publish a compose app later). Work **inside the VM** (console is enough).

**SSH from the host (optional).** NAT does not give you a stable guest IP on the LAN. You can stay in the VM window, or in VirtualBox add **Settings → Network → Advanced → Port forwarding** for **host 2222 → guest 22** only, then:

```bash
ssh -p 2222 ubuntu@127.0.0.1
```

Use your VM username if it is not `ubuntu`. Do **not** forward 80, 443, or 18789.

### 1.5.1 Update Ubuntu

```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y ca-certificates curl
```

If the upgrade installed a new kernel, reboot the VM (`sudo reboot`), then log in again.

### 1.5.2 Confirm outbound internet

The VM only needs **outbound** HTTPS. A generic check is enough:

```bash
curl -fsSI https://www.google.com | head -n 5
```

You want a successful TLS response (for example HTTP **200** or **301**), not “Could not resolve host” or a hang. If this fails, fix NAT/shared network in the VM manager before installing anything else.

### 1.5.3 Install Docker

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

## 1.6 Install the Edgible CLI (on the VM)

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

## 1.7 Log the CLI into your Edgible account

**Outcome:** The CLI on the VM logged into your organisation.

Use the email and **new** password from **1.3** (not the temporary password from the email). On the VM:

```bash
edgible auth login \
  --user-email you@example.com \
  --user-password 'your-password'
```

Or run `edgible auth login` and follow the prompts.

This writes tokens and the active organization id under your **guest** home directory.

```bash
edgible whoami
edgible config list
```

Note the **organization** id. You will need it when you author YAML in a later chapter.

If you belong to more than one org:

```bash
edgible auth select-org
```

### Verify

- [ ] Login completes without error.
- [ ] `edgible whoami` prints Profile / Environment / Account / Organization.
- [ ] `edgible config list` shows an organization id.
- [ ] Dashboard still shows your account (refresh). Devices may still be empty.

---

## 1.8 Install and start the Edgible serving agent

**Outcome:** A serving device (`mini-pc`) connected to Edgible, with no inbound ports opened on your router.

The Edgible serving agent must run **on the VM** as systemd. It registers a device named `mini-pc` in your org. It is not OpenClaw.

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

That process connects **outbound** to the control plane (WebSocket over HTTPS). It does not open a port on your router.

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

## 1.9 Hello World

**Outcome:** An application hosted on your laptop / mini-PC that is accessible from the internet.

The Edgible serving agent being healthy is not the same as “the internet can reach a process on this VM.” This step is Edgible saying **Hello World**: a throwaway nginx page you open from a **phone**, before you touch OpenClaw.

Choose **None** (public access) when asked how the application should be protected. That is acceptable **only** because this page is a public Hello World. Do not use None for OpenClaw or anything private.

### 1.9.1 Run nginx on the VM

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

### 1.9.2 Publish it with Edgible

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

### 1.9.3 Wait for the certificate (console)

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

### 1.9.4 Hit it from your phone

This is the real check: the page must load when you are **not** on the same LAN as the laptop.

1. On the phone, turn **Wi‑Fi off** (use cellular).
2. Open a browser to the **URL** from `edgible app list`.
3. You should see the same **Hello World** as `curl` on the VM.

If it fails at first, wait a minute, re-run `edgible app status`, and retry. You are not opening a port on the router; the VM is still NAT-only.

Leave this app running until the teardown chapter (or `edgible app delete --name hello-world` when you are done with it).

### Verify

- [ ] `edgible whoami` prints Profile / Environment / Account / Organization.
- [ ] `curl http://127.0.0.1:8081/` shows Hello World on the VM.
- [ ] `edgible app list` shows **hello-world** with a `hello-world.<org>.edgible.com` URL.
- [ ] In the console, **hello-world** → **Certificates** shows the cert as issued / ready.
- [ ] `curl` to the **https** URL shows Hello World on the VM.
- [ ] The same page loads on a phone on **cellular**.

---

## Next

[2. OpenClaw on the VM (loopback Gateway)](02-openclaw-on-the-box.md) — Gateway on loopback, Gemini Flash, local hello / Control UI. Series: [README](README.md).
