#!/usr/bin/env python3
"""Create or reuse an Edgible app for a local listening port. Print the https URL."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time

NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$")
ALLOWED_AUTH = {"none", "org", "api-key"}
ORG_ONLY_PORTS = {18789}
POLL_SECONDS = 5
POLL_ATTEMPTS = 18  # ~90s, matches first-publish cert wait in the getting-started guide


def log(msg: str) -> None:
    print(msg, flush=True)


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr, flush=True)
    raise SystemExit(code)


def run_edgible(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    cmd = ["edgible", *args]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if check and proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip() or f"exit {proc.returncode}"
        die(f"$ {' '.join(cmd)}\n{err}", proc.returncode or 1)
    return proc


def load_json(proc: subprocess.CompletedProcess[str]) -> dict:
    text = (proc.stdout or "").strip()
    if not text:
        die("edgible produced no JSON (are you logged in? `edgible auth login`)")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        die(f"Could not parse edgible JSON: {exc}\n{text[:500]}")


def parse_auth(raw: str) -> str:
    parts = [p.strip().lower() for p in raw.split(",") if p.strip()]
    if not parts:
        die("--auth-modes is empty")
    unknown = [p for p in parts if p not in ALLOWED_AUTH]
    if unknown:
        die(f"Unknown auth mode(s): {', '.join(unknown)}. Use none, org, and/or api-key.")
    # Keep a stable order: org, api-key, none
    order = ["org", "api-key", "none"]
    ordered = [m for m in order if m in parts]
    return ",".join(ordered)


def require_edgible() -> None:
    if not shutil.which("edgible"):
        die("edgible is not on PATH. Install and `edgible auth login` on this machine first.")


def pick_device(device_id: str | None, device_name: str | None) -> tuple[str, str]:
    proc = run_edgible(["device", "list", "--type", "serving", "--json"])
    devices = load_json(proc).get("devices") or []
    if not devices:
        die("No serving devices in this org. Register the Edgible agent first.")

    if device_id:
        for d in devices:
            if d.get("id") == device_id:
                return str(d["id"]), str(d.get("name") or d["id"])
        die(f"No serving device with id {device_id}")

    if device_name:
        matches = [d for d in devices if d.get("name") == device_name]
        if len(matches) != 1:
            names = ", ".join(d.get("name") or d.get("id") for d in devices)
            die(f"Serving device {device_name!r} not found. Known: {names}")
        d = matches[0]
        return str(d["id"]), str(d.get("name") or d["id"])

    if len(devices) == 1:
        d = devices[0]
        return str(d["id"]), str(d.get("name") or d["id"])

    names = ", ".join(f"{d.get('name')} ({d.get('id')})" for d in devices)
    retries = "\n".join(
        f"  --device-name {d.get('name')}" for d in devices if d.get("name")
    )
    die(
        "Several serving devices. Pass --device-name for *this* machine "
        f"(the VM you are on, not AWS).\nKnown: {names}\nRetry with one of:\n{retries}"
    )


def find_app_by_name(name: str) -> dict | None:
    proc = run_edgible(["app", "list", "--json"])
    payload = load_json(proc)
    apps = payload.get("applications") or payload.get("apps") or []
    for app in apps:
        if app.get("name") == name:
            return app
    return None


def app_url(app_id: str) -> str:
    proc = run_edgible(["app", "get", "--app-id", app_id, "--json"])
    data = load_json(proc)
    return str(data.get("url") or "").strip()


def wait_for_url(app_id: str) -> str:
    url = ""
    for _ in range(POLL_ATTEMPTS):
        url = app_url(app_id)
        if url.startswith("https://"):
            return url.rstrip("/")
        time.sleep(POLL_SECONDS)
    extra = f" last value: {url}" if url else ""
    die(
        "Certificate/URL not ready after ~90s. Check Certificates in "
        f"https://app.prod.edgible.com/ then `edgible app get --app-id {app_id}`.{extra}"
    )


def create_app(name: str, port: int, auth: str, device_id: str) -> None:
    args = [
        "app",
        "create",
        "existing",
        "--non-interactive",
        "--name",
        name,
        "--port",
        str(port),
        "--protocol",
        "http",
        "--https-upgrade",
        "--auth-modes",
        auth,
        "--device-id",
        device_id,
    ]
    run_edgible(args)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Publish a local port through Edgible (existing workload)."
    )
    parser.add_argument("--name", required=True, help="Application name (DNS label)")
    parser.add_argument("--port", required=True, type=int, help="Local TCP port already listening")
    parser.add_argument(
        "--auth-modes",
        required=True,
        help="none (public), org (sign-in), api-key, or comma-separated",
    )
    parser.add_argument("--device-id", help="Serving device id")
    parser.add_argument("--device-name", help="Serving device name (this machine)")
    args = parser.parse_args()

    require_edgible()
    log("edgible-app-create: starting")

    name = args.name.strip().lower()
    if not NAME_RE.match(name):
        die("--name must be a lowercase DNS label (letters, digits, hyphens).")

    port = args.port
    if port < 1 or port > 65535:
        die("--port must be 1–65535")

    auth = parse_auth(args.auth_modes)
    modes = set(auth.split(","))
    if port in ORG_ONLY_PORTS and "none" in modes:
        die(
            f"Port {port} is OpenClaw Control UI. Use --auth-modes org "
            "(never none / public)."
        )

    device_id, device_name = pick_device(args.device_id, args.device_name)
    log(f"edgible-app-create: device {device_name} ({device_id})")
    health = run_edgible(["device", "health", "--name", device_name], check=False)
    if health.returncode != 0:
        die(
            f"Device {device_name!r} is not healthy.\n"
            f"{(health.stderr or health.stdout or '').strip()}"
        )

    existing = find_app_by_name(name)
    if existing:
        log(f"edgible-app-create: app {name} already exists, waiting for URL")
        app_id = str(existing["id"])
        url = wait_for_url(app_id)
        print(f"Already published as {name} (auth unchanged here).", flush=True)
        print(f"URL={url}", flush=True)
        print(f"AUTH={auth}", flush=True)
        print(f"DEVICE={device_name}", flush=True)
        print(f"PORT={port}", flush=True)
        print(f"APP_ID={app_id}", flush=True)
        print("STATUS=existing", flush=True)
        return

    log(f"edgible-app-create: creating {name} on port {port} ({auth})")
    create_app(name, port, auth, device_id)
    log("edgible-app-create: create returned, waiting for https URL (up to ~90s)")
    created = find_app_by_name(name)
    if not created:
        die("Create appeared to succeed but the app is not in `edgible app list`.")
    app_id = str(created["id"])
    url = wait_for_url(app_id)
    print(f"Published {name} on port {port} ({auth}) via {device_name}.", flush=True)
    print(f"URL={url}", flush=True)
    print(f"AUTH={auth}", flush=True)
    print(f"DEVICE={device_name}", flush=True)
    print(f"PORT={port}", flush=True)
    print(f"APP_ID={app_id}", flush=True)
    print("STATUS=created", flush=True)


if __name__ == "__main__":
    main()
