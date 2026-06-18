# C&RBGC Notes Walkthrough

_2026-06-17T03:02:44Z by Showboat 0.6.1_

<!-- showboat-id: bfc22c39-97c8-4f5f-bdf5-29c6945b9926 -->

## Overview

This repository is **not a code project** — it's a [Flowershow](https://flowershow.app)
digital garden: a vault of golf-history essays and notes that publishes to
<https://crbgc-philoserf.flowershow.me>. The "source" being walked through here is the
small layer of configuration and conventions that turn a flat folder of Markdown into a
coherent, navigable website.

Three things define how the repo works:

1. **Content** — flat Markdown notes at the repo root, each with YAML frontmatter and
   `[[wikilinks]]` between them.
2. **Site config** — `config.json` (nav, footer, theme) tells Flowershow how to render the
   vault. The look is the stock `letterpress` theme; an earlier `custom.css` override was
   removed.
3. **Publish model** — publishing is done **manually from inside Obsidian** via the
   Flowershow plugin. `git push` stores history but does **not** deploy. What publishes is
   governed by the plugin's `excludePatterns`.

GitHub is the system of record for history; Flowershow is the renderer.

## Architecture: a flat vault of notes

There are no subdirectories of content — every note lives at the repo root. The structure
is conceptual, not filesystem-based: a set of index hub pages each gather a topic's notes
via wikilinks. Hubs are no longer marked by a filename prefix; they are the notes carrying
the `index` tag. Below are the non-Markdown root files and the index hubs.

```bash
ls -1 | grep -vE "^\.|\.md$"; echo "--- index hubs (index tag) ---"; grep -lE "^  - index$" *.md | grep -v "^_" | sort
```

```output
biome.json
config.json
Taskfile.yml
--- index hubs (index tag) ---
Course Architecture.md
Courses to Play.md
Game Philosophy.md
Hickory Era.md
History.md
Rules of Golf Editions.md
Solo Golf.md
```

Seven hubs carry the topic structure. Not all of them sit in the navbar — `Solo Golf` is a
hub reachable from the home page and cross-links but deliberately kept out of `config.json`
nav, which is a curated, ordered subset rather than the full set.

## Site configuration — `config.json`

Flowershow reads `config.json` for the site title, navigation, footer, and theme. The nav
is a hand-picked, ordered list of hub links — adding a topic to the navbar means a new entry
here, but a hub can exist without one. The theme is `letterpress`, locked to light mode
(`showModeSwitch: false`); there is no `custom.css`.

```bash
sed -n "/\"nav\"/,/]/p" config.json
```

```output
  "nav": {
    "title": "C&RBGC Notes",
    "links": [
      { "href": "/Game Philosophy", "name": "Game Philosophy" },
      { "href": "/History", "name": "History" },
      { "href": "/Hickory Era", "name": "Hickory Era" },
      { "href": "/Rules of Golf Editions", "name": "Rules of Golf" },
      { "href": "/Course Architecture", "name": "Course Architecture" },
      { "href": "/Courses to Play", "name": "Courses to Play" }
    ]
```

## Content model — frontmatter

Every note opens with YAML frontmatter in a fixed six-key order — `title`, `description`,
`tags` (alphabetized), `created`, `date`, `lastmod` — normalized by the Obsidian Linter on
each edit. (An earlier state of the repo carried only `title` + `date`; a curation pass
brought the corpus up to the documented shape, so match the full shape in new notes.) A
representative header:

```bash
awk 'f<2{print} /^---$/{f++}' "Hickory Era American Golf.md"
```

```output
---
title: Hickory Era American Golf
description: History of American golf from the 1880s to 1935, covering key figures, clubs, tournaments, and equipment of the hickory shaft era.
tags:
  - american-golf
  - golden-age-golf
  - golf-equipment
  - golf-history
  - hickory-golf
created: 2026-06-01
date: 2026-05-24
lastmod: 2026-06-10
---
```

## Index hubs and wikilinks

An index hub is a short intro paragraph followed by a list of `[[wikilinks]]` to the notes
in its topic, plus the `index` tag in its frontmatter. This is the only structure tying the
flat vault together: nav points to a hub, the hub points to the notes. A new note should be
linked from its relevant hub, or it becomes an orphan reachable only by URL.

```bash
cat "Hickory Era.md"
```

