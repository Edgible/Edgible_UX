# 1. Edgible on an Ubuntu VM

**Your own box, reachable from the internet, with no inbound port on your router.**

## 1.0 Why

You have a machine you trust: a mini-PC at home, or the VM standing in for one in this chapter. Nothing outside your own network can reach it. A website, a workflow canvas, an agent or a model on that box is usable only by whoever is sitting at the keyboard. Every other guide starts from what this chapter leaves you with, so do this one first.

The usual ways of publishing one are the ones to avoid. Forwarding a port on the router puts a process you have not hardened in front of everyone who scans your address, and you inherit dynamic DNS and certificates as homework. A mesh VPN works, but every device that will ever need the service has to be enrolled first, which rules out a colleague, a phone you borrowed, or a webhook from Stripe. Renting a cloud box solves reachability by giving up the whole premise: the data is no longer on hardware you own.

Edgible takes the third route. A serving agent on the guest opens an outbound connection on TCP 443 and holds it open, so a public HTTPS hostname of the shape `https://<app>.<org>.edgible.com` appears with a certificate already on it and nothing inbound on your router. Each app, and so each hostname, carries its own auth mode: `org` for “only my organisation gets past a browser login”, `api-key` for a bearer secret, `None` for open to the world. Hello World at the end of this chapter is `None` because it is a throwaway page. A page that loads on a phone with Wi‑Fi off is the proof that publishing worked.

