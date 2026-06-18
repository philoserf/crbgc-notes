# A Theory of crbgc-notes

_A Naur-style account of the understanding needed to modify this system without
damaging its conceptual integrity. Not published (`^_` excluded).\_

## What this system is, in the world it models

This is not a notes app and not, despite appearances, a generic digital garden. It is
**one person's argument about golf, published as a reading-room**. The thesis is explicit
in the corpus once you read it as a whole: that golf has an _original orientation_ —
walking, hickory-era equipment, minimalist classical architecture, the game as fellowship
rather than score — and that this orientation was corrupted by modernization and is now
being recovered. Notes like "Recovering Golf's Original Orientation," "Modernization's
Corruption of Golf," "Golf's Original Constraints," and "Enemies of Golf" are not neutral
encyclopedia entries; they are the load-bearing claims, and the historical surveys (the
hickory era, public-golf history, the Rules editions) are evidence marshalled behind them.
A sibling project — say, a club's general golf wiki — would have the same file types and
the same Flowershow stack and still be a _different system_, because it would lack this
editorial spine. If you flatten this into "a collection of golf notes," you have lost the
theory.

The world being modeled, then, has these entities: **claims** (the argument essays),
**evidence** (historical surveys and, distinctly, _primary-source reference texts_ — the
verbatim Rules of Golf editions from 1744 through the consolidated 2023 code), **topic
hubs**, and a **reading order**. The code's vocabulary maps onto this only partially, and
the gaps are where you'll get hurt.

## The organizing ideas

**The index page is the spine, and it does three jobs at once.** A file like
`Hickory Era.md` — a topic hub, identified by the `index` tag rather than any filename
prefix — is simultaneously (1) a topic hub — a short framing paragraph plus a hand-curated
list of `[[wikilinks]]`; (2) usually a navigation entry, since `config.json`'s nav is a
hand-picked, ordered subset of the hubs; and (3) a wikilink target like any other note.
This triple duty is the single most important abstraction in the system. The invariant it
implies: _a note is reachable only if some index links to it, and the site's navigable
structure is carried by the index pages._ Note the "usually" in job 2: the nav is now a
curated subset rather than the whole set — the `Solo Golf` hub, for instance, is reachable
from the home page and cross-links but is deliberately kept off the navbar. The vault is
otherwise a flat folder — there are no content subdirectories, and the structure is
entirely conceptual, carried by these seven hubs. Adding a topic area is therefore a
two-or-three-part move: a new index note (tagged `index`), wikilinks from it to its notes,
and — if the topic belongs in the navbar — a nav entry in `config.json`. Skip the wikilinks
and the notes are orphans; skip the nav entry and the topic is reachable only by link,
which is sometimes the intent.

**Publishing is a human act in Obsidian, deliberately severed from git.** This is the
system's most counterintuitive and most defended decision (commit 5324c8b: "Point
CLAUDE.md at the Obsidian plugin as the canonical publisher"). `git push` records history
and deploys nothing. The actual publish runs from inside the Obsidian Flowershow plugin,
whose compiled `main.js` — all ~46,000 lines of it — is _vendored into the repo_ so the
publishing mechanism travels with the content. Its credential is the one thing split out:
`.obsidian/plugins/flowershow/data.json` is the sole gitignored file, because it holds the
auth token. So the separation that matters is not code-vs-content but **publisher-code
(committed) vs publisher-credential (gitignored)**.

**The vault is public-by-default, and `excludePatterns` is the safety membrane.**
Everything at the root publishes unless it matches a regex in the plugin config: currently
`^CLAUDE\.md$`, `^_`, `^Drafts/`, `^Private/`. This is why the `_` prefix is load-bearing
rather than cosmetic, and why the warning against the `fl` CLI is not stylistic fussiness —
the CLI ignores `excludePatterns` and would publish everything outside `.gitignore`, which
is a much weaker filter. The threat model here is _accidental publication of working
material_, and the membrane is the only thing standing in front of it.

**The look is not freely chosen — it converges on the governance site.** `custom.css`
exists because of commit e2f4216, "Converge typography and palette with crbgc.org." The
green accent (`#006747`), the serif body, the suppressed logo-as-wordmark — these
deliberately echo the club's _formal_ site, which is a separate Hugo repo (`../crbgc/`)
publishing official records. The two sites are siblings with a principled division of
labor: governance and minutes there, essays and editorializing here. The visual
convergence is the thread that tells a reader they belong to the same club. Treat
`custom.css` as expressive of that relationship, not as arbitrary theming.

**A handful of defensive invariants come from the renderer, not the domain.** Flowershow
renders KaTeX unconditionally, so a literal `$` in prose starts a math span and corrupts
the page. The corpus enacts the defense — four notes carry escaped `\$` — and two separate
commits exist solely to fix dollar signs. Likewise, the Obsidian Linter rewrites files on
save (alphabetizing tags, normalizing heading case and em-dash spacing); commit 662c5ef is
the author _chasing the linter's output_ across eight files. The principle for a
maintainer: **match the tools' output rather than fight it**, because the tools win on the
next save regardless.

