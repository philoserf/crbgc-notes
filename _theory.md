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

**The `(Index)` page is the spine, and it does three jobs at once.** A file named
`(Index) Hickory Era.md` is simultaneously (1) a topic hub — a short framing paragraph
plus a hand-curated list of `[[wikilinks]]`; (2) a navigation entry, because
`config.json`'s nav contains exactly one link per index page and nothing else; and (3) a
wikilink target like any other note. This triple duty is the single most important
abstraction in the system. The invariant it implies: _the navigable structure of the site
equals the set of index pages, and a note is reachable only if some index links to it._
The vault is otherwise a flat folder — there are no content subdirectories, and the
structure is entirely conceptual, carried by these eight hubs. Adding a topic area is
therefore a three-part move: new `(Index)` file, new nav entry in `config.json`, and
wikilinks from the index to its notes. Miss the middle step and the topic is invisible;
miss the third and the notes are orphans.

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

**The frontmatter content model is documented but not enacted.** `CLAUDE.md` specifies a
six-key ordered frontmatter — `title, description, tags, created, date, lastmod` — and
commit 74c02fe added that specification deliberately. Yet _not one note in the corpus uses
it._ Every note carries `title` plus `date` and nothing else; the only file in the repo
matching the documented shape is CLAUDE.md's own example. This is a genuine divergence
between the recorded theory and the enacted theory. A maintainer who trusts the document
and starts writing six-key frontmatter will produce notes inconsistent with all fifty-seven
existing ones; a maintainer who trusts the corpus will write `title`+`date` and contradict
the document. I cannot tell from the code whether the six-key shape is aspirational (a
target the author intends to migrate toward) or vestigial (copied from another repo's
conventions). This is the single most likely place to cause quiet damage.

**The spine invariant is already broken by the newest work.** The rule "every note is
linked from its relevant index" is real and is the whole basis of navigability — but the
two most recently added content notes, "Golf Measures" and "Golf's Transition from Hickory
to Steel Shafts" (commit 1a3cb6c), are orphans, linked from no index. The author added
prose and did not wire it into the spine. So the invariant is _normative, not enforced_: it
describes how the system is supposed to cohere, and the most recent commit silently
violates it. Before you trust "the indexes cover everything," check; they don't.

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
`(Index)` page (is the note wired in?), then `config.json` (does nav need a link?), then —
if anything is sensitive — `excludePatterns`. That covers the overwhelming majority of real
work.

What would require rethinking something fundamental is **anything that disturbs the
flat-root, path-as-identity assumption**. The exclude patterns are regexes over
vault-relative paths; the nav hrefs are literal strings like `/(Index) Game Philosophy`
with spaces and parentheses baked into the URL; wikilinks resolve by bare filename.
Introduce content subdirectories and you break the flat nav model and the `^Drafts/`-style
filters simultaneously. Rename the `(Index) ` prefix and you touch every filename, every
nav href, and every cross-link at once. Switch publishers away from the Obsidian plugin and
you lose the `excludePatterns` membrane — the public-by-default vault becomes a
publish-everything vault, which is precisely the failure the current design spends its
complexity to prevent. These are the load-bearing walls; the prefix-in-the-URL brittleness
in particular is the kind of thing a maintainer without the theory would "clean up" and
thereby break navigation.

## Where I am inferring, and could be wrong

I am inferring the _editorial thesis_ from reading the corpus, not from any stated mission;
the author may regard these as neutral notes and would then find my framing overconfident —
though the title clustering and the existence of explicitly argumentative essays make me
fairly sure.

I am inferring that the **six-key frontmatter is aspirational rather than abandoned** purely
from the fact that it was added to the doc recently while the corpus stayed at two keys; I
genuinely cannot resolve which direction the author intends to converge, and you should ask
rather than guess before mass-editing frontmatter.

I read the **orphaned newest notes** as drift (work-in-progress not yet wired in) rather
than intent, but it is possible the author deliberately keeps some notes reachable only by
URL. The pattern — newest commits, no index touched — points to oversight, but the code
alone can't confirm it.

Finally, the **convergence with crbgc.org** is documented in one commit message and visible
in the CSS, but how tightly the two sites are meant to track each other over time is not
recorded anywhere. If the governance site restyles, whether this one is obligated to follow
is a decision the theory gestures at but never fixes.
