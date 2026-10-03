# The tunneling dream

**Edgible scored against the four requirements in the awesome-tunneling dream list.**

[awesome-tunneling](https://github.com/anderspitman/awesome-tunneling) opens with four things its curator wanted in one tool. This page maps each one to what Edgible does today, and to a step in the guides you can check. The first, second, and fourth hold on the path the guides show. The third holds when the agent is installed without `sudo`.

## The short version

Publish the site from the machine it already runs on.

`edgible agent install`, with no `sudo`, runs the agent as you. In the dashboard, or with `edgible app create existing`, you map a name to the port the site is already listening on. Edgible issues `https://site.<org>.edgible.com`, points that name, and manages the certificate. The page loads before you touch DNS.

`www.example.com` is a name you already have. Edgible does not register it. At the DNS provider for `example.com`, one record puts your name in front:

```text
www.example.com.   CNAME   site.<org>.edgible.com.
```

Edgible then issues a certificate for `www.example.com` as well. The rest of the zone stays where it is.

That is the list, in order. A name is pointed for you (1). Certificates are managed (2). The client does not run as root (3). The dashboard or the CLI does the mapping (4). The `CNAME` is the extra step only when you want your own name in front.

## The four requirements

In his words, shortened only enough to sit on the page:

1. Register a domain name, and automatically point its records at the server that runs the tunnels.
2. Automatically set up and manage HTTPS certificates for that domain, apex and subdomains.
3. A client that tunnels HTTP and TCP through that server, without root on the client.
4. A simple GUI that maps a domain or subdomain to a port on a client, and proxies every connection for that name there.

He adds that some tools already issue certificates through Let's Encrypt. What he has not found is domain registration and DNS management done simply, in the same tool.

## How we read the intent

This is our reading of those four lines. The scorecard below is scored against this reading. If the intent is different, the miss is in this section.

1. One tool should leave you with a working name pointed at the tunnel, without a separate trip to a registrar and a DNS panel. "Register" and "point the records" are one requirement: getting the name and managing its DNS belong together. We do not read it as "the tool must be an accredited registrar that sells any name you type." We do read it as "DNS for that name is not a chore you do by hand." His note about registration and DNS being the missing piece is what fixes that reading.
2. Once there is a domain, HTTPS for it should be issued and renewed for you. Apex means the bare name, `example.com`. A subdomain is a name in front of it, such as `www.example.com`. Both should work. The apex is named on purpose: it is the name people type, and it is the name a normal `CNAME` often cannot point, because that record cannot sit next to mail records. We read the requirement as "cover the whole domain, including that awkward name," not as a separate kind of certificate.
3. The program on your machine that carries the tunnel, for both web and plain TCP, should not have to run as root.
4. A screen where you choose a name, a port, and a machine, and every connection to that name is proxied to that port on that machine.

## Scorecard

| # | Dream item | Edgible today |
| --- | --- | --- |
| 1 | Name and DNS, pointed for you | Met for the hostname Edgible issues. A name you already own is one `CNAME` you create, not a registration inside Edgible. |
| 2 | Certificates managed | Met for that issued hostname, and for a custom name after the `CNAME` exists. A bare apex (`example.com` with no subdomain) is a DNS limit, described below. |
| 3 | Client without root | Met for `edgible agent install` with no `sudo`: the agent runs as you. `sudo edgible agent install` is a system service and that process runs as root. |
| 4 | GUI maps a hostname to a port | Met in the dashboard, and by the same fields in `edgible app create existing`. |

## 1. A name, with records pointed for you

The dream asks for domain registration and DNS in one step. Edgible is not a registrar. It does not sell you `example.com`.

What it does on first publish is zero-DNS publish: `edgible app create existing` provisions `https://<app>.<org>.edgible.com`, points that name at your serving device, and starts certificate issuance. You do not edit a zone. [Edgible on an Ubuntu VM](../guides/start-here/01-edgible-on-vm.md) §1.9 is the check: the CLI prints the URL before any `CNAME` exists, and the page loads on a phone on cellular.

A name you already own is a second step, not the first. [A domain of your own](../guides/website-on-edgible/02-publish-the-site.md#26-a-domain-of-your-own-optional) adds the hostname on the app and has you create one record at the DNS provider you already use:

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

Certificates, and a screen that maps a name to a port, are already common. A client that needs no root is less common, and it is the install these guides use, with the logged-out Mac still the exception in the table above. The row the list's author says he cannot find is the first: a name that exists and points at your machine without a separate DNS chore. That is the ordinary publish path here. A working `https://` name is issued before you edit a zone. If you later attach a name you already own, that is one record at the DNS provider you already use, and the rest of the zone stays where it is. The other shapes in this field are a short-lived name you do not keep, a name you cannot put your own domain on, a custom name only after the whole zone moves to the operator, or you run the DNS, the certificates, and the proxy yourself. [For evaluators and architects](for-evaluators.md) compares those approaches, still without product names.

## Related

- [For evaluators and architects](for-evaluators.md): the same job, without this list's wording
- [What Edgible does](../capabilities.md): each feature mapped to the chapter that demonstrates it
- [Glossary](../glossary.md): zero-DNS publish, custom domain, serving agent, auth modes