## The seams, and where the theory is thinnest

The clean seams are the two just described: vault↔renderer (mediated by `excludePatterns`
and KaTeX escaping) and this-repo↔governance-repo (mediated by visual convergence and a
content split). Both are principled.

The thin and contested seams are internal, and they are where I'd direct your attention:

**The frontmatter content model is now enacted, where it once wasn't.** `CLAUDE.md`
specifies a six-key ordered frontmatter — `title, description, tags, created, date,
lastmod` — added in commit 74c02fe. For a time the document and the corpus diverged: notes
carried only `title` and `date`, and nothing matched the spec but CLAUDE.md's own example.
The curation pass (commit e66d073, "enrich frontmatter") closed that gap, and the corpus
now broadly matches the documented shape — alphabetized `tags`, the three date keys, a
one-line `description`. The residual caution is narrower: `date` is occasionally omitted,
and the Obsidian Linter re-alphabetizes tags and normalizes heading case and em-dash
spacing on save, so match its output rather than hand-format and re-fight it.

**The spine invariant is normative, not enforced — so check it.** The rule "every note is
linked from its relevant index" is the whole basis of navigability, but nothing enforces
it, and it has been violated before. "Golf Measures" and "Golf's Transition from Hickory to
Steel Shafts" (commit 1a3cb6c) were once orphans, linked from no index. Since then "Golf
Measures" was removed in the curation pass and the transition note was wired into both the
History and Hickory hubs; a current sweep finds no orphans. But that is a property of the
latest cleanup, not of the system — the next added note can silently break it again.
Before you trust "the indexes cover everything," check.

**"Note" silently spans two kinds of object.** The same flat root, the same frontmatter,
and the same wikilink machinery hold both a 27 KB authored essay and a 4,500-line verbatim
transcription of the 2023 Rules of Golf. The Rules editions are reference corpus — ingested
primary sources — not editorial prose, yet nothing in the vocabulary distinguishes them.
They publish identically and sit in nav identically. This works today but means any future
operation that assumes "a note is a readable essay" (a word-count badge, an excerpt
generator, a reading-time estimate) will be wrong for the entire Rules cluster.

**Version-controlled editor state generates persistent noise.** Only `data.json` is
gitignored; the rest of `.obsidian/` — `workspace.json`, the compiled plugins, themes — is
tracked. The history is dotted with "Update Obsidian workspace state" commits and a plugin
update that churned 31,000 lines. This is incidental, not essential: it is per-machine UI
state riding in the same history as the content. Don't read meaning into those diffs, and
don't let them mask a real change.

**The backlog convention points at a row that doesn't exist.** `CLAUDE.md` says to read
the crbgc-notes row in `../NEXT.md` when starting work; there is no crbgc-notes row, only a
crbgc one. A small thing, but it tells you the workspace-level conventions were written
ahead of being fully populated.

## What changes easily, and what would require rethinking

The system is shaped to absorb **more of the same**: a new essay, wikilinked from an
existing index, optionally with a new index and nav entry if it opens a topic, restyled
through `custom.css`, kept private by an `_`/`Drafts/`/`Private/` placement until ready. A
maintainer who holds the theory will, for any such change, look first at the relevant
index page (is the note wired in?), then `config.json` (does nav need a link?), then —
if anything is sensitive — `excludePatterns`. That covers the overwhelming majority of real
work.

What would require rethinking something fundamental is **anything that disturbs the
flat-root, path-as-identity assumption**. The exclude patterns are regexes over
vault-relative paths; the nav hrefs are literal strings like `/Game Philosophy` with
spaces still baked into the URL; wikilinks resolve by bare filename. Introduce content
subdirectories and you break the flat nav model and the `^Drafts/`-style filters
simultaneously. The `(Index) ` filename prefix the hubs once carried was itself one of
these walls, and removing it was exactly such a sweep — it touched every index filename,
every nav href, and the hub references in `CLAUDE.md` in one move (the spaces in the slugs
are the residual brittleness it left behind). Switch publishers away from the Obsidian
plugin and you lose the `excludePatterns` membrane — the public-by-default vault becomes a
publish-everything vault, which is precisely the failure the current design spends its
complexity to prevent. These are the load-bearing walls; renaming a hub still means
updating its filename, its nav href, and every cross-link in lockstep.

## Where I am inferring, and could be wrong

I am inferring the _editorial thesis_ from reading the corpus, not from any stated mission;
the author may regard these as neutral notes and would then find my framing overconfident —
though the title clustering and the existence of explicitly argumentative essays make me
fairly sure.

(Two inferences this account once carried — that the six-key frontmatter was aspirational,
and that the orphaned newest notes were drift — have since been settled by the curation
pass: the frontmatter is now enacted across the corpus, and the orphans are wired in. Both
moved from "contested seam" to "resolved," which is why they no longer appear above.)

Finally, the **convergence with crbgc.org** is documented in one commit message and visible
in the CSS, but how tightly the two sites are meant to track each other over time is not
recorded anywhere. If the governance site restyles, whether this one is obligated to follow
is a decision the theory gestures at but never fixes.
