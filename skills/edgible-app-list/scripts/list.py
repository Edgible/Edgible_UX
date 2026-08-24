#!/usr/bin/env python3
"""List Edgible apps. Default: this serving device (OpenClaw's box). --all = whole org."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys

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


def require_edgible() -> None:
    if not shutil.which("edgible"):
        die("edgible is not on PATH. Install and `edgible auth login` on this machine first.")


def serving_devices() -> list[dict]:
    proc = run_edgible(["device", "list", "--type", "serving", "--json"])
    return load_json(proc).get("devices") or []


def device_id_to_name(devices: list[dict]) -> dict[str, str]:
    return {
        str(d["id"]): str(d.get("name") or d["id"])
        for d in devices
        if d.get("id")
    }


def pick_device(
    device_id: str | None,
    device_name: str | None,
    devices: list[dict],
) -> tuple[str, str]:
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
        "Several serving devices. Default list is apps on *this* OpenClaw box — "
        "pass --device-name (not AWS if you are on the VM).\n"
        f"Known: {names}\nRetry with one of:\n{retries}\n"
        "Or pass --all for every app in the org."
    )


def app_device_ids(app: dict) -> set[str]:
    ids: set[str] = set()
    wid = app.get("workloadId")
    if wid and str(wid) != "unknown":
        ids.add(str(wid))
    cfg = app.get("configuration")
    if isinstance(cfg, dict):
        raw = cfg.get("deviceIds") or cfg.get("deviceId")
        if isinstance(raw, list):
            ids.update(str(x) for x in raw if x)
        elif raw:
            ids.add(str(raw))
    return ids


def app_device_names(app: dict, id_to_name: dict[str, str]) -> str:
    ids = app_device_ids(app)
    names = [id_to_name.get(i, i) for i in sorted(ids)]
    return ",".join(names) if names else "unknown"


def app_url(app_id: str) -> str:
    proc = run_edgible(["app", "get", "--app-id", app_id, "--json"], check=False)
    if proc.returncode != 0:
        return ""
    try:
        data = json.loads((proc.stdout or "").strip() or "{}")
    except json.JSONDecodeError:
        return ""
    return str(data.get("url") or "").strip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="List Edgible apps on this device, or the whole org with --all."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Every app in the org (all serving devices)",
    )
    parser.add_argument("--device-id", help="Serving device id")
    parser.add_argument("--device-name", help="Serving device name (this OpenClaw box)")
    args = parser.parse_args()

    require_edgible()
    log("edgible-app-list: starting")

    devices = serving_devices()
    id_to_name = device_id_to_name(devices)

    proc = run_edgible(["app", "list", "--json"])
    payload = load_json(proc)
    apps = payload.get("applications") or payload.get("apps") or []

    if args.all:
        scope = "org"
        device_name = "*"
        filtered = apps
        log("edgible-app-list: scope org (all devices)")
    else:
        device_id, device_name = pick_device(
            args.device_id, args.device_name, devices
        )
        scope = "device"
        filtered = [a for a in apps if device_id in app_device_ids(a)]
        log(f"edgible-app-list: scope device {device_name} ({device_id})")

    print(f"SCOPE={scope}", flush=True)
    print(f"DEVICE={device_name}", flush=True)
    print(f"COUNT={len(filtered)}", flush=True)
    if not filtered:
        print("STATUS=empty", flush=True)
        return

    for app in filtered:
        name = app.get("name") or ""
        app_id = str(app.get("id") or "")
        port = app.get("port")
        status = app.get("status") or ""
        url = app_url(app_id) if app_id else ""
        app_device = app_device_names(app, id_to_name)
        print(
            f"NAME={name} DEVICE={app_device} PORT={port} STATUS={status} "
            f"URL={url} APP_ID={app_id}",
            flush=True,
        )
    print("STATUS=ok", flush=True)


if __name__ == "__main__":
    main()
