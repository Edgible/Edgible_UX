# 5. Uptime monitoring with Uptime Kuma

**A monitor that watches the public hostname the way a visitor would, and tells you when it stops answering.**

## 5.0 Why

You now have three things published and no idea when one of them breaks. A container that exits after an update, a database that fills the disk, a laptop that went to sleep: all of these end with a page that does not load, and none of them announce themselves. The first person to notice should not be a customer.

Uptime Kuma checks a URL on a schedule and notifies you when the answer changes. Pointing it at the public hostname rather than at `127.0.0.1` is deliberate: it then tests the whole path a visitor uses, including the serving agent, the certificate and the tunnel, not just whether nginx is alive locally.

There is one thing this arrangement cannot do, and 5.4 is about not fooling yourself over it.

```
Ubuntu guest      uptime-kuma ──► https://site.<org>.edgible.com  (out and back in)
                        ▲
                        │  127.0.0.1:3001 (loopback only)
                  published as status.<org>.edgible.com ← org
```

**Where you run this:** everything on the **Ubuntu guest**, with the Uptime Kuma interface in the **host browser** once it is published.

## 5.1 The job

You run Uptime Kuma on the guest, publish it with `org`, add a monitor for the public site, and prove it works by breaking the site on purpose.

**Done when**

- `docker compose -f ~/uptime-kuma/docker-compose.yml ps` shows the container running.
- `edgible app list` shows `status` with `org` on port `3001`.
- `https://status.<org>.edgible.com` asks for the Edgible `org` login first.
- A monitor for `https://site.<org>.edgible.com` is up and green.
- Stopping the site container turns that monitor red, and starting it turns it green again.
- Port `3001` is bound to `127.0.0.1` and not forwarded.

**Need first:** [4. Publish Umami](04-publish-umami.md). The site, `analytics`, `umami` and `hello-world` all still published. Check free memory before starting: `free -h`. With the site, Umami, Postgres and the serving agent already running, a 2 GB guest is out of room, and this is the container that will make it fail. 4 GB is the working number.

**Not this chapter:** monitoring from outside your house, status pages for customers, or teardown.

## 5.2 Run Uptime Kuma

On the guest:

```bash
mkdir -p ~/uptime-kuma
cat > ~/uptime-kuma/docker-compose.yml <<'YAML'
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    restart: unless-stopped
    ports:
      - "127.0.0.1:3001:3001"
    volumes:
      - uptime-kuma-data:/app/data
volumes:
  uptime-kuma-data:
YAML

cd ~/uptime-kuma && docker compose up -d
```

Port `3001` avoids the `3000` Umami already holds. The image tag is pinned to a major version rather than `latest`, so an unattended pull cannot replace this with a version whose data format your volume does not match.

**Smoke test.** On the guest:

```bash
curl -sI http://127.0.0.1:3001/ | head -1
ss -ltnp | grep 3001
free -h
```

A `200` or a redirect, the port on `127.0.0.1:3001`, and enough memory left that the numbers are not alarming.

## 5.3 Publish it with `org`, then create the admin account

Uptime Kuma has no password until you create one on first use, and it will hand the account-creation screen to whoever arrives first. So publish it with `org`, which puts the Edgible login in front of it, and only then open it.

```bash
edgible app create existing
```

| Prompt | Answer |
|--------|--------|
| Application name | `status` |
| Upgrade protocol from HTTP to HTTPS? | Yes (if asked) |
| Custom domains / additional hostnames | leave blank (Enter) |
| How should access to this application be protected? | `org` |
| Use Edgible managed gateway? | Yes (if asked) |
| Select serving device | `mini-pc` |
| Select local workload | `uptime-kuma` |
| Select port | `3001` |

Wait for the certificate in the console, then open `https://status.<your-org>.edgible.com` in the host browser. The Edgible `org` login comes first. Behind it, Uptime Kuma asks you to create the admin account: do that now, and store the password.

This is the same shape as the Umami dashboard in 4.3 and the opposite of the site in chapter 2. Three services, three answers to the same prompt, each one following from who needs to reach the thing.

## 5.4 Add the monitor, then break the site on purpose

In Uptime Kuma, **Add New Monitor**:

| Field | Value |
| --- | --- |
| Monitor Type | HTTP(s) |
| Friendly Name | `site` |
| URL | `https://site.<your-org>.edgible.com` |
| Heartbeat Interval | 60 seconds |
| Retries | 2 |

Save, and it should go green within a minute. Add a second monitor the same way for `https://analytics.<your-org>.edgible.com/script.js`, which is the path your visitors' browsers actually depend on. Do not monitor the `org` hostnames: they answer with a login page, so what you would be testing is Edgible's login, not your service.

**Smoke test.** A monitor that has never gone red has not been tested. On the guest:

```bash
docker compose -f ~/site/docker-compose.yml stop
```

Within a couple of minutes the `site` monitor goes red, and the public URL stops loading on your phone. Then:

```bash
docker compose -f ~/site/docker-compose.yml start
```

It returns to green. You have now seen the thing detect a real outage rather than assuming it would.

Notifications are worth setting up while you are here, under **Settings**, then **Notifications**, because a dashboard nobody is looking at is not monitoring. Telegram is the least troublesome: create a bot, paste the token and chat ID, and use **Test** to confirm. Email through a consumer provider tends to need an app password and often silently fails, so if you go that way, do not trust it until the test message arrives.

## 5.5 What this cannot tell you

The monitor runs on the machine it is monitoring. If that machine loses power, loses its internet connection, or is a laptop that closed its lid, the site goes down and so does the thing that was supposed to tell you. You will see nothing, which reads exactly like everything being fine.

So be clear about what you have. This catches the common failures, which are one service breaking while the box stays up: a container that exited, a certificate problem, an application error, a database that stopped accepting connections. It cannot catch the box itself going away.

Covering that needs a check from somewhere else, which does not have to be much. A free external monitor pointed at the same public hostname closes the gap, and the two together are complementary: the external one tells you the machine is gone, and this one tells you which service broke while the machine was fine.

### Verify

- [ ] `docker compose -f ~/uptime-kuma/docker-compose.yml ps` shows the container running.
- [ ] `ss -ltnp | grep 3001` shows `127.0.0.1:3001`.
- [ ] `edgible app list` shows `status` with `org` on port `3001`.
- [ ] `https://status.<org>.edgible.com` asks for the Edgible `org` login, in a private window.
- [ ] Monitors for the site and for `/script.js` are green.
- [ ] Stopping the site container turned the monitor red; starting it turned it green.
- [ ] Ports `3001`, `3000` and `8080` are not forwarded on the router.

## Next

[6. Tear down the website stack](06-website-teardown.md), when you are done, or leave it running: this is the one series in these guides you may actually want to keep. Series: [README](README.md).
