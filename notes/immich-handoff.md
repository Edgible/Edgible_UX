# Immich guide: where we got to

Working notes for the `guide/immich-on-edgible` branch. Not part of the published
site: `scripts/build.sh` stages named files, and `notes/` is not one of them.
Delete this file before merging to `main`.

## The idea

A new series, "Immich on Edgible": a self-hosted photo library replacing Google
Photos, published behind a hostname so the phone app can back up to it from
anywhere. Chosen over the other candidates (Home Assistant, Vaultwarden, a mail
server) because the pain is one most people already feel monthly, and the
migration is a one-evening trial rather than a hardware project.

Candidate theme, in the style of the existing series: *your photos, on your own
disk*. The other series read as the joy of self hosting (website), private AI
(LLM), on-trend relevance (OpenClaw), back office workhorse (n8n).

Rejected for now, with reasons worth keeping:

- **Mail server.** Receiving mail needs inbound port 25 and an MX host that
  accepts connections, which is the opposite of what Edgible does, and
  residential IP reputation kills sending. A webmail client behind `org` would
  work, and a local Dovecot fed by `getmail` from Gmail is the interesting
  version, but neither is next.
- **Home Assistant.** Genuinely strong, especially with the reader's Fronius
  solar (local Solar API, no cloud) and Amber spot pricing. Parked because it
  needs inverter setup before anything can be demonstrated.

## What the hardware is

- The guide's machine is a second Ubuntu VM with 8 GB of RAM. Immich wants 6 GB
  minimum, so the 4 GB guest from `start-here` is not enough and the chapter
  will have to say so.
- Photo storage over NFS. **The database cannot go on NFS**: Immich's own
  `.env` says network shares are unsupported for `DB_DATA_LOCATION`, and their
  requirements doc says local SSD, never a network share. So library on the
  share, Postgres on the VM disk.
- Unresolved: library size, and what exports the NFS share (NAS appliance or a
  Linux box). The UID mapping advice depends on the answer.

## Facts already checked against upstream docs

- Listens on `2283`. Official `docker-compose.yml` plus `.env` with
  `UPLOAD_LOCATION`, `DB_DATA_LOCATION`, `DB_PASSWORD`, `TZ`, `IMMICH_VERSION`.
- Storage template engine is **off** by default since 1.92.0. Originals then sit
  in `upload/` under machine-generated names and `library/` stays empty. Turn it
  on *before* importing to get `Year/Year-Month-Day/Filename`, otherwise a
  Storage Template Migration job has to move everything afterwards.
- Originals are never modified, and are ordinary files. Critical folders are
  `library/`, `upload/` and `profile/`. `thumbs/` and `encoded-video/`
  regenerate. Immich writes its own database dumps to `backups/` daily, keeping
  14, and those hold metadata only.
- ML is a separate container: CLIP smart search, facial recognition via
  `insightface`, duplicate detection on CLIP embeddings, and OCR. Accelerators
  are CUDA, ROCm, OpenVINO, ARM NN and RKNN, and the ML container can run on a
  different machine from the library.
- Google Takeout import wants `immich-go`, not Immich's own uploader:
  `immich-go upload from-google-photos --server=http://localhost:2283
  --api-key=... /path/takeout-*.zip`. It reads the JSON sidecars, so dates,
  locations and albums survive; a plain folder upload loses them. It can read
  the archives without unzipping. Album recreation defaults on.
  `--pause-immich-jobs` keeps the ML jobs from fighting the upload.
- Takeout quirks to cover: `-edited` duplicates, Live Photos splitting, a photo
  in three albums appearing three times, and "Storage saver" accounts getting
  back already-recompressed files.
- **No bulk traffic goes through Edgible.** `immich-go` posts to
  `127.0.0.1:2283`, and `rclone` pulls the Takeout from Google Drive straight to
  the VM. The one trap is the phone: the app's automatic endpoint switching
  takes a home SSID with a LAN URL plus the Edgible hostname for elsewhere, so
  the initial camera-roll backup stays on the LAN. It needs location permission
  to read the SSID, the multi-SSID list is buggy upstream, and app 3.0.0 fixed
  stale endpoints after switching.
- Auth mode will be `None`, because the mobile app cannot pass an `org` browser
  login, with Immich's own accounts doing the protecting. That differs from the
  website guide's `None` and the chapter should say why.

## Still to establish, and only by running it

Per `AGENTS.md`, every command is literal and every claim has a check behind it,
so none of the above is publishable until it has been done on the machine:

1. NFS mount options and UID mapping that let the container write. Mount before
   Docker starts, or Immich sees an empty library and fails its `.immich` marker
   check; the advice circulating for that error is to wipe the database, which
   would be a bad thing for a reader to do.
2. Whether Takeout dates land in the files or only in Immich's database.
3. How long the ML pass really takes on this hardware.
4. A restore rehearsal: database dump plus `UPLOAD_LOCATION`, restored from
   scratch, before the guide tells anyone to cancel Google storage.

## Housekeeping

- Chapters have to be added to `nav` in `mkdocs.yml` as they are created, or the
  `--strict` build in the git hooks fails.
- Series diagrams are generated, not drawn: add an entry to `SERIES` and one per
  chapter to `CHAPTERS` in `scripts/gen_diagrams.py`.
- `capabilities.md`, the root `README.md` guide list and `scripts/gen_llms.py`
  all need the new series adding before merge.
- Still open from before this branch: the Uptime Kuma chapter in the website
  series has never been run end to end.
