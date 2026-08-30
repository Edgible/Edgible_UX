# 2. Publish the site

**Your own pages on a public HTTPS hostname, with the router untouched.**

## 2.0 Why

The site answers on `127.0.0.1:8080`, which is useful to nobody but you. This chapter gives it a hostname anyone can open. The comparison worth holding in mind: the usual way to do this is to rent a box and copy the files to someone else's disk, or to forward port 80 and inherit certificates and dynamic DNS as ongoing work. Here the files stay on your machine, the router stays as it is, and the certificate is issued for you.

This is also the chapter where the auth mode is genuinely `None` and that is the correct answer, not a shortcut. A marketing site is meant to be read by strangers, including ones who will never have a login. Later chapters in this series publish two things that are not meant to be public, so you will see the same command with a different answer.

```
a stranger, anywhere    https://site.<org>.edgible.com   ← None (a public site)
                                 ▲
                                 │  outbound 443, held open
Ubuntu guest            Edgible serving agent ──► 127.0.0.1:8080
                                 │
                        nginx ──► ~/site/public

your router             no forwarded port
```

**Where you run this:** `edgible` on the **Ubuntu guest**, the console in the **host browser**, the final check on a **phone on cellular**.

## 2.1 The job

You create an Edgible app pointing at port `8080` with auth mode `None`, wait for the certificate, and load the site on a phone with Wi‑Fi off.

**Done when**

- `edgible app list` shows an app named `site` with a `site.<org>.edgible.com` URL.
- The console shows that app's certificate as issued.
- `curl https://site.<org>.edgible.com/` from the guest returns your page.
- The site loads on a phone on cellular.
- Port `8080` is still not forwarded, and still bound to `127.0.0.1` on the guest.

**Need first:** [1. The site on the VM](01-site-on-the-vm.md), so `curl http://127.0.0.1:8080/` returns your page. Leave that container and `hello-world` running.

**Not this chapter:** analytics, uptime monitoring, or a domain of your own.

## 2.2 Create the app

The nginx container from chapter 1 is already listening on `8080`, so this is an existing app and there is no YAML to write:

```bash
edgible app create existing
```

Answer the prompts like this:

| Prompt | Answer |
|--------|--------|
| Application name | `site` |
| Upgrade protocol from HTTP to HTTPS? | Yes (if asked) |
| Custom domains / additional hostnames | leave blank (Enter) |
| How should access to this application be protected? | `None` (public access) |
| Use Edgible managed gateway? | Yes (if asked) |
| Select serving device | `mini-pc` |
| Select local workload | `site` (the nginx container) |
| Select port | `8080` |

The CLI prints the application URL, of the shape `https://site.<org>.edgible.com`. Copy the exact host it prints.

`None` here means Edgible does not put a login in front of the hostname. It does not mean the box is exposed: the only thing reachable is port `8080` on that guest, because that is the one port this app names. Nothing else on the machine gained a route in.

## 2.3 Wait for the certificate

First publish usually takes 30 to 90 seconds. Watch it in the console rather than retrying the URL:

1. In the host browser, open [https://app.prod.edgible.com/](https://app.prod.edgible.com/).
2. Open the `site` application.
3. Find the **Certificates** section and wait for issued (or the equivalent ready state).

Then, on the guest:

```bash
edgible app list
curl -sS https://site.<your-org>.edgible.com/ | head -5
```

You should see your HTML. If `curl` complains about the certificate, wait and refresh **Certificates** in the console. Do not work around it with `http://` or `-k`: a certificate error here means the certificate is not ready, and both of those hide the one thing you are checking.

## 2.4 Load it from a phone

**Smoke test.** The page must load when you are nowhere near your own network.

1. On the phone, turn Wi‑Fi off so you are on cellular.
2. Open `https://site.<your-org>.edgible.com`.
3. You should see the same page `curl` returned on the guest.

That page came off a disk in your house, over a connection your machine dialled out. The router still has no forwarded port. Confirm that from the guest, because it is the claim worth checking rather than assuming:

```bash
ss -ltnp | grep 8080
```

Still `127.0.0.1:8080`. Nothing is listening for the internet.

## 2.5 Updating the site

Because chapter 1 bind-mounted the directory, publishing a change is a copy. From your laptop:

```bash
rsync -av --delete ./dist/ ubuntu@mini-pc:~/site/public/
```

Then hard-refresh the public URL. No rebuild, no container restart, no Edgible command: the app points at a port, and what that port serves is your business. Delete a file and it is gone from the site, which is what `--delete` is for and also why it is worth having the site in version control somewhere.

### Verify

- [ ] `edgible app list` shows `site` with a `site.<org>.edgible.com` URL.
- [ ] The console shows that app's certificate as issued.
- [ ] `curl https://site.<org>.edgible.com/` from the guest returns your page.
- [ ] The site loads on a phone on cellular.
- [ ] `ss -ltnp | grep 8080` still shows `127.0.0.1:8080`.
- [ ] Port `8080` is not forwarded on the router.

## Next

[3. Umami on the VM](03-umami-on-the-vm.md) adds analytics, self-hosted beside the site, so visitor data lands on your disk rather than someone else's. Series: [README](README.md).
