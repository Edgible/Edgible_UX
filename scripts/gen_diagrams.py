#!/usr/bin/env python3
"""Draw the topology diagrams for the series indexes and the chapters.

Every series makes the same shape of claim: some caller out on the internet
reaches one or more published hostnames, each with its own auth mode, and all of
them arrive at one machine whose services are bound to loopback behind a router
with nothing forwarded. So the diagrams are generated from a short spec rather
than drawn by hand, which keeps the pictures saying the same thing the same
way, and makes a palette or wording change one edit instead of many.

A chapter diagram is the same shape narrowed to one step, so it comes from the
same spec and the same renderer, with four things a series index never needs: a
tag on a hostname card saying which chapter published it, an empty hostname
column for the chapters where nothing is published yet, a second machine panel
for the ones where the service lives on the Mac and the guest only forwards, and
a third-party box for the outbound connections to Gemini, Telegram or WhatsApp.

Two files per series, light and dark. Material's colour scheme is a toggle on
the page rather than an OS preference, and an SVG loaded through <img> cannot
see that toggle, so the markdown references both with #only-light and #only-dark
and the theme hides the one that does not apply.

Run from the repo root; writes into static/images/diagrams/.
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "static" / "images" / "diagrams"

# Auth modes are the one thing a reader must be able to tell apart at a glance,
# so each gets a colour rather than only a label.
OPEN, LOGIN, KEY = "open", "login", "key"

PALETTES = {
    "light": {
        "panel": "#e4e8f2",
        "card": "#ffffff",
        "edge": "#c2c8d8",
        "rule": "#e0e3ea",
        "ink": "#000033",
        "muted": "#4a4f66",
        # The same mid blue the table headers use, so a header bar reads as a
        # header wherever it appears. Navy is reserved for the chrome.
        "machine": "#2e4a9e",
        "machine_ink": "#ffffff",
        OPEN: "#2f6fb0",
        LOGIN: "#000033",
        KEY: "#7a5cc0",
        "flow_open": "#2f6fb0",
        "flow_closed": "#8a90a6",
    },
    "dark": {
        "panel": "#1a1a2e",
        "card": "#22223c",
        "edge": "#3a3a5c",
        "rule": "#33334f",
        "ink": "#e7e7f0",
        "muted": "#a5a8bd",
        "machine": "#3a56ad",
        "machine_ink": "#ffffff",
        OPEN: "#7db2e8",
        LOGIN: "#c3c6d8",
        KEY: "#b39ce8",
        "flow_open": "#7db2e8",
        "flow_closed": "#767a93",
    },
}

AUTH_LABEL = {
    OPEN: "open to anyone",
    LOGIN: "org login",
    KEY: "bearer key",
}

SERIES = {
    "start-here": {
        "caller": ["Phone", "cellular", "Wi-Fi off"],
        "hosts": [("hello-world.<org>.edgible.com", OPEN)],
        "machine": "ONE MACHINE YOU OWN",
        "ports": [("127.0.0.1:8080", "Hello World")],
        "notes": [
            "the agent connects out, nothing connects in",
            "router: no forwarded port",
            "nothing listens on the LAN",
        ],
    },
    "website-on-edgible": {
        "caller": ["Phone", "cellular", "Wi-Fi off"],
        "hosts": [
            ("site.<org>.edgible.com", OPEN),
            ("analytics.<org>…/script.js", OPEN),
            ("umami.<org>.edgible.com", LOGIN),
            ("status.<org>.edgible.com", LOGIN),
        ],
        "machine": "ONE MACHINE YOU OWN",
        "ports": [
            ("127.0.0.1:8080", "nginx, the site"),
            ("127.0.0.1:3000", "Umami"),
            ("127.0.0.1:3001", "Uptime Kuma"),
        ],
        "notes": [
            "visitor data on your disk",
            "router: no forwarded port",
        ],
    },
    "n8n-on-edgible": {
        "caller": ["Phone", "and GitHub,", "Stripe, curl"],
        "hosts": [
            ("n8n.<org>.edgible.com", LOGIN),
            ("n8n-hooks.<org>.edgible.com", OPEN),
        ],
        "machine": "ONE MACHINE YOU OWN",
        "ports": [("127.0.0.1:5678", "n8n, one process")],
        "notes": [
            "credentials stay in the container",
            "two hostnames, one port",
            "router: no forwarded port",
        ],
    },
    "openclaw-on-edgible": {
        "caller": ["Phone", "cellular", "no VPN"],
        "hosts": [("openclaw-ui.<org>.edgible.com", LOGIN)],
        "machine": "ONE MACHINE YOU OWN",
        "ports": [("127.0.0.1:18789", "OpenClaw Gateway")],
        "notes": [
            "the agent's shell never leaves the box",
            "admin console behind org login",
            "router: no forwarded port",
        ],
    },
    "llm-on-edgible": {
        "caller": ["n8n VM", "and OpenClaw,", "on other boxes"],
        "hosts": [("ollama.<org>.edgible.com", KEY)],
        "machine": "THE GPU STAYS HOME",
        "ports": [
            ("127.0.0.1:11434", "Ollama on the Mac"),
            ("guest forwarder", "socat to the Mac"),
        ],
        "notes": [
            "weights never leave the machine",
            "Authorization: Bearer, not an open port",
            "router: no forwarded port",
        ],
    },
}

MAC = {
    "title": "MACOS HOST",
    "ports": [("0.0.0.0:11434", "Ollama.app, Metal")],
    "notes": ["the weights and the GPU stay here"],
    "link": "UTM virt LAN, often 192.168.64.1",
}

# One entry per chapter that opens with a diagram. The key is the SVG basename,
# so it is the series directory and the chapter number, and the markdown refers
# to it as ../../images/diagrams/<key>-light.svg.
CHAPTERS = {
    "start-here-01": {
        "caller": ["Phone", "cellular", "Wi-Fi off"],
        "hosts": [("hello-world.<org>.edgible.com", OPEN, "this chapter")],
        "machine": "UBUNTU GUEST",
        "ports": [("127.0.0.1:8081", "nginx, Hello World")],
        "notes": [
            "the serving agent holds the connection open",
            "router: no forwarded port",
        ],
        "alt": (
            "A phone on cellular opens hello-world.<org>.edgible.com, which is open to "
            "anyone. It arrives at nginx bound to 127.0.0.1:8081 on the Ubuntu guest, "
            "reached over the outbound connection the serving agent holds open, so the "
            "router has no forwarded port."
        ),
    },
    "website-on-edgible-01": {
        "caller": ["The internet", "cannot reach", "this yet"],
        "hosts": [],
        "empty": "nothing published yet",
        "machine": "UBUNTU GUEST",
        "ports": [
            ("127.0.0.1:8080", "nginx container"),
            ("~/site/public", "the files it serves"),
        ],
        "notes": ["curl on the guest is the only client", "router: no forwarded port"],
        "alt": (
            "Nothing is published yet. An nginx container on the Ubuntu guest serves "
            "~/site/public on 127.0.0.1:8080, reachable only from the guest itself."
        ),
    },
    "website-on-edgible-02": {
        "caller": ["A stranger", "anywhere", "no login"],
        "hosts": [("site.<org>.edgible.com", OPEN, "this chapter")],
        "machine": "UBUNTU GUEST",
        "ports": [("127.0.0.1:8080", "nginx"), ("~/site/public", "the files")],
        "notes": ["the files stay on your disk", "router: no forwarded port"],
        "alt": (
            "A stranger anywhere opens site.<org>.edgible.com, open to anyone with no "
            "login. It arrives at nginx on 127.0.0.1:8080 on the Ubuntu guest, serving "
            "files that stay on your own disk, with no forwarded port."
        ),
    },
    "website-on-edgible-03": {
        "caller": ["The internet", "cannot reach", "this yet"],
        "hosts": [],
        "empty": "nothing published yet",
        "machine": "UBUNTU GUEST",
        "ports": [("127.0.0.1:3000", "umami container"), ("postgres", "named volume: the data")],
        "notes": ["the visitor data lands here", "router: no forwarded port"],
        "alt": (
            "Umami is not published yet. The umami container answers on "
            "127.0.0.1:3000 on the Ubuntu guest and writes to a postgres container "
            "whose named volume holds the visitor data."
        ),
    },
    "website-on-edgible-04": {
        "caller": ["Visitors", "and you,", "anywhere"],
        "hosts": [
            ("analytics.<org>…/script.js", OPEN, "every visitor"),
            ("umami.<org>.edgible.com", LOGIN, "you"),
        ],
        "machine": "UBUNTU GUEST",
        "ports": [("127.0.0.1:3000", "umami"), ("postgres", "the data")],
        "notes": ["one port, two hostnames", "two different access rules"],
        "alt": (
            "Two hostnames reach the same Umami on 127.0.0.1:3000. The tracking script "
            "on analytics.<org>.edgible.com is open to every visitor; the dashboard on "
            "umami.<org>.edgible.com needs an org login."
        ),
    },
    "website-on-edgible-05": {
        "caller": ["You", "on a phone", "or laptop"],
        "hosts": [("status.<org>.edgible.com", LOGIN, "this chapter")],
        "machine": "UBUNTU GUEST",
        "ports": [("127.0.0.1:3001", "uptime-kuma")],
        "notes": ["the monitor answers to you", "router: no forwarded port"],
        "outbound": {
            "title": "site.<org>.edgible.com",
            "sub": "your own public hostname, checked from the outside",
            "label": "the monitor's own check, out and back in",
        },
        "alt": (
            "Uptime Kuma on 127.0.0.1:3001 on the Ubuntu guest is published as "
            "status.<org>.edgible.com behind an org login, and checks your public site "
            "hostname by going out to the internet and back in."
        ),
    },
    "n8n-on-edgible-01": {
        "caller": ["The internet", "cannot reach", "this yet"],
        "hosts": [],
        "empty": "no hostname yet",
        "machine": "UBUNTU GUEST",
        "ports": [("127.0.0.1:5678", "n8n")],
        "notes": ["the editor is loopback only", "router: no forwarded port"],
        "alt": (
            "n8n is not published yet. It answers on 127.0.0.1:5678 on the Ubuntu "
            "guest, reachable only from the guest itself."
        ),
    },
    "n8n-on-edgible-02": {
        "caller": ["You", "on cellular", "Wi-Fi off"],
        "hosts": [
            ("n8n.<org>.edgible.com", LOGIN, "this chapter"),
            ("n8n-hooks.<org>.edgible.com", OPEN, "chapter 3"),
        ],
        "machine": "UBUNTU GUEST",
        "ports": [("127.0.0.1:5678", "n8n, one process")],
        "notes": ["canvas, credentials, workflows", "one port behind both hostnames"],
        "alt": (
            "The n8n editor is published as n8n.<org>.edgible.com behind an org login, "
            "and chapter 3 adds an open webhook hostname. Both arrive at the one n8n "
            "process on 127.0.0.1:5678 on the Ubuntu guest."
        ),
    },
    "n8n-on-edgible-03": {
        "caller": ["Stripe", "and GitHub,", "no account"],
        "hosts": [
            ("n8n-hooks.<org>.edgible.com", OPEN, "this chapter"),
            ("n8n.<org>.edgible.com", LOGIN, "chapter 2"),
        ],
        "machine": "UBUNTU GUEST",
        "ports": [("127.0.0.1:5678", "n8n, one process")],
        "notes": ["canvas, credentials, workflows", "one port behind both hostnames"],
        "alt": (
            "Services that cannot log in, such as Stripe and GitHub, reach the open "
            "n8n-hooks.<org>.edgible.com, while the editor stays behind an org login on "
            "n8n.<org>.edgible.com. Both arrive at one n8n process on 127.0.0.1:5678."
        ),
    },
    "n8n-on-edgible-05": {
        "caller": ["A stranger", "on cellular", "no account"],
        "hosts": [
            ("n8n-hooks.<org>…/webhook/…", OPEN, "this chapter"),
            ("n8n.<org>.edgible.com", LOGIN, "canvas only"),
        ],
        "machine": "UBUNTU GUEST",
        "ports": [("127.0.0.1:5678", "n8n, Webhook node")],
        "notes": ["the JSON reply comes from your box", "router: no forwarded port"],
        "alt": (
            "A stranger on cellular with no account hits a webhook path on the open "
            "n8n-hooks hostname and gets a JSON reply from the n8n Webhook node on "
            "127.0.0.1:5678, while the canvas stays behind an org login."
        ),
    },
    "openclaw-on-edgible-01": {
        "caller": ["Phone", "cellular", "Wi-Fi off"],
        "hosts": [("hello-world.<org>.edgible.com", OPEN, "Start here")],
        "machine": "UBUNTU GUEST",
        "ports": [
            ("127.0.0.1:18789", "OpenClaw Gateway"),
            ("127.0.0.1:8081", "nginx, still public"),
        ],
        "notes": [
            "no hostname for the Gateway in this chapter",
            "router: 18789 not forwarded",
        ],
        "alt": (
            "The OpenClaw Gateway runs on 127.0.0.1:18789 on the Ubuntu guest with no "
            "hostname of its own in this chapter, and connects out to Google AI Studio "
            "for Gemini Flash. Only the Hello World page from Start here is published."
        ),
        "outbound": {
            "title": "Google AI Studio",
            "sub": "Gemini Flash answers the prompts",
            "label": "the Gateway connects out",
        },
    },
    "openclaw-on-edgible-02": {
        "caller": ["You", "on cellular", "no VPN"],
        "hosts": [("openclaw-ui.<org>.edgible.com", LOGIN, "this chapter")],
        "machine": "UBUNTU GUEST",
        "ports": [("127.0.0.1:18789", "OpenClaw Gateway")],
        "notes": [
            "org login, then the gateway token",
            "then approve the device",
            "router: 18789 still not forwarded",
        ],
        "alt": (
            "The OpenClaw Control UI is published as openclaw-ui.<org>.edgible.com "
            "behind an org login, then a gateway token and a device approval. It "
            "arrives at the Gateway on 127.0.0.1:18789, which stays unforwarded."
        ),
    },
    "openclaw-on-edgible-04": {
        "caller": ["You", "in chat:", "UI, Telegram", "or WhatsApp"],
        "hosts": [("openclaw-ui.<org>.edgible.com", LOGIN, "chapter 2")],
        "machine": "UBUNTU GUEST",
        "ports": [
            ("127.0.0.1:18789", "OpenClaw Gateway"),
            ("edgible skill", "runs the edgible CLI"),
        ],
        "notes": ["the CLI acts in your own org", "the same box that serves your apps"],
        "alt": (
            "Asking in chat, through the Control UI, Telegram or WhatsApp, reaches the "
            "OpenClaw Gateway on 127.0.0.1:18789, which runs the edgible skill and so "
            "the edgible CLI in your own org, on the box that serves your apps."
        ),
    },
    "openclaw-on-edgible-05": {
        "caller": ["You", "on a phone", "Telegram app"],
        "hosts": [("openclaw-ui.<org>.edgible.com", LOGIN, "chapter 2")],
        "machine": "UBUNTU GUEST",
        "ports": [("127.0.0.1:18789", "OpenClaw Gateway")],
        "notes": ["no inbound door for the bot", "router: 18789 not forwarded"],
        "outbound": {
            "title": "api.telegram.org",
            "sub": "your bot's messages arrive over that connection",
            "label": "the Gateway connects out",
        },
        "alt": (
            "Messaging your Telegram bot from a phone reaches the OpenClaw Gateway on "
            "127.0.0.1:18789, because the Gateway connects out to api.telegram.org and "
            "collects the messages. There is no inbound door for the bot."
        ),
    },
    "openclaw-on-edgible-06": {
        "caller": ["You", "on a phone", "WhatsApp"],
        "hosts": [("openclaw-ui.<org>.edgible.com", LOGIN, "cannot bind")],
        "machine": "UBUNTU GUEST",
        "ports": [
            ("127.0.0.1:18789", "OpenClaw Gateway"),
            ("Cursor over ACP", "edits ~/hello-world"),
        ],
        "notes": ["a linked device, not a business API", "the bound thread is the phone's"],
        "outbound": {
            "title": "WhatsApp servers",
            "sub": "the linked device pairs over that connection",
            "label": "the Gateway connects out",
        },
        "alt": (
            "WhatsApp on a phone, paired as a linked device, reaches the OpenClaw "
            "Gateway on 127.0.0.1:18789 over the connection the Gateway opens "
            "outward, and the bound thread drives Cursor over ACP to edit the public "
            "Hello World page."
        ),
    },
    "llm-on-edgible-02": {
        "caller": ["Any", "off-box", "client"],
        "hosts": [("ollama.<org>.edgible.com", KEY, "this chapter")],
        "machine": "UBUNTU GUEST",
        "ports": [
            ("socat", "127.0.0.1:11434 here"),
            ("serving agent", "app ollama, api-key"),
        ],
        "notes": ["the guest only forwards"],
        "machine2": MAC,
        "alt": (
            "An off-box client calls ollama.<org>.edgible.com with a bearer key. It "
            "arrives at the serving agent on the Ubuntu guest, where socat forwards "
            "127.0.0.1:11434 across the virt LAN to Ollama.app on the macOS host, so "
            "the weights and the GPU stay there."
        ),
    },
    "llm-on-edgible-03": {
        "caller": ["n8n VM", "another box", "you own"],
        "hosts": [
            ("ollama.<org>.edgible.com", KEY, "Basic LLM Chain"),
            ("ollama.<org>…/v1", KEY, "AI Assistant chat"),
        ],
        "machine": "UBUNTU GUEST",
        "ports": [("socat", "127.0.0.1:11434 here")],
        "notes": ["Authorization: Bearer, not an open port"],
        "machine2": MAC,
        "alt": (
            "n8n on another box you own calls ollama.<org>.edgible.com with a bearer "
            "key, the Basic LLM Chain node on the bare hostname and the AI Assistant "
            "chat on the /v1 path. Both arrive through socat on the Ubuntu guest at "
            "Ollama.app on the macOS host."
        ),
    },
    "llm-on-edgible-04": {
        "caller": ["OpenClaw", "another box", "you own"],
        "hosts": [("ollama.<org>.edgible.com", KEY, "no /v1 suffix")],
        "machine": "UBUNTU GUEST",
        "ports": [("socat", "127.0.0.1:11434 here")],
        "notes": ["Authorization: Bearer, not an open port"],
        "machine2": {**MAC, "ports": [("0.0.0.0:11434", "gpt-oss:20b loads here")]},
        "alt": (
            "The OpenClaw Gateway on another box you own calls "
            "ollama.<org>.edgible.com with a bearer key and no /v1 suffix. It arrives "
            "through socat on the Ubuntu guest at Ollama.app on the macOS host, where "
            "gpt-oss:20b loads."
        ),
    },
}

WIDTH = 960
CARD_H = 58
CARD_GAP = 18
CARD_X = 250
CARD_W = 250
MACHINE_X = 612
MACHINE_W = 340
PAD = 40
PANEL_GAP = 44
COL2 = 146
OUT_H = 64


def panel_h(ports: list, notes: list) -> int:
    return 96 + 26 * (len(ports) + len(notes))


# SVG text does not wrap, so a string that is too long for its box silently
# runs out over the edge of the panel. These are rough advance widths for the
# two fonts at the sizes used above, deliberately generous, and the check below
# fails the build rather than shipping a diagram with prose hanging off it.
JOST_EM = 0.52
MONO_EM = 0.55


def too_wide(text: str, limit: int, size: int, mono: bool = False) -> bool:
    return len(text) * size * (MONO_EM if mono else JOST_EM) > limit


def check(name: str, spec: dict) -> list[str]:
    bad = []
    inner = MACHINE_W - 40

    def panel(title: str, ports: list, notes: list, where: str) -> None:
        if too_wide(title, inner, 13):
            bad.append(f"{name}: {where} title does not fit: {title!r}")
        for port, what in ports:
            if too_wide(port, COL2 - 30, 12, mono=True):
                bad.append(f"{name}: {where} port does not fit: {port!r}")
            if too_wide(what, inner - COL2 + 20, 12, mono=True):
                bad.append(f"{name}: {where} port note does not fit: {what!r}")
        for note in notes:
            if too_wide(note, inner, 13):
                bad.append(f"{name}: {where} note does not fit: {note!r}")

    panel(spec["machine"], spec["ports"], spec["notes"], "machine")
    if spec.get("machine2"):
        m2 = spec["machine2"]
        panel(m2["title"], m2["ports"], m2.get("notes", []), "second machine")

    for host in spec["hosts"]:
        name_w = len(host[0]) * 13 * MONO_EM
        tag = host[2] if len(host) > 2 else ""
        if name_w > CARD_W - 30:
            bad.append(f"{name}: hostname does not fit: {host[0]!r}")
        if too_wide(AUTH_LABEL[host[1]] + tag, CARD_W - 60, 13):
            bad.append(f"{name}: auth label and tag collide: {tag!r}")

    if not spec["hosts"] and too_wide(spec.get("empty", ""), CARD_W - 24, 13):
        bad.append(f"{name}: empty label does not fit: {spec['empty']!r}")

    return bad


def svg_for(spec: dict, palette: dict) -> str:
    p = palette
    hosts = spec["hosts"]
    second = spec.get("machine2")
    outbound = spec.get("outbound")

    stack_h = max(len(hosts), 1) * CARD_H + (max(len(hosts), 1) - 1) * CARD_GAP
    h1 = panel_h(spec["ports"], spec["notes"])
    machines_h = h1 + (PANEL_GAP + panel_h(second["ports"], second.get("notes", [])) if second else 0)

    # The hostname column and the caller sit on the axis of the first machine
    # panel, because that is where the outbound connection is drawn from. If
    # either is taller than that panel, the whole machine column moves down.
    my = PAD
    axis = my + h1 / 2
    overflow = max(PAD - (axis - stack_h / 2), PAD - (axis - 60))
    if overflow > 0:
        my += overflow
        axis += overflow

    content_bottom = max(my + machines_h, axis + stack_h / 2, axis + 60)
    height = content_bottom + PAD + (OUT_H + 44 if outbound else 0)

    parts: list[str] = []
    add = parts.append

    add(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height:.0f}" '
        f'width="{WIDTH}" height="{height:.0f}" role="img" aria-labelledby="t d">'
    )
    add(f"<title id=\"t\">{escape(spec['alt'])}</title>")
    add(f"<desc id=\"d\">{escape(spec['alt'])}</desc>")
    add(
        "<style>"
        f".label{{font-family:Jost,system-ui,sans-serif;font-size:15px;fill:{p['ink']}}}"
        f".small{{font-family:Jost,system-ui,sans-serif;font-size:13px;fill:{p['muted']}}}"
        f".mono{{font-family:Iosevka,ui-monospace,monospace;font-size:13px;fill:{p['ink']}}}"
        f".monoxs{{font-family:Iosevka,ui-monospace,monospace;font-size:12px;fill:{p['muted']}}}"
        f".head{{font-family:Jost,system-ui,sans-serif;font-size:13px;font-weight:600;"
        f"fill:{p['machine_ink']};letter-spacing:.04em}}"
        f".card{{fill:{p['card']};stroke:{p['edge']};stroke-width:1.5}}"
        "</style>"
    )
    add(f'<rect x="0" y="0" width="{WIDTH}" height="{height:.0f}" rx="10" fill="{p["panel"]}"/>')

    # caller
    caller_y = axis - 60
    add(f'<rect class="card" x="36" y="{caller_y:.0f}" width="112" height="120" rx="8"/>')
    head, *rest = spec["caller"]
    add(f'<text class="label" x="92" y="{caller_y + 46:.0f}" text-anchor="middle">{escape(head)}</text>')
    for i, line in enumerate(rest):
        add(
            f'<text class="small" x="92" y="{caller_y + 66 + i * 18:.0f}" '
            f"text-anchor=\"middle\">{escape(line)}</text>"
        )

    top = axis - stack_h / 2

    if not hosts:
        # Chapters that publish nothing still need the column, because the point
        # being made is that it is empty at this stage.
        add(
            f'<rect x="{CARD_X}" y="{top:.0f}" width="{CARD_W}" height="{CARD_H}" rx="8" '
            f'fill="none" stroke="{p["edge"]}" stroke-width="1.5" stroke-dasharray="6 5"/>'
        )
        add(
            f'<text class="small" x="{CARD_X + CARD_W / 2:.0f}" y="{top + 26:.0f}" '
            f'text-anchor="middle">{escape(spec.get("empty", "no hostname yet"))}</text>'
        )
        add(
            f'<text class="small" x="{CARD_X + CARD_W / 2:.0f}" y="{top + 44:.0f}" '
            f'text-anchor="middle">reachable on loopback only</text>'
        )

    for i, host in enumerate(hosts):
        name, auth = host[0], host[1]
        tag = host[2] if len(host) > 2 else None
        y = top + i * (CARD_H + CARD_GAP)
        add(f'<rect class="card" x="{CARD_X}" y="{y:.0f}" width="{CARD_W}" height="{CARD_H}" rx="8"/>')
        add(f'<rect x="{CARD_X}" y="{y:.0f}" width="6" height="{CARD_H}" rx="3" fill="{p[auth]}"/>')
        add(f'<text class="mono" x="{CARD_X + 22}" y="{y + 26:.0f}">{escape(name)}</text>')
        add(f'<text class="small" x="{CARD_X + 22}" y="{y + 46:.0f}">{escape(AUTH_LABEL[auth])}</text>')
        if tag:
            add(
                f'<text class="small" x="{CARD_X + CARD_W - 14}" y="{y + 46:.0f}" '
                f'text-anchor="end">{escape(tag)}</text>'
            )

        stroke = p["flow_open"] if auth == OPEN else p["flow_closed"]
        dash = "" if auth == OPEN else ' stroke-dasharray="5 4"'
        y1 = caller_y + 60 + (i - (len(hosts) - 1) / 2) * 8
        y2 = y + CARD_H / 2
        add(
            f'<path d="M148 {y1:.0f} C 200 {y1:.0f}, 200 {y2:.0f}, {CARD_X} {y2:.0f}" '
            f'fill="none" stroke="{stroke}" stroke-width="2"{dash}/>'
        )

    def machine(y: float, title: str, ports: list, notes: list) -> None:
        h = panel_h(ports, notes)
        add(
            f'<rect class="card" x="{MACHINE_X}" y="{y:.0f}" width="{MACHINE_W}" '
            f'height="{h}" rx="8"/>'
        )
        add(
            f'<path d="M{MACHINE_X + 8} {y:.0f} h{MACHINE_W - 16} a8 8 0 0 1 8 8 v22 '
            f'h-{MACHINE_W} v-22 a8 8 0 0 1 8 -8 z" fill="{p["machine"]}"/>'
        )
        add(f'<text class="head" x="{MACHINE_X + 20}" y="{y + 20:.0f}">{escape(title)}</text>')

        row = y + 60
        for port, what in ports:
            add(f'<text class="monoxs" x="{MACHINE_X + 20}" y="{row:.0f}">{escape(port)}</text>')
            add(f'<text class="monoxs" x="{MACHINE_X + COL2}" y="{row:.0f}">{escape(what)}</text>')
            row += 26

        if notes:
            row += 6
            add(
                f'<line x1="{MACHINE_X + 20}" y1="{row - 18:.0f}" x2="{MACHINE_X + MACHINE_W - 20}" '
                f'y2="{row - 18:.0f}" stroke="{p["rule"]}" stroke-width="1.5"/>'
            )
            for note in notes:
                add(f'<text class="small" x="{MACHINE_X + 20}" y="{row:.0f}">{escape(note)}</text>')
                row += 26

    machine(my, spec["machine"], spec["ports"], spec["notes"])

    if second:
        y2 = my + h1 + PANEL_GAP
        machine(y2, second["title"], second["ports"], second.get("notes", []))
        add(
            f'<path d="M{MACHINE_X + MACHINE_W / 2:.0f} {my + h1:.0f} V{y2:.0f}" fill="none" '
            f'stroke="{p["ink"]}" stroke-width="2" stroke-dasharray="5 4"/>'
        )
        add(
            f'<text class="small" x="{MACHINE_X + MACHINE_W / 2 + 10:.0f}" '
            f'y="{my + h1 + PANEL_GAP / 2 + 4:.0f}">{escape(second["link"])}</text>'
        )

    # the outbound connection, drawn from the machine towards the hostnames,
    # because the direction the connection is opened in is the whole point
    if hosts:
        add(
            f'<path d="M{MACHINE_X} {axis:.0f} H{CARD_X + CARD_W + 12}" fill="none" '
            f'stroke="{p["ink"]}" stroke-width="2.5"/>'
        )
        add(
            f'<text class="small" x="{(MACHINE_X + CARD_X + CARD_W) / 2:.0f}" y="{axis - 10:.0f}" '
            f'text-anchor="middle">outbound 443</text>'
        )
    else:
        add(
            f'<path d="M{MACHINE_X} {axis:.0f} H{CARD_X + CARD_W + 12}" fill="none" '
            f'stroke="{p["flow_closed"]}" stroke-width="2" stroke-dasharray="6 5"/>'
        )

    if outbound:
        oy = content_bottom + 44
        add(
            f'<rect class="card" x="{CARD_X}" y="{oy:.0f}" width="{CARD_W + 120}" '
            f'height="{OUT_H}" rx="8"/>'
        )
        add(f'<text class="label" x="{CARD_X + 20}" y="{oy + 26:.0f}">{escape(outbound["title"])}</text>')
        add(f'<text class="small" x="{CARD_X + 20}" y="{oy + 48:.0f}">{escape(outbound["sub"])}</text>')
        add(
            f'<path d="M{MACHINE_X + 40} {my + machines_h:.0f} V{oy + OUT_H / 2:.0f} '
            f'H{CARD_X + CARD_W + 120}" fill="none" stroke="{p["ink"]}" stroke-width="2"/>'
        )
        add(
            f'<text class="small" x="{MACHINE_X + 52}" y="{oy + OUT_H / 2 - 10:.0f}">'
            f'{escape(outbound["label"])}</text>'
        )

    add("</svg>")
    return "\n".join(parts) + "\n"


ALT = {
    "start-here": (
        "A phone on cellular reaches hello-world.<org>.edgible.com, which is open to "
        "anyone. It arrives at one machine you own, where Hello World is bound to "
        "127.0.0.1:8080 and the serving agent holds an outbound connection on 443, so "
        "the router has no forwarded port."
    ),
    "website-on-edgible": (
        "A phone on cellular reaches four hostnames. The site and the Umami tracking "
        "script are open to anyone; the Umami dashboard and the Uptime Kuma status page "
        "need an org login. All four arrive at one machine you own, whose nginx, Umami "
        "and Uptime Kuma containers are bound to loopback, with no forwarded port."
    ),
    "n8n-on-edgible": (
        "A phone, and services like GitHub and Stripe, reach two hostnames. The n8n "
        "editor needs an org login; the webhook hostname is open to anyone. Both arrive "
        "at one n8n process bound to 127.0.0.1:5678 on a machine you own, with no "
        "forwarded port."
    ),
    "openclaw-on-edgible": (
        "A phone on cellular, with no VPN, reaches openclaw-ui.<org>.edgible.com behind "
        "an org login. It arrives at the OpenClaw Gateway bound to 127.0.0.1:18789 on a "
        "machine you own, so the agent's shell and admin console are never exposed and "
        "the router has no forwarded port."
    ),
    "llm-on-edgible": (
        "An n8n VM and an OpenClaw VM on other machines call "
        "ollama.<org>.edgible.com with a bearer key. It arrives at Ollama on the Mac, "
        "bound to 127.0.0.1:11434 and reached through a forwarder on the guest, so the "
        "model weights and the GPU stay home and the router has no forwarded port."
    ),
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    written = 0
    specs = {name: {**spec, "alt": ALT[name]} for name, spec in SERIES.items()}
    specs.update(CHAPTERS)

    problems = [p for name, spec in specs.items() for p in check(name, spec)]
    if problems:
        print("\n".join(problems))
        return 1

    for name, spec in specs.items():
        for scheme, palette in PALETTES.items():
            path = OUT / f"{name}-{scheme}.svg"
            path.write_text(svg_for(spec, palette), encoding="utf-8")
            written += 1
    print(f"wrote {written} diagrams to {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
