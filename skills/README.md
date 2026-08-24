# OpenClaw skills (Edgible)

Hyphenated slugs, **`edgible-app-<verb>`**, aligned with `edgible app <verb>`.

| Skill | CLI | Chat words that should still match |
| --- | --- | --- |
| [edgible-app-create](edgible-app-create/) | `edgible app create existing` | publish, put on the internet, give me a URL |
| [edgible-app-list](edgible-app-list/) | `edgible app list` (default: **this** serving device) | what’s published, URLs on this box |
| [edgible-app-delete](edgible-app-delete/) | `edgible app delete` | unpublish, take down, remove |

Avoid `edgible-create` / `edgible-remove`: too vague (org? device? app?). Put “publish” in the **description**, not the folder name — OpenClaw `/skill` uses the frontmatter `name`.

Copy each skill folder onto the Gateway: `~/.openclaw/workspace/skills/<name>/`.