![A phone on cellular opens hello-world.<org>.edgible.com, which is open to anyone. It arrives at nginx bound to 127.0.0.1:8081 on the Ubuntu guest, reached over the outbound connection the serving agent holds open, so the router has no forwarded port.](../../images/diagrams/start-here-01-light.svg#only-light)
![A phone on cellular opens hello-world.<org>.edgible.com, which is open to anyone. It arrives at nginx bound to 127.0.0.1:8081 on the Ubuntu guest, reached over the outbound connection the serving agent holds open, so the router has no forwarded port.](../../images/diagrams/start-here-01-dark.svg#only-dark)

**Where you run this:** signup and the console in the **host browser**; the VM manager on the host; everything else (`edgible`, Docker, `curl`) on the **Ubuntu guest**; the final check on a **phone on cellular**.

## 1.1 The job

You stand up an Ubuntu 24 VM, log the Edgible CLI into your org, register a serving device, and publish Hello World. The “mini-PC” is that guest: VirtualBox (Windows/Linux) or UTM (Mac). Whichever guide you go on to, it starts here.

**Done when**

- An Edgible account and an organisation.
- Ubuntu 24.04 on the VM, outbound HTTPS only (no port forwarding).
- `edgible whoami` on the VM prints Profile / Environment / Account / Organization.
- Serving device `minipc` with **Health check OK**.
- `https://hello-world.<org>.edgible.com` loads on a phone (cellular).

**Need first:** an Edgible account, which 1.3 creates from scratch in a few minutes; an invite email is one route in but not required. Host kit is 1.2. NAT is enough: outbound TCP 443 only.

**Not this chapter:** a website of your own, analytics, n8n, OpenClaw, or a published model. Those are the guides that follow.

## 1.2 What you need on the host computer

| Item | Notes |
| --- | --- |
| An Edgible account | Sign up from [www.edgible.com](https://www.edgible.com), which takes you to the console at [https://app.prod.edgible.com/](https://app.prod.edgible.com/). Host browser, not the VM. A temporary password arrives by email. 1.3 walks through it. |
| VM manager | VirtualBox or UTM; see 1.4. |
| Ubuntu 24.04 LTS ISO | Match the CPU: `amd64` on typical PCs; `arm64` on Apple Silicon. |
| Sudo on the guest | You will install the Edgible serving agent (systemd). It configures WireGuard, iptables, and Caddy. Once it registers, your org lists it as a serving device named `minipc`. The *agent* is the software running on the box; the *device* is that entry in your organisation. |

NAT is enough. The VM only needs outbound TCP 443. Do not port-forward 22, 80, or 443.

---

## 1.3 Create account

**Outcome:** An Edgible account and organisation you can sign into at the console.

Do this on your laptop or desktop browser (the host), not inside the VM. Start at [www.edgible.com](https://www.edgible.com) and follow the signup, which lands you in the console at [https://app.prod.edgible.com/](https://app.prod.edgible.com/). That console, not the marketing site, is where you sign in from then on. You pick a permanent password here; that is what you will type later on the VM for `edgible auth login`.

1. Go to [www.edgible.com](https://www.edgible.com) and start the signup, or open [https://app.prod.edgible.com/](https://app.prod.edgible.com/) directly and choose **Create your account**. If you were sent an invitation email, its link goes to the same place.
2. On **Create your account**, enter first name, last name, and email. If you were invited, use the address the invite was sent to. Submit. Edgible does not ask for a password yet. It emails you a temporary one.
3. Check that inbox (and spam) for the temporary password email. Stay on the **Check your email** page in the browser; it is waiting for that password.
4. Paste the temporary password from the email and continue.
5. You have to change your password before continuing. Enter a new password (at least 8 characters), confirm it, and save. From this point on the temporary password is dead. Use only the new one.
6. You are then asked to create an organisation. Do that now. A default name such as *Your name’s organization* is fine for this trial.
  An organisation is the workspace that owns your serving devices, applications, and public hostnames. Your account is you (email and password). The organisation is the *place* those machines and apps live, so a device registered later is not attached to a personal login, and you can add another person or another box to the same org. Early trials are one person, one org: create it and keep going.
7. You should land on the **Dashboard** at [https://app.prod.edgible.com/](https://app.prod.edgible.com/). An empty device list is fine.

Keep the email and the new password somewhere you can paste into the VM. To return later, always use [https://app.prod.edgible.com/](https://app.prod.edgible.com/).

### Verify

- [ ] You can sign in at [https://app.prod.edgible.com/](https://app.prod.edgible.com/) and see the Dashboard.
- [ ] You have created an organisation.
- [ ] You know the account email and the new password (not the temporary one).

---

## 1.4 Create the virtual machine

**Outcome:** An Ubuntu 24 virtual machine in a VM manager, standing in for the mini-PC.

A virtual machine (VM) is a full computer that runs as an app on the laptop or PC in front of you. It stands in for the mini-PC: Ubuntu 24 inside, Edgible and whatever you go on to publish on that guest, not on your host OS.

A VM is used here only because it costs you no hardware. The serving agent runs just as well on a machine's own Linux install, Ubuntu included, so if you already have a spare box, a mini-PC or a laptop running Ubuntu, install straight onto it and skip to 1.5. Everything after that point is identical, apart from reaching the machine over your LAN rather than through the port forward in 1.5.

To create one you need a VM manager (hypervisor): the app that hosts the VM. Install that first, then create a virtual machine based on Ubuntu 24.04 LTS that runs inside it.


| Your computer       | VM manager                                |
| ------------------- | ----------------------------------------- |
| Windows or Linux PC | [VirtualBox](https://www.virtualbox.org/) |
| Mac                 | [UTM](https://mac.getutm.app/)            |


Use Ubuntu Server (not Desktop). You will work in a terminal, like a mini-PC.

Recommended minimums (sized so the same guest can run the services the later guides publish, not only the Edgible serving agent):


| Resource | Recommended minimum | Floor if you are short on host RAM/disk                                                                      |
| -------- | ------------------- | ------------------------------------------------------------------------------------------------------------ |
| Memory   | 4 GB            | 2 GB can boot Ubuntu and the Edgible serving agent, but a database, an agent or a model on top of it will struggle. |
| Disk     | 40 GB           | 20 GB is enough for this chapter only; container images need the rest. Dynamically allocated is fine. |
| CPUs     | 2               | 1 works; two is the minimum we recommend.                                                                |


Download the ISO from [Ubuntu Server](https://ubuntu.com/download/server): `amd64` for typical VirtualBox on Intel/AMD PCs, `arm64` for UTM **Virtualize** on Apple Silicon.

During the Ubuntu installer:

- Enable the **OpenSSH server**.
- Create a user you will remember (for example `ubuntu`). Give it sudo.
- Skip extra snaps except what the installer requires.

### 1.4.1 VirtualBox (Windows or Linux PC)

1. Install [VirtualBox](https://www.virtualbox.org/) if needed.
2. **New** VM: type Linux, version **Ubuntu (64-bit)**.
3. Set memory, CPUs, and disk to the recommended minimums above (VDI, dynamically allocated is fine).
4. Attach the `amd64` Ubuntu 24.04 Server ISO to the optical drive.
5. Network: **NAT** (default). That is enough for outbound HTTPS.
6. Start the VM and complete the Ubuntu installer. Reboot when asked; remove the ISO if the VM tries to install again.
7. Log in at the VM console with the user you created.

Optional but useful: **Devices → Shared Clipboard → Bidirectional** after Guest Additions, so you can paste the Edgible password. Until then, type it.

### 1.4.2 UTM (Mac)

1. Install [UTM](https://mac.getutm.app/) if needed.
2. **Create a New Virtual Machine** → **Virtualize** (Apple Silicon) or **Virtualize** on Intel Mac with an amd64 ISO. Do not use **Emulate** unless you have no other choice (it is slow).
3. Operating System: **Linux**. Boot ISO: Ubuntu 24.04 Server `arm64` on Apple Silicon, `amd64` on Intel.
4. Set memory, CPU cores, and disk to the recommended minimums above.
5. Network: **Shared Network** (NAT). That is enough.
6. Start, complete the Ubuntu installer, reboot, log in at the console.

### Verify

- [ ] You can log into Ubuntu 24.04 in the VM console.
- [ ] `lsb_release -a` shows 24.04.
- [ ] `sudo -n true` works, or `sudo -v` accepts your password.

---

## 1.5 Prepare the virtual machine

**Outcome:** An updated VM with outbound internet and Docker installed.

This step is ordinary Linux housekeeping on the guest: updates, outbound internet, and Docker (every later guide runs its service in a container). Work inside the VM (console is enough).

SSH from the host is worth setting up now. NAT does not give you a stable guest IP on the LAN, so `ssh ubuntu@minipc` will not resolve: the device name you register with Edgible later is a record in Edgible, not a hostname on your network. Instead, forward one host port to the guest's SSH port.

In VirtualBox: **Settings → Network → Advanced → Port forwarding**, host 2222 → guest 22. In UTM: **Edit → Network → Port Forwarding**, host 2222 → guest 22. Then, from the host:

```bash
sudo apt-get install -y openssh-server   # on the guest, if it is not already there
```

```bash
ssh -p 2222 ubuntu@127.0.0.1
```

Use your VM username if it is not `ubuntu`. Do not forward 80 or 443.

Later chapters copy files to the guest and carry a port back to your laptop's browser over SSH, and both use this forward:

```bash
rsync -av --delete -e 'ssh -p 2222' ./dist/ ubuntu@127.0.0.1:~/site/public/
ssh -p 2222 -L 3000:127.0.0.1:3000 ubuntu@127.0.0.1
```

If your guest is a separate physical machine on your LAN rather than a VM, use its own address and the default port instead, for example `ubuntu@192.168.1.20`.

### 1.5.1 Update Ubuntu

```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y ca-certificates curl
```

If the upgrade installed a new kernel, reboot the VM (`sudo reboot`), then log in again.

### 1.5.2 Confirm outbound internet

The VM only needs outbound HTTPS. A generic check is enough:

```bash
curl -fsSI https://www.google.com | head -n 5
```

You want a successful TLS response (for example HTTP `200` or `301`), not “Could not resolve host” or a hang. If this fails, fix NAT/shared network in the VM manager before installing anything else.

### 1.5.3 Install Docker

Edgible itself does not need Docker. The serving agent publishes whatever is already listening on a local port, however that process got there. Docker is here because it is a tidy way to run and tear down the services these guides publish, and because every later chapter uses it, so installing it once now saves repeating it.

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

If you see permission denied on `/var/run/docker.sock`, the group is not active yet. Run `newgrp docker`, start a new login, or use `sudo docker` until then.

### Verify

- [ ] `sudo apt-get upgrade` completed (reboot if a new kernel was installed).
- [ ] `curl -fsSI https://www.google.com` succeeds.
- [ ] `docker version` and `docker run --rm hello-world` succeed.
- [ ] You have a durable way to type commands on the VM (console or SSH).

---

## 1.6 Install the Edgible CLI (on the VM)

**Outcome:** The `edgible` command on the VM.

Still inside the guest:

```bash
curl -fsSL https://get.edgible.com/install.sh | bash
```

The CLI needs Node.js 20+. The installer offers to install it if it is missing. Accept that.

Reload your PATH if `edgible` is not found (new shell, or `source ~/.bashrc`).

```bash
edgible --version
edgible --help
```

### Verify

- [ ] `edgible --version` prints a version.
- [ ] You did not install the CLI on the Mac/PC host for this guide. The serving device is the VM.

---

## 1.7 Log the CLI into your Edgible account

**Outcome:** The CLI on the VM logged into your organisation.

Use the email and new password from 1.3 (not the temporary password from the email). On the VM:

```bash
edgible auth login \
  --user-email you@example.com \
  --user-password 'your-password'
```

Or run `edgible auth login` and follow the prompts. Depending on how your account signs in, the CLI may hand you a short code and a URL instead of taking a password: open that URL in the host browser, paste the code to confirm it is you, and the CLI finishes on its own. That is the expected flow, not an error, and it is why the console is worth having open in a tab.

This writes tokens and the active organization id under your guest home directory.

```bash
edgible whoami
edgible config list
```

Note the organization id. You will need it when you author YAML in a later chapter.

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

**Outcome:** A serving device (`minipc`) connected to Edgible, with no inbound ports opened on your router.

The Edgible serving agent must run on the VM as systemd. It registers a device named `minipc` in your org.

Keep the name to letters and digits. Hyphens can cause trouble, which is why it is `minipc` rather than `mini-pc`. If you are naming real machines rather than a throwaway VM, a machine-plus-OS pattern reads well and stays unique, as in `lggram17ubuntuv24`. The name has to be unique within the org, and later chapters pass it to `--device-name`, so pick one now and use it consistently.

```bash
sudo edgible agent install \
  --type systemd \
  --device-type serving \
  --device-name minipc \
  --non-interactive
```

Expect 30–60 seconds. Then:

```bash
sudo edgible agent start
sudo systemctl status edgible-agent --no-pager
```

That process connects outbound to the control plane (WebSocket over HTTPS). It does not open a port on your router.

Wait a few seconds, then:

```bash
edgible device health --name minipc
```

Expect **Health check OK** within about 15 seconds.

If it hangs or fails:

```bash
sudo journalctl -u edgible-agent -n 80 --no-pager
sudo edgible agent status
```

Common causes: login was skipped, no outbound 443, or the device name already exists in the org from a previous attempt (`--device-name` must be unique).

### Verify

- [ ] `systemctl status edgible-agent` shows `active (running)`.
- [ ] `edgible device health --name minipc` prints **Health check OK**.
- [ ] Dashboard lists a serving device named `minipc`.

---

## 1.9 Hello World

**Outcome:** An application hosted on your laptop / mini-PC that is accessible from the internet.

The Edgible serving agent being healthy is not the same as “the internet can reach a process on this VM.” This step is Edgible saying Hello World: a throwaway nginx page you open from a phone.

Choose `None` (public access) when asked how the application should be protected. That is acceptable only because this page is a public Hello World. Do not use `None` for anything private.

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

You should see the Hello World HTML. That is local only. Your phone cannot reach `8081` on the VM, and you did not port-forward it.

### 1.9.2 Publish it with Edgible

The nginx container is already listening on `8081`. Create an existing app. Edgible will discover that port. No YAML file.

```bash
edgible app create existing
```

(`app` is short for `application`.) Answer the prompts like this:

| Prompt | Answer |
|--------|--------|
| Application name | `hello-world` |
| Upgrade protocol from HTTP to HTTPS? | Yes (if asked) |
| Custom domains / additional hostnames | leave blank (Enter) |
| How should access to this application be protected? | `None` (public access) |
| Use Edgible managed gateway? | Yes (if asked, so you are not asked for a gateway ID) |
| Select serving device | `minipc` |
| Select local workload | `hello-world` (the nginx container) |
| Select port | `8081` |

When it succeeds, the CLI prints an application URL. Standard shape is `https://<app>.<org>.edgible.com`, so for this app something like `https://hello-world.<org>.edgible.com`. That is **zero-DNS publish**: a working public hostname and certificate with no registrar step and no DNS record to create (see [Glossary](../glossary.md)). Always copy the exact host the CLI prints. Do not open that HTTPS URL yet. The certificate is still being issued.

### 1.9.3 Wait for the certificate (console)

First publish typically takes 30–90 seconds. Use the console to watch it, rather than hammering the URL.

1. On the host browser, open [https://app.prod.edgible.com/](https://app.prod.edgible.com/).
2. Open the `hello-world` application you just created.
3. Find the **Certificates** section. It will move from pending / issuing to issued (or equivalent ready state) when TLS is in place.
4. When the certificate looks ready, copy the HTTPS URL from the console (or from `edgible app list` / `edgible app status` on the VM).

Then, from the VM:

```bash
edgible app list
edgible app status
curl -sS https://<the-hostname>/
```

You should see Hello World over HTTPS. If curl complains about the certificate, wait and refresh **Certificates** in the console; do not fall back to `http://`.

### 1.9.4 Hit it from your phone

**Smoke test.** The page must load when you are not on the same LAN as the laptop.

1. On the phone, turn Wi‑Fi off (use cellular).
2. Open a browser to the URL from `edgible app list`.
3. You should see the same Hello World as `curl` on the VM.

If it fails at first, wait a minute, re-run `edgible app status`, and retry. You are not opening a port on the router; the VM is still NAT-only.

Leave this app running. The guides that follow use it as the check that publishing still works. Each of them ends with a teardown chapter that removes its own services, with a final optional step for removing Hello World once you are finished with all of them.

### Verify

- [ ] `edgible whoami` prints Profile / Environment / Account / Organization.
- [ ] `curl http://127.0.0.1:8081/` shows Hello World on the VM.
- [ ] `edgible app list` shows `hello-world` with a `hello-world.<org>.edgible.com` URL.
- [ ] In the console, `hello-world` → **Certificates** shows the cert as issued / ready.
- [ ] `curl` to the `https` URL shows Hello World on the VM.
- [ ] The same page loads on a phone on cellular.

---

## Next

Pick a guide. They all run on this VM, with Hello World still up.

- [Website on Edgible](../website-on-edgible/README.md): your own site instead of Hello World, plus self-hosted analytics and uptime monitoring. The shortest path from here.
- [n8n on Edgible](../n8n-on-edgible/README.md): workflows, and one process published twice with two auth modes.
- [OpenClaw on Edgible](../openclaw-on-edgible/README.md): an agent you talk to from your phone.
- [LLM on Edgible](../llm-on-edgible/README.md): a model on your own hardware, called by other machines.

Series: [README](README.md).
