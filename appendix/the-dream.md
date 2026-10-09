# The tunneling dream

**Edgible scored against the four requirements in the awesome-tunneling dream list.**

[awesome-tunneling](https://github.com/anderspitman/awesome-tunneling) opens with four things its curator wanted in one tool. This page maps each one to what Edgible does today, and to a step in the guides you can check. Three of the four are met. The first, the one he says nobody has done, is only partly met here, and the section on it says why.

One thing up front. The dream describes a tool that pairs a client on your machine with a server that runs the tunnels. With Edgible, that server is ours: you run the serving agent, which connects out to it, and Edgible runs the server. If you want to run the server as well, the self-hosted tools on the same list are the place to look.

## The short version

Publish the site from the machine it already runs on.

`edgible agent install`, with no `sudo`, runs the agent as you. In the dashboard, or with `edgible app create existing`, you map a name to the port the site is already listening on. Edgible issues `https://site.<org>.edgible.com`, points that name, and manages the certificate. The page loads before you touch DNS.

`www.example.com` is a name you already have. Edgible does not register it. At the DNS provider for `example.com`, one record puts your name in front:

```text
www.example.com.   CNAME   site.<org>.edgible.com.
```

Edgible then issues a certificate for `www.example.com` as well. The rest of the zone stays where it is.

So: a working name is pointed for you, but registering your own domain is still a separate job (1, partly). Certificates are managed (2). The client does not run as root, for web and TCP (3). The dashboard or the CLI does the mapping (4).

## The four requirements

In his words, shortened only enough to sit on the page:

1. Register a domain name, and automatically point its records at the server that runs the tunnels.
2. Automatically set up and manage HTTPS certificates for that domain, apex and subdomains.
3. A client that tunnels HTTP and TCP through that server, without root on the client.
4. A simple GUI that maps a domain or subdomain to a port on a client, and proxies every connection for that name there.

He adds that some tools already issue certificates through Let's Encrypt. What he has not found is domain registration and DNS management done simply, in the same tool.

## How we read the intent

This is our reading of those four lines. The scorecard below is scored against this reading. If the intent is different, the miss is in this section.

1. One tool should get you a domain and leave its DNS pointed at the tunnel, without a separate trip to a registrar and a DNS panel. "Register" and "point the records" are one requirement: getting the name and managing its DNS belong together. We do not read it as "the tool must be an accredited registrar." We do read it as "your own domain, with DNS that is not a chore you do by hand." His note that registration and DNS are the missing piece is what fixes that reading, and it is why a name under someone else's domain only meets half of it.
2. Once there is a domain, HTTPS for it should be issued and renewed for you. Apex means the bare name, `example.com`. A subdomain is a name in front of it, such as `www.example.com`. Both should work. The apex is named on purpose: it is the name people type, and it is the name a normal `CNAME` often cannot point, because that record cannot sit next to mail records. We read the requirement as "cover the whole domain, including that awkward name," not as a separate kind of certificate.
3. The program on your machine that carries the tunnel, for both web and plain TCP, should not have to run as root.
4. A screen where you choose a name, a port, and a machine, and every connection to that name is proxied to that port on that machine.

## Scorecard

| # | Dream item | Edgible today |
| --- | --- | --- |
| 1 | Name and DNS, pointed for you | Partly met. The hostname Edgible issues works with no DNS step. A domain of your own is registered elsewhere and pointed with one `CNAME` you create. |
| 2 | Certificates managed | Met for the issued hostname, and for a custom name once the `CNAME` exists. A bare apex (`example.com` with no subdomain) is a DNS limit, described below. |
| 3 | Client without root | Met for `edgible agent install` with no `sudo`, for HTTPS and for plain TCP. `sudo edgible agent install` is a system service, and that process runs as root. |
| 4 | GUI maps a hostname to a port | Met in the dashboard, and by the same fields in `edgible app create existing`. |

## 1. A name, with records pointed for you

The dream asks for domain registration and DNS in one step. Edgible is not a registrar. It does not sell you `example.com`.

What it does on first publish is zero-DNS publish: `edgible app create existing` provisions `https://<app>.<org>.edgible.com`, points that name at your serving device, and starts certificate issuance. You do not edit a zone. [Edgible on an Ubuntu VM](../guides/start-here/01-edgible-on-vm.md) §1.9 is the check: the CLI prints the URL before any `CNAME` exists, and the page loads on a phone on cellular.

That is half of the item. The name is under `edgible.com`, not yours, and other services also hand out a lasting name under their own domain. The half he is missing, buying your own domain and having its DNS managed for you in the same tool, is still missing here.

What Edgible does instead is keep that half small. [A domain of your own](../guides/website-on-edgible/02-publish-the-site.md#26-a-domain-of-your-own-optional) adds the hostname on the app and has you create one record at the DNS provider you already use:

```text
www.example.com.   CNAME   site.<org>.edgible.com.
```

The zone stays where it is. Nameservers do not move.

## 2. Certificates managed for you

The certificate for `https://<app>.<org>.edgible.com` is issued as part of publish. In the console, open the app and watch **Certificates** move to issued. The same state shows in `edgible app list` and `edgible app status`. [Edgible on an Ubuntu VM](../guides/start-here/01-edgible-on-vm.md) §1.9.3 is that wait.

After the `CNAME` in §1 above, Edgible issues a certificate for the custom name as well. [A domain of your own](../guides/website-on-edgible/02-publish-the-site.md#26-a-domain-of-your-own-optional) is the check: `www.example.com` loads with a certificate for that name.

A `CNAME` cannot sit at the apex of a domain next to mail records, so `example.com` with no subdomain needs a provider that offers `ALIAS` or `ANAME` flattening, or a redirect from the apex to `www`. That constraint is DNS, and the website guide states it in the same section.

## 3. A client that does not need root

This item is met when you do not use `sudo`.

`edgible agent install` with no `sudo` installs a per-user agent. On Linux that is `systemd-user`. On macOS that is `launchd-user`. The process runs as the user who installed it, and the tunnel is userspace, so it does not open a kernel network device. `ps` on that process shows your login user, not root.

The guides install that way: [Edgible on an Ubuntu VM](../guides/start-here/01-edgible-on-vm.md) §1.8, and [Edgible publishes Ollama](../guides/llm-on-edgible/02-edgible-to-ollama.md). On Linux, §1.8 also runs `sudo loginctl enable-linger "$USER"` once so the agent stays up after you log out.

`sudo edgible agent install` is the other tier. That writes a system service. On Linux the unit sets `User=root`. On macOS it is a launch daemon under `/Library/LaunchDaemons/`, which runs as root for as long as the service is up. The steps in the guides do not use it. [Edgible on an Ubuntu VM](../guides/start-here/01-edgible-on-vm.md) §1.6 shows the link that puts the launcher on `sudo`'s path, for anyone who wants this tier.

As installed, that per-user agent stops when you log out. On Linux it also stops when an SSH session ends, and it does not start at boot. Linux can change that. macOS cannot.

| | Linux | macOS |
| --- | --- | --- |
| Install | `edgible agent install` | `edgible agent install` |
| Runs as | your login user | your login user |
| After logout, as installed | stops | stops |
| Keep it running after logout | Run once: `sudo loginctl enable-linger "$USER"`. After that it starts at boot and stays up when you log out. The agent still runs as you. | No equivalent. An always-on Mac uses `sudo edgible agent install`, and that process runs as root. |

### Plain TCP

The dream asks for HTTP and TCP. The guides publish web apps over HTTPS, but the same serving agent carries plain TCP, and UDP as well. The CLI lists the protocols an app can use:

```bash
edgible app create existing --help | grep -i protocol
```

That prints `Protocol (http, https, tcp, udp)`. Only the protocol changes:

```bash
edgible app create existing \
  --name game-server \
  --port 25565 \
  --protocol tcp \
  --device-id <device-id>
```

No chapter checks a TCP app end to end yet. Until one does, the line above is the claim, and the help output is its check.

## 4. A GUI that maps a hostname to a port

The dashboard at [app.prod.edgible.com](https://app.prod.edgible.com/) is that GUI. Creating an app asks for the serving device and the local port, and the hostname is the one from §1.

The same mapping is the prompt table in [Edgible on an Ubuntu VM](../guides/start-here/01-edgible-on-vm.md) §1.9.2: application name, auth mode, serving device, port. From the CLI, with the prompts answered by flags:

```bash
edgible app create existing \
  --name hello-world \
  --port 8081 \
  --auth-modes none \
  --device-id <device-id>
```

`edgible app list` then shows that name, that device, and the issued hostname. Connections to the hostname are proxied to that port on that device. The phone check in §1.9 is the proof the proxy is live, and the verify list on that chapter still shows the port was not forwarded on the router.

## What is different

Most of the dream is common ground now. Plenty of tools manage certificates, map a name to a port, and run their client without root, and Edgible does those too. The piece he is missing, registering your own domain and managing its DNS in the same tool, is not solved here either.

Where Edgible differs is in what happens around that gap:

- Your DNS stays where it is. Your own domain is one `CNAME` at the provider you already use. You do not move your nameservers or hand the whole zone to us, and the rest of the zone, mail included, stays as it is. [A domain of your own](../guides/website-on-edgible/02-publish-the-site.md#26-a-domain-of-your-own-optional) is the check.
- Each published hostname has its own auth mode: `None`, `org`, or `api-key`. One process can sit on two hostnames with different auth modes. [Publish Umami](../guides/website-on-edgible/04-publish-umami.md) puts the tracking script on a `None` hostname and the dashboard on an `org` hostname, on the same port.
- It is not only web. The same serving agent carries plain TCP and UDP, so the dream's "HTTP and TCP" is one tool here, not two. §3 has the check.

[For evaluators and architects](for-evaluators.md) compares these approaches more broadly, without product names.

## Related

- [For evaluators and architects](for-evaluators.md): the same job, without this list's wording
- [What Edgible does](../capabilities.md): each feature mapped to the chapter that demonstrates it
- [Glossary](../glossary.md): zero-DNS publish, custom domain, serving agent, auth modes