```output
---
title: Hickory Era
description: Index of notes covering hickory-shaft golf (1830s–1920s), including clubs, rules, history, and modern play.
tags:
  - golf-history
  - hickory-golf
  - index
  - vintage-golf
created: 2026-06-01
date: 2026-05-26
lastmod: 2026-06-12
---

Notes on the hickory-shaft era of golf—roughly 1830s through the late 1920s—and getting started playing it today.

- [[Hickory Golf Starter Guide]]
- [[Hickory Era Golf Club Names]]
- [[Hickory Era American Golf]]
- [[Hickory Golf Resources Directory]]
- [[Golf Rules History 1830s to Hickory Era]]
- [[Colonel Bogey and the Bogey Competition]]
- [[Golf's Transition from Hickory to Steel Shafts]]
- [[Hickory Era Golf Writing Survey]]
- [[Society of Hickory Golfers Overview]]
- [[Roger Hill Hickory Golf Profile]]
- [[Tad Moore Hickory Golf Clubs]]
```

## Tooling — `Taskfile.yml` + `.prettierignore`

The toolchain is Prettier (installed globally), driven by Task. `task fmt` formats all
Markdown; `task check` depends on it. Prettier reads `.prettierignore` to skip per-machine
editor state (`.obsidian/`) and the Task cache (`.task/`). A leftover `biome.json` still
sits at the root but targets the now-removed `custom.css`, so it is effectively vestigial.

> This file is a showboat document — every fenced block is re-runnable and checked with
> `uvx showboat verify`. It is intentionally **not** excluded from Prettier: `task fmt`
> lightly restyles the prose (emphasis markers, blank lines) but leaves the command and
> output fences untouched, so verification still passes. Don't hand-edit the output blocks;
> regenerate the doc or re-run `showboat verify --output` instead.

```bash
cat Taskfile.yml; echo "--- .prettierignore ---"; cat .prettierignore
```

```output
version: "3"

tasks:
  default:
    silent: true
    cmds:
      - task --list

  fmt:
    desc: Format markdown with prettier
    cmds:
      - prettier --list-different --ignore-unknown --write .

  check:
    desc: Run all formatting checks
    deps: [fmt]
--- .prettierignore ---
.obsidian/
.task/
```

## The publish model — Obsidian plugin, not git

This is the load-bearing part of the repo. Publishing happens **from inside Obsidian** via
the Flowershow plugin; `git push` only records history. The plugin config lives at
`.obsidian/plugins/flowershow/data.json` — **gitignored** because it holds an auth token.

The vault is **public by default**: anything not matched by `excludePatterns` (regex on
vault-relative paths) publishes. That's why scratch/working files must never sit at the root
unprefixed — and why this walkthrough is named `_walkthrough.md`, matching the `^_` pattern
so it stays unpublished. The list also pins out `CLAUDE.md` and the verbatim consolidated
`Rules of Golf.md`.

> Do **not** publish with the `fl` CLI — it ignores this exclude list and would upload
> everything outside `.gitignore`.

```bash
grep -A6 "\"excludePatterns\"" .obsidian/plugins/flowershow/data.json
```

```output
  "excludePatterns": [
    "^CLAUDE\\.md$",
    "^Rules of Golf\\.md$",
    "^_",
    "^Drafts/",
    "^Private/"
  ],
```

## Licensing — a footer link, no in-repo files

There are no license files in the repo (an earlier `LICENSE`/`CONTENT-LICENSE.md` pair was
removed). Prose and media are offered under CC BY-NC-SA 4.0 via a footer link in
`config.json` that points at the canonical creativecommons.org deed; code and config carry
no explicit license.

```bash
grep -A1 "CC BY-NC-SA 4.0" config.json
```

```output
            "name": "CC BY-NC-SA 4.0",
            "href": "https://creativecommons.org/licenses/by-nc-sa/4.0/"
```

## Editorial boundary with the club site

One structural fact lives outside this repo: the club's **governance** site (bylaws,
minutes, notices, news) is a separate sibling repo, `../crbgc/`
([philoserf/crbgc](https://github.com/philoserf/crbgc)), which publishes via Hugo to
<https://crbgc.org>. This repo is the **personal/editorial** side — essays, history surveys,
architecture writing. Keep the split clean: prose and notes here, official records there.

### Recap of the data flow

An Obsidian edit triggers the Linter (frontmatter normalized), then splits two ways: `git
commit` records history only, while the Flowershow plugin publish runs the `excludePatterns`
filter and renders the survivors through `config.json` to the live site. The index hubs are
the spine that ties it together — `config.json` nav points at a hub, which points via
`[[wikilinks]]` at the individual notes.
