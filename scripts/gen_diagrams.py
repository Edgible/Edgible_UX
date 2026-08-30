#!/usr/bin/env python3
"""Draw the topology diagram that opens each series index.

Every series makes the same shape of claim: some caller out on the internet
reaches one or more published hostnames, each with its own auth mode, and all of
them arrive at one machine whose services are bound to loopback behind a router
with nothing forwarded. So the diagrams are generated from a short spec rather
than drawn by hand, which keeps five pictures saying the same thing the same
way, and makes a palette or wording change one edit instead of five.

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
        "panel": "#f4f5f7",
        "card": "#ffffff",
        "edge": "#c9cdd8",
        "rule": "#e0e3ea",
        "ink": "#000033",
        "muted": "#4a4f66",
        "machine": "#000033",
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
        "machine": "#0b0b22",
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
            "serving agent, outbound 443 only",
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

WIDTH = 960
CARD_H = 58
CARD_GAP = 18
CARD_X = 250
CARD_W = 250
MACHINE_X = 612
MACHINE_W = 312
PAD = 40


def svg_for(spec: dict, palette: dict) -> str:
    p = palette
    hosts = spec["hosts"]
    stack_h = len(hosts) * CARD_H + (len(hosts) - 1) * CARD_GAP
    machine_h = 96 + 26 * (len(spec["ports"]) + len(spec["notes"]))
    height = max(stack_h, machine_h) + PAD * 2
    mid = height / 2

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
    caller_y = mid - 60
    add(f'<rect class="card" x="36" y="{caller_y:.0f}" width="112" height="120" rx="8"/>')
    head, *rest = spec["caller"]
    add(f'<text class="label" x="92" y="{caller_y + 46:.0f}" text-anchor="middle">{escape(head)}</text>')
    for i, line in enumerate(rest):
        add(
            f'<text class="small" x="92" y="{caller_y + 66 + i * 18:.0f}" '
            f"text-anchor=\"middle\">{escape(line)}</text>"
        )

    # published hostnames
    top = mid - stack_h / 2
    for i, (host, auth) in enumerate(hosts):
        y = top + i * (CARD_H + CARD_GAP)
        add(f'<rect class="card" x="{CARD_X}" y="{y:.0f}" width="{CARD_W}" height="{CARD_H}" rx="8"/>')
        add(f'<rect x="{CARD_X}" y="{y:.0f}" width="6" height="{CARD_H}" rx="3" fill="{p[auth]}"/>')
        add(f'<text class="mono" x="{CARD_X + 22}" y="{y + 26:.0f}">{escape(host)}</text>')
        add(f'<text class="small" x="{CARD_X + 22}" y="{y + 46:.0f}">{escape(AUTH_LABEL[auth])}</text>')

        stroke = p["flow_open"] if auth == OPEN else p["flow_closed"]
        dash = "" if auth == OPEN else ' stroke-dasharray="5 4"'
        y1 = caller_y + 60 + (i - (len(hosts) - 1) / 2) * 8
        y2 = y + CARD_H / 2
        add(
            f'<path d="M148 {y1:.0f} C 200 {y1:.0f}, 200 {y2:.0f}, {CARD_X} {y2:.0f}" '
            f'fill="none" stroke="{stroke}" stroke-width="2"{dash}/>'
        )

    # the machine
    my = mid - machine_h / 2
    add(
        f'<rect class="card" x="{MACHINE_X}" y="{my:.0f}" width="{MACHINE_W}" '
        f'height="{machine_h}" rx="8"/>'
    )
    add(
        f'<path d="M{MACHINE_X + 8} {my:.0f} h{MACHINE_W - 16} a8 8 0 0 1 8 8 v22 '
        f'h-{MACHINE_W} v-22 a8 8 0 0 1 8 -8 z" fill="{p["machine"]}"/>'
    )
    add(f'<text class="head" x="{MACHINE_X + 20}" y="{my + 20:.0f}">{escape(spec["machine"])}</text>')

    row = my + 60
    for port, what in spec["ports"]:
        add(f'<text class="monoxs" x="{MACHINE_X + 20}" y="{row:.0f}">{escape(port)}</text>')
        add(f'<text class="monoxs" x="{MACHINE_X + 150}" y="{row:.0f}">{escape(what)}</text>')
        row += 26

    row += 6
    add(
        f'<line x1="{MACHINE_X + 20}" y1="{row - 18:.0f}" x2="{MACHINE_X + MACHINE_W - 20}" '
        f'y2="{row - 18:.0f}" stroke="{p["rule"]}" stroke-width="1.5"/>'
    )
    for note in spec["notes"]:
        add(f'<text class="small" x="{MACHINE_X + 20}" y="{row:.0f}">{escape(note)}</text>')
        row += 26

    # the outbound connection, drawn from the machine towards the hostnames
    add(
        f'<path d="M{MACHINE_X} {mid:.0f} H{CARD_X + CARD_W + 12}" fill="none" '
        f'stroke="{p["ink"]}" stroke-width="2.5"/>'
    )
    add(
        f'<text class="small" x="{(MACHINE_X + CARD_X + CARD_W) / 2:.0f}" y="{mid - 10:.0f}" '
        f'text-anchor="middle">dials out on 443</text>'
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
    for name, spec in SERIES.items():
        spec = {**spec, "alt": ALT[name]}
        for scheme, palette in PALETTES.items():
            path = OUT / f"{name}-{scheme}.svg"
            path.write_text(svg_for(spec, palette), encoding="utf-8")
            written += 1
    print(f"wrote {written} diagrams to {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
