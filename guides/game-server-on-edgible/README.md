# Game server on Edgible: chapters

**Game night on a box you own, for the friends you invite.**

A Minecraft server is the oldest self-hosting job there is, and the usual ways to share one each cost something. A rented server is a monthly bill and someone else's machine. A forwarded port puts your home address on the internet. Here the server runs in a container on the machine from Start here, and your friends reach it on two published hostnames, with no port forwarded and nothing rented.

It is also the first series in these guides that is not web. Minecraft comes in two editions that speak two protocols: Java Edition, on PCs, connects over TCP, and Bedrock Edition, on phones and tablets, connects over UDP. One server answers both, because a plugin called Geyser lets Bedrock players into a Java server. Edgible publishes each protocol as its own app, so the same machine is a TCP app and a UDP app at once.

![Friends on PC and on phone reach two hostnames: mc-java on TCP port 25565 and mc-bedrock on UDP port 29132, both open to anyone. Both arrive at one Minecraft server on one machine you own, with Paper on 127.0.0.1:25565 and Geyser on 127.0.0.1:29132, and no forwarded port.](../../images/diagrams/game-server-on-edgible-light.svg#only-light)
![Friends on PC and on phone reach two hostnames: mc-java on TCP port 25565 and mc-bedrock on UDP port 29132, both open to anyone. Both arrive at one Minecraft server on one machine you own, with Paper on 127.0.0.1:25565 and Geyser on 127.0.0.1:29132, and no forwarded port.](../../images/diagrams/game-server-on-edgible-dark.svg#only-dark)

A TCP or UDP app has no auth mode. There is no browser and no HTTP request in a game connection, so there is nothing for an `org` login or an `api-key` to attach to, and the CLI refuses one. What decides who plays is the game itself: online mode, which checks every Java player's account, and a whitelist, which lists the friends you invite. Chapter 1 turns both on before anything is published.

Treat a TCP or UDP app as reachable by anyone, not only by people you gave the address to. That is fine for a game server, whose whitelist does the job a login would. It is not fine for a service whose only protection would be an address nobody knows, such as SSH, a database or a home-automation controller. Do not publish those as TCP or UDP apps.

Each chapter is one job and one smoke test. Do them in order.

Chapters share a shape: a one-line hook under the title, then **N.0 Why** (what is missing without this chapter, and which machine you run it on), then **N.1 The job** (what you'll do, how you'll know, what you need, what this is not). Steps after that, a **Verify** checklist that mirrors *Done when*, and **Next** at the end.

**Need first:** [Start here](../start-here/README.md) (serving device `minipc`, Docker installed, Hello World on the phone). Leave `hello-world` running. The server takes 2 GB of the guest's memory, so the guest wants 4 GB.

| # | Chapter | Smoke test |
| --- | --- | --- |
| 1 | [1. Minecraft on the VM](01-minecraft-on-the-vm.md) | `mc-monitor` answers on TCP `25565` and on UDP `19132` inside the container; nothing on the internet yet |
| 2 | [2. Java players over TCP](02-java-over-tcp.md) | `mc-java.<org>.edgible.com:25565` answers from outside; a friend on PC joins |
| 3 | [3. Bedrock players over UDP](03-bedrock-over-udp.md) | `mc-bedrock.<org>.edgible.com:29132` answers from outside; a friend on a phone joins the same world |
| 4 | [4. Tear down the game server](04-game-server-teardown.md) | Both hostnames gone; nothing on `25565` or `29132`; `hello-world` and the serving agent left |

Two limits are stated where they arise. A TCP or UDP app must use a public port from `20000` to `29999`, and one app holds a port on its gateway at a time ([2.5](02-java-over-tcp.md#25-when-port-25565-is-taken)). And most consoles cannot add a server by address, so this series promises friends on PC and on phone ([3.5](03-bedrock-over-udp.md#35-what-about-consoles)).

Other guides: [Website on Edgible](../website-on-edgible/README.md), [n8n on Edgible](../n8n-on-edgible/README.md), [OpenClaw on Edgible](../openclaw-on-edgible/README.md), [LLM on Edgible](../llm-on-edgible/README.md), [Self Hosting is Social](../self-hosting-is-social/README.md).
