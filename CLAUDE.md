---
title: CLAUDE
description: Instructions for Claude Code on working with a Flowershow digital garden vault, its toolchain, content model, and dual-license setup.
tags:
  - claude-code
  - digital-garden
  - flowershow
  - obsidian
  - repository-setup
created: 2026-06-01
lastmod: 2026-06-11
---

## CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

### What This Repo is

A [Flowershow](https://flowershow.app) digital garden, hosted at <https://crbgc-philoserf.flowershow.me>. GitHub holds the history; publishing to Flowershow is done from inside Obsidian using the Flowershow plugin (config at `.obsidian/plugins/flowershow/data.json`, including `excludePatterns`). `git push` does **not** auto-deploy. Do **not** publish this vault with the `fl` CLI—the CLI ignores the plugin's exclude list and uploads everything outside `.gitignore`.

The vault is public by default: anything not matched by `excludePatterns` publishes. Never park scratch files, session recaps, or working drafts at the vault root—put them in `Drafts/` or `Private/` (both excluded), or keep them out of this repo entirely.

### Related: the Club Site

The club's formal/governance site (bylaws, minutes, notices, news) lives in the sibling repo `../crbgc/` ([philoserf/crbgc](https://github.com/philoserf/crbgc)) and publishes via Hugo to <https://crbgc.org>. This repo (`crbgc-notes/`) is the personal/editorial side—essays, history surveys, course architecture writing. Keep the split clean: prose and notes here, governance and official records there.

### Commands

```bash
task fmt    # prettier --write across all markdown (honors .gitignore + .prettierignore)
task check  # alias for fmt; placeholder for future checks
```

Prettier is the only markdown toolchain—installed globally via Homebrew on this machine. Prettier reads `.gitignore` and `.prettierignore` by default; `.prettierignore` excludes `.obsidian/` (per-machine editor state) and `.task/` (Taskfile cache). `biome.json` covers only `custom.css`. Run `task check` before committing markdown changes.

The directory is also an Obsidian vault (`.obsidian/`), so markdown is typically authored in Obsidian and committed from the same working tree. The Obsidian Linter plugin rewrites files on edit (alphabetizes tags, normalizes heading case and em-dash spacing, escapes literal `$`)—match its output rather than fighting it.

### Content Model

- Every note carries YAML frontmatter with keys in this order: `title`, `description` (one line), `tags` (alphabetized list), `created`, `date`, `lastmod` (dates are `YYYY-MM-DD`; some notes omit `date`). Match the existing shape when adding new pages.
- The vault is flat—all notes at the root. Topic hubs are the index notes carrying the `index` tag (e.g. `History.md`, `Game Philosophy.md`); each links out to its notes with `[[wikilinks]]`, and the primary hubs are listed in `config.json` nav. A new note should be linked from the relevant index. Not every hub is in the nav—`Solo Golf` is reachable via the home page and cross-links rather than the navbar.
- Flowershow renders KaTeX unconditionally, so escape literal `$` in prose.
- No in-repo license files. Prose and media are offered under CC BY-NC-SA 4.0 via the footer link in `config.json`, which points at the canonical creativecommons.org deed. Code and config carry no explicit license.

### Site Configuration

- `config.json`—Flowershow site config: title, nav (one link per primary index hub), footer, theme (`letterpress`, light-only). Adding a topic area means a new index note (tagged `index`) and, if it belongs in the navbar, a nav entry here.
- `custom.css`—theme overrides (green accent, serif body). Formatted/linted by Biome.
- Publish excludes live in the plugin's `excludePatterns` (regex on vault-relative paths): currently `CLAUDE.md`, and anything starting `_`, `Drafts/`, or `Private/`. Anything else in the vault publishes.

### Backlog

The next concrete step for this repo lives in `../NEXT.md` at the workspace root (one row per repo). Read the crbgc-notes row when starting work; update it when that step ships. If no row exists yet, add one.
