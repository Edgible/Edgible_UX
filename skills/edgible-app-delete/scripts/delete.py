#!/usr/bin/env python3
"""Delete an Edgible application by name. Does not stop Docker or delete files."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys

NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$")


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


def find_app_by_name(name: str) -> dict | None:
    proc = run_edgible(["app", "list", "--json"])
    payload = load_json(proc)
    apps = payload.get("applications") or payload.get("apps") or []
    matches = [app for app in apps if app.get("name") == name]
    if len(matches) > 1:
        ids = ", ".join(str(a.get("id")) for a in matches)
        die(f"Several apps named {name!r}. Pass --app-id. IDs: {ids}")
    return matches[0] if matches else None


def main() -> None:
    parser = argparse.ArgumentParser(description="Delete an Edgible application by name.")
    parser.add_argument("--name", help="Application name (DNS label)")
    parser.add_argument("--app-id", help="Application id (overrides --name)")
    args = parser.parse_args()

    require_edgible()
    log("edgible-app-delete: starting")

    app_id = (args.app_id or "").strip() or None
    name = (args.name or "").strip().lower() or None

    if app_id:
        log(f"edgible-app-delete: deleting id {app_id}")
        run_edgible(["app", "delete", "--app-id", app_id, "--force", "--non-interactive"])
        print(f"APP_ID={app_id}", flush=True)
        print("STATUS=deleted", flush=True)
        return

    if not name:
        die("Pass --name or --app-id")
    if not NAME_RE.match(name):
        die("--name must be a lowercase DNS label (letters, digits, hyphens).")

    existing = find_app_by_name(name)
    if not existing:
        print(f"No Edgible app named {name}.", flush=True)
        print(f"NAME={name}", flush=True)
        print("STATUS=missing", flush=True)
        return

    app_id = str(existing["id"])
    log(f"edgible-app-delete: deleting {name} ({app_id})")
    run_edgible(["app", "delete", "--name", name, "--force", "--non-interactive"])
    print(f"NAME={name}", flush=True)
    print(f"APP_ID={app_id}", flush=True)
    print("STATUS=deleted", flush=True)


if __name__ == "__main__":
    main()
