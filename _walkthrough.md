# C&RBGC Notes Walkthrough

_2026-06-13T16:00:16Z by Showboat 0.6.1_

<!-- showboat-id: 11261895-5b77-4b0b-a15d-7f28fbf11eb3 -->

## Overview

This repository is **not a code project** — it's a [Flowershow](https://flowershow.app)
digital garden: a vault of golf-history essays and notes that publishes to
<https://crbgc-philoserf.flowershow.me>. The "source" being walked through here is the
small layer of configuration, theming, and conventions that turn a flat folder of
Markdown into a coherent, navigable website.

Three things define how the repo works:

1. **Content** — flat Markdown notes at the repo root, each with YAML frontmatter and
   `[[wikilinks]]` between them.
2. **Site config** — `config.json` (nav, footer, theme) and `custom.css` (look) tell
   Flowershow how to render the vault.
3. **Publish model** — publishing is done **manually from inside Obsidian** via the
   Flowershow plugin. `git push` stores history but does **not** deploy. What publishes
   is governed by the plugin's `excludePatterns`.

GitHub is the system of record for history; Flowershow is the renderer.

## Architecture: a flat vault of notes

There are no subdirectories of content — every note lives at the repo root. The
structure is conceptual, not filesystem-based: a set of `(Index) *.md` hub pages each
gather a topic's notes via wikilinks, and those same index pages are the site's
navigation. Below is the root layout (content notes elided for brevity).

```bash
ls -1 | grep -vE "^\.|\.md$" ; echo "..."; ls -1 "(Index) "*.md
```

```output
biome.json
config.json
custom.css
LICENSE
Taskfile.yml
...
(Index) Course Architecture.md
(Index) Courses to Play.md
(Index) Game Philosophy.md
(Index) Hickory Era.md
(Index) History.md
(Index) Players and Writers.md
(Index) Rules of Golf Editions.md
(Index) Solo Golf.md
```

## Site configuration — `config.json`

Flowershow reads `config.json` for the site title, navigation, footer, and theme. The
key contract: **every `(Index)` page gets one nav link**, so adding a topic area means
both a new `(Index)` page and a new entry here. The theme is `letterpress`, locked to
light mode (`showModeSwitch: false`).

```bash
sed -n "/\"nav\"/,/]/p" config.json
```

```output
  "nav": {
    "title": "C&RBGC Notes",
    "links": [
      { "href": "/(Index) Game Philosophy", "name": "Game Philosophy" },
      { "href": "/(Index) Course Architecture", "name": "Course Architecture" },
      { "href": "/(Index) Courses to Play", "name": "Courses to Play" },
      { "href": "/(Index) Hickory Era", "name": "Hickory Era" },
      { "href": "/(Index) History", "name": "History" },
      { "href": "/(Index) Solo Golf", "name": "Solo Golf" },
      { "href": "/(Index) Rules of Golf Editions", "name": "Rules of Golf" },
      { "href": "/(Index) Players and Writers", "name": "Players and Writers" }
    ]
```

## Content model — frontmatter

Every note opens with YAML frontmatter. In practice the committed shape is minimal —
`title` plus a date — normalized by the Obsidian Linter plugin on each edit. (The repo's
CLAUDE.md documents a fuller intended shape with `description`/`tags`/`lastmod`; match
whatever the neighboring notes already use.) Here is a representative note header:

```bash
sed -n "1,4p" "Hickory Era American Golf.md"
```

```output
---
title: Hickory Era American Golf
date: 2026-05-24
---
```

## Index hubs and wikilinks

An `(Index)` page is just a short intro paragraph followed by a list of `[[wikilinks]]`
to the notes in its topic. This is the only structure tying the flat vault together: nav
points to the index, the index points to the notes. A new note should be linked from its
relevant index, or it becomes an orphan reachable only by URL.

```bash
cat "(Index) Hickory Era.md"
```

```output
---
title: (Index) Hickory Era
date: 2026-05-26
---

Notes on the hickory-shaft era of golf—roughly 1830s through the late 1920s—and getting started playing it today.

- [[Hickory Golf Starter Guide]]
- [[Hickory Era Golf Club Names]]
- [[Hickory Era American Golf]]
- [[Hickory Golf Resources Directory]]
- [[Golf Rules History 1830s to Hickory Era]]
- [[Hickory Era Golf Writing Survey]]
- [[Society of Hickory Golfers Overview]]
- [[Society of Hickory Golfers Origins]]
- [[Tad Moore Hickory Golf Clubs]]
```

