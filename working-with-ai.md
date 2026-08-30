# Working with an AI tool

These guides are published so that a coding agent or a chat assistant can read them as easily as you can. Everything below is served from this site, needs no account, and is free to fetch.

## The markdown source of any page

Every page is served twice: as HTML for reading, and as markdown at the same path with `.md` on the end. The markdown is the source these pages are written in, so an assistant reading it gets the commands and the checklists without the navigation and styling wrapped around them.

```bash
curl https://guides.edgible.com/capabilities.md
curl https://guides.edgible.com/guides/n8n-on-edgible/03-n8n-webhook-door.md
```

At the top of each page there are two actions next to the edit pencil. One copies that page's markdown to your clipboard, ready to paste into a chat. The other opens the markdown in the browser.

## The whole site in one fetch

`llms.txt` is an index. It lists every page as a link to its raw markdown, each with a one-line summary, so an agent can pick what it needs rather than crawling the site.

```bash
curl https://guides.edgible.com/llms.txt
```

`llms-full.txt` is every page concatenated into a single document, about 200 KB, for a tool that would rather take the corpus in one go than fetch pages individually.

```bash
curl https://guides.edgible.com/llms-full.txt
```

## Terms in one place

[Glossary](glossary.md) defines every term the guides use, so an assistant can pick up the vocabulary in one fetch rather than inferring it chapter by chapter:

```bash
curl https://guides.edgible.com/glossary.md
```

## Ways people use this

Point an assistant at `llms.txt` and ask which chapter covers what you are trying to do. The summaries are written to make that question answerable without opening every page.

Paste a single chapter into a chat and work through it with the assistant watching the output. Each chapter states what you should have when you finish and ends with a checklist, so an assistant has something concrete to compare your terminal output against.

Give a coding agent the markdown for a chapter and have it adapt the commands to your machine names, ports and organisation, rather than you editing each command by hand.

Ask a question against the whole corpus by fetching `llms-full.txt`, when you do not yet know which guide the answer is in.

## How current a page is

Every page carries the date its source last changed: at the foot of the HTML, and in the first two lines of the markdown, alongside the page's canonical URL.

```
Source: https://guides.edgible.com/guides/n8n-on-edgible/01-n8n-on-the-vm.md
Last updated: 2026-08-28
```

Those two lines travel with the text when it is pasted into a chat, which is what lets an assistant cite the page and lets you work out later which version you followed. The date comes from the commit history of [the repository](https://github.com/Edgible/Edgible_UX), not from a field anyone maintains by hand. A page dated some months ago is not necessarily wrong, but it is worth checking a version number or a command flag against the tool you are running.

## Crawling

`robots.txt` allows everything, for search engines and answer engines alike. This is public documentation, and being quoted accurately is the point. `sitemap.xml` lists every page.

## What to keep an eye on

An assistant that has read these guides will happily produce commands for your machines. The guides publish services and change what is reachable from the public internet, so read a command before you run it, particularly anything that creates an app with `None` auth or changes what a service binds to.

Assistants also blend sources. If an answer mentions an Edgible flag or a command that does not appear in any chapter here, treat it as invented until you have seen it in the [CLI](https://github.com/Edgible) itself.
