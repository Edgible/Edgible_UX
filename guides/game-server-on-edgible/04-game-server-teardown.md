# 4. Tear down the game server

**Both hostnames gone, the server stopped, and a deliberate decision about the world.**

## 4.0 Why

Neither app in this series has an auth mode, so for as long as they exist, anyone who has the address can reach the server and read its status. The whitelist keeps strangers out of the world, but a server you have stopped playing on is still a public endpoint on a box you own.

This is also a shared machine. It may still be running another series, so the default here is this series only: `hello-world` and the Edgible serving agent stay.

If game night is a regular thing, skip this chapter. The world lives in a named volume, and the server carries on as long as the guest does.

**Where you run this:** `edgible` and Docker on the **Ubuntu guest**.

## 4.1 The job

You delete both apps, stop the server, then decide separately whether the world goes too.

**Done when**

- `edgible app list` no longer shows `mc-java` or `mc-bedrock`.
- `mc-monitor status` against `mc-java.<org>.edgible.com` fails to find the host.
- `docker ps` no longer shows `minecraft`.
- Nothing is listening on `25565` or `29132`.
- `hello-world` still loads, and `edgible device health` is still OK.

**Need first:** nothing beyond having done the series.

**Not this chapter:** deleting the Ubuntu VM, `edgible auth logout`, or tearing down another series.

## 4.2 Unpublish both hostnames

```bash
edgible app delete mc-java --yes
edgible app delete mc-bedrock --yes
```

Each prints `Teardown confirmed` once the serving device has dropped the app.

**Smoke test.** On the guest:

```bash
docker run --rm itzg/mc-monitor status --host mc-java.<org>.edgible.com --port 25565
```

It fails with `could not connect to Minecraft server`, because the hostname no longer resolves. `edgible app list` shows neither app.

Deleting an app removes the hostname, not the server. Minecraft is still running on loopback, which is why unpublishing comes first: nothing is reachable from outside while you take the rest down.

## 4.3 Stop the server

```bash
docker compose -f ~/minecraft/docker-compose.yml down
```

`down` without `-v` keeps the named volume, so the world, the whitelist and the Floodgate setting survive. Bringing it back is `docker compose up -d` in `~/minecraft`, then chapters 2 and 3 again to publish it.

**Smoke test.** On the guest:

```bash
docker ps
ss -ltnp | grep 25565
ss -lunp | grep 29132
```

No `minecraft` container, and nothing on either port.

## 4.4 The world, if you want it gone

The volume holds the world your friends built. Removing it is separate from everything above because it is the one step that cannot be undone. To keep a copy first:

```bash
docker run --rm -v minecraft_minecraft-data:/data -v "$HOME:/backup" alpine tar -czf /backup/minecraft-world.tgz -C /data .
```

Then remove it:

```bash
docker volume rm minecraft_minecraft-data
rm -rf ~/minecraft
```

Compose prefixes the volume name with the project directory, so confirm the name with `docker volume ls` first.

## Verify

- [ ] `edgible app list` shows neither `mc-java` nor `mc-bedrock`.
- [ ] `mc-monitor status` against `mc-java.<org>.edgible.com` fails to connect.
- [ ] `docker ps` does not show `minecraft`.
- [ ] `ss` shows nothing on `25565` or `29132`.
- [ ] `hello-world` still loads, and `edgible device health` is OK.

## Next

Bring the server back with `docker compose up -d` in `~/minecraft` whenever game night comes round. Other guides: [Website on Edgible](../website-on-edgible/README.md), [Self Hosting is Social](../self-hosting-is-social/README.md). Series: [README](README.md).