## Theming — `custom.css` + `biome.json`

`custom.css` overrides the `letterpress` theme: a club-green accent (`#006747`), a serif
body font, green underlined links, and CSS that hides the default logo image so the
wordmark is text. `biome.json` is scoped to format/lint **only** `custom.css` — it is not
a general project linter. Here are the theme variables that drive the look:

```bash
sed -n "/:root {/,/}/p" custom.css
```

```output
:root {
  --color-l-background: #fafaf7;
  --color-l-foreground: #1a1a1a;
  --color-l-accent: #006747;

  /* Explicit unprefixed aliases so the override rules below resolve even
     if the theme doesn't remap --color-l-* (light-only, set in config.json). */
  --color-accent: #006747;

  --font-body: ui-serif, Georgia, Cambria, "Times New Roman", serif;
  --font-heading:
    ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;

  --font-size-base: 1.0625rem;
  --line-height-normal: 1.6;
  --font-size-h1: calc(var(--font-size-base) * 1.765);
  --font-size-h2: calc(var(--font-size-base) * 1.294);
  --font-size-h3: var(--font-size-base);
}
```

## The publish model — Obsidian plugin, not git

This is the load-bearing part of the repo. Publishing happens **from inside Obsidian**
via the Flowershow plugin; `git push` only records history. The plugin config lives at
`.obsidian/plugins/flowershow/data.json` — which is **gitignored** because it holds an
auth token (redacted below).

The vault is **public by default**: anything not matched by `excludePatterns` (regex on
vault-relative paths) publishes. That's why scratch/working files must never sit at the
root unprefixed — and why this very walkthrough is named `_walkthrough.md`, matching the
`^_` exclude pattern so it stays unpublished.

> Do **not** publish with the `fl` CLI — it ignores this exclude list and would upload
> everything outside `.gitignore`.

```bash
grep -A5 "\"excludePatterns\"" .obsidian/plugins/flowershow/data.json
```

```output
  "excludePatterns": [
    "^CLAUDE\\.md$",
    "^_",
    "^Drafts/",
    "^Private/"
  ],
```

## Tooling — `Taskfile.yml` + `.ignore`

The only toolchain is Prettier (installed globally via Homebrew), driven by Task.
`task fmt` formats all Markdown; `task check` is an alias for it, reserved for future
checks. Prettier reads `.ignore` to skip per-machine editor state (`.obsidian/`) and the
Taskfile cache (`.task/`). **Never** run Prettier on `_walkthrough.md` — showboat owns
its own formatting and Prettier would corrupt the verified output blocks.

```bash
sed -n "/  fmt:/,/write \./p" Taskfile.yml; echo "--- .ignore ---"; cat .ignore
```

```output
  fmt:
    desc: Format markdown with prettier
    cmds:
      - prettier --list-different --ignore-unknown --ignore-path .ignore --write .
--- .ignore ---
.obsidian/
.task/
```

## The two-license split

Licensing is deliberately split and the boundary is load-bearing: `LICENSE` (MIT) covers
code/config/templates, while `CONTENT-LICENSE.md` (CC BY-NC-SA 4.0) covers the prose and
media. Don't merge them or apply one across the other domain. The footer in `config.json`
links the content license; the social link points at the GitHub repo.

```bash
head -1 LICENSE; echo "---"; sed -n "1,6p" CONTENT-LICENSE.md
```

```output
MIT License
---
---
title: CONTENT-LICENSE
---

## Content License

```

## Editorial boundary with the club site

One last structural fact that lives outside this repo: the club's **governance** site
(bylaws, minutes, notices, news) is a separate sibling repo, `../crbgc/`
([philoserf/crbgc](https://github.com/philoserf/crbgc)), which publishes via Hugo to
<https://crbgc.org>. This repo is the **personal/editorial** side — essays, history
surveys, architecture writing. Keep the split clean: prose and notes here, official
records there.

### Recap of the data flow

An Obsidian edit triggers the Linter (frontmatter normalized), then splits two ways:
`git commit` records history only, while the Flowershow plugin publish runs the
`excludePatterns` filter and renders the survivors through `config.json` + `custom.css`
to the live site. The `(Index)` pages are the spine that ties it together — `config.json`
nav points at an `(Index)` hub, which points via `[[wikilinks]]` at the individual notes.
