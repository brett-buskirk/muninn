# CLAUDE.md — Muninn Build Handoff

Spec for building **Muninn**, the memory half of a two-raven estate-management pair. Hand this to a
fresh Claude Code agent working in `~/github-repos/muninn/` as the working brief.

## The concept

In Norse myth Odin keeps two ravens: **Huginn** (*thought*) and **Muninn** (*memory*). They already
have a code sibling — [`huginn`](https://github.com/brett-buskirk/huginn) is a public Bash CLI that
flies the `~/github-repos` estate and reports **what it sees right now**: current branches, dirty
trees, open PRs, convention drift. Huginn is deliberately **stateless and present-tense**.

**Muninn is memory.** It answers the questions huginn structurally can't:

- *What happened across all my repos this week?*
- *What have I actually shipped — releases, merged work — and when?*
- *Give me a written summary of that I can hand a client or drop in a work-log.*

Huginn = the present. Muninn = the past, and the narrative over it. Build Muninn as huginn's twin:
same language, same look, same conventions — the other raven on the same shoulder.

## Scope — v0.1 is "the archivist"

Muninn v0.1 is a **read-only archivist**: everything is *derived* from git history and the GitHub API.
No stored state, no database — same "derive, don't store" ethos that keeps huginn simple. Three
commands:

### `muninn log [--since <window>] [repo]`
A unified, reverse-chronological **activity timeline across the whole estate** — merged PRs, releases/tags,
and commits interleaved, newest first. Optional `repo` arg scopes to one repo. `--since` takes a window
like `1w`, `3d`, `2mo` (default: `1w`).

Suggested line shape (one event per line, grouped by day is fine):
```
2d   asgard      ⑃ #14  feat: node autoscaling        (merged)
2d   huginn      ⚑ v0.2.0  public, config-driven
5d   heimdall    ●  chore: bump grafana to 11.1
```
Use icons/colors to distinguish PR · release · commit. Cap or summarize sanely so a busy week doesn't
scroll forever (e.g. collapse long commit runs to a count).

### `muninn releases`
Every tag/release across the estate — a **changelog-of-changelogs**. One block per repo (or a flat
newest-first timeline), showing version, date, and release title. Pull from `gh release list` plus git
tags. This is the "what versions are out there, and when did they ship" view.

### `muninn digest [--since <window>] [--md]`
A **written summary of what shipped** in the window — the headline feature. Terminal-formatted by
default; `--md` emits clean Markdown to stdout (redirect to a file). Per repo touched: commits, merged
PRs (by title), releases cut; with an estate-level headline of totals. This doubles as a contractor's
*"what I shipped"* report for client updates, invoicing notes, a portfolio/brag-doc, or LinkedIn.

Target Markdown shape:
```markdown
# What shipped — Jun 25–Jul 2, 2026

Across 6 repos: 34 commits · 8 PRs merged · 2 releases.

## huginn
- Released **v0.2.0** — public, config-driven, self-contained
- Merged #1 config-driven · #2 bundled templates · #3 doc-accuracy · #4 release
- 22 commits

## asgard
- 7 commits on `main`
```

## Tech stack & architecture — mirror huginn

**This is the most important instruction: `huginn` is your reference implementation.** Read
`~/github-repos/huginn/huginn` (it's public and sits right beside this repo) and match it closely.
Muninn and huginn should feel like one toolkit.

- **Single Bash script** named `muninn` at the repo root, `set -uo pipefail`. Optional helper modules
  beside it (huginn keeps its `status` renderer in `repo-status.sh`) — split only if it helps.
- **Deps:** `bash`, `git`, `gh` (authenticated), `jq`. Nothing else.
- **Dispatcher pattern:** a `case "${1:-help}"` at the bottom routing to `cmd_<name>` functions, each
  with a matching `help_<name>`. **Two-level help:** `muninn help` shows a grouped menu; `muninn
  <command> help` shows per-command detail. Copy huginn's structure verbatim and adapt.
- **Config-driven, same precedence as huginn — env var → config file → smart default:**
  - Config file: `${XDG_CONFIG_HOME:-$HOME/.config}/muninn/config` (override with `MUNINN_CONFIG`).
  - Keys: `MUNINN_ROOT` (estate dir, default `~/github-repos`), `MUNINN_OWNER` (default: `gh` login,
    resolved lazily), `MUNINN_FAMILY` (space-separated repos to exclude), `MUNINN_SINCE` (default
    window, default `1w`).
  - **Nice touch — free config for huginn users:** if `MUNINN_*` is unset and `~/.config/huginn/config`
    exists, fall back to its `HUGINN_ROOT`/`HUGINN_OWNER`/`HUGINN_FAMILY`. A huginn user then gets a
    working Muninn with zero setup. Provide a `muninn init` (like huginn's) to write a config too.
- **Estate discovery:** identical to huginn — directories under `$ROOT` containing a `.git`, sorted,
  minus `$FAMILY`. Reuse its `repos()` helper shape.
- **ANSI truecolor** for output, gated on `[ -t 1 ] && [ -z "$NO_COLOR" ]` exactly like huginn; empty
  color vars when non-TTY or `NO_COLOR` set. **Respect `NO_COLOR` and non-TTY.**
- **Fast/local by default; network only where noted.** `git log`/tags are local and instant. PR and
  release enrichment go through `gh` — mark those commands as touching the network in their help, the
  way huginn does for `doctor`/`prs`.

## Working conventions (estate-wide — non-negotiable)

This repo follows the same standard as the rest of the estate. `huginn` is the reference; you can also
inspect the standard live with `huginn conventions`.

- **No direct commits to `main`.** Branch → PR via `gh pr create` → let the checks go green → **stop
  at the PR and let Brett merge.** Do not merge unless he explicitly says so. Build the tool as a
  sequence of focused PRs (one per command is a good rhythm), not one giant drop.
- **Signed commits.** SSH commit signing is already configured on this machine; commits must come out
  **Verified**. End commit messages with `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- **AgentGate runs on every PR** (`.agentgate.yml` + the workflow are already scaffolded here). Keep
  `secrets`/`dangerous_patterns` clean; `scope` is advisory.
- **The `brett-buskirk` gh account must be the active one** (`gh auth switch --user brett-buskirk` if a
  `/login` flipped it to `itguysocal`).
- **Match huginn's voice** in help text and docs — terse, lowercase, a little wry. Consistency across
  the pair matters. Keep author-facing copy professional; this is a public-facing portfolio tool.

## Docs suite to produce

Mirror huginn's (already partly scaffolded — `README.md`, `CONTRIBUTING.md`, `LICENSE` exist):
- **`README.md`** — what Muninn is (lead with the Huginn/Muninn framing), install (clone + symlink to
  `~/.local/bin/muninn` + `muninn init`), command table, "how it works", a config table.
- **`CHANGELOG.md`** — Keep a Changelog + SemVer, exactly like huginn. Start an `[Unreleased]`, roll to
  `[0.1.0]` at release.
- **`ROADMAP.md`** — see "Deferred" below.
- **`CONTRIBUTING.md`** — adapt huginn's (syntax-check, shellcheck, `cmd_*`/`help_*` pattern, path vars).

## Build sequence

1. Scaffold the `muninn` dispatcher: config block, color block, `repos()`/`is_family()`/`is_help()`/
   `need_owner()` helpers, empty `cmd_*`/`help_*` stubs, the `case` router, grouped `cmd_help`. (Lift
   huginn's skeleton wholesale and strip its command bodies.)
2. `muninn log` — the spine. Git commits first (local, fast), then interleave `gh` merged PRs + tags.
3. `muninn releases`.
4. `muninn digest` — terminal formatting first, then `--md` output.
5. Two-level help + per-command `help_*`; polish the grouped menu.
6. Docs suite + install symlink; `muninn init`.
7. Confirm `huginn doctor muninn` stays clean; open the release PR; (Brett merges, tags `v0.1.0`,
   publishes the release — same flow huginn used).

## Definition of Done

`muninn log`, `releases`, and `digest` all work against the real estate; `digest --md` produces a
shareable Markdown report; the tool is config-driven with two-level help; docs suite complete; passes
`huginn doctor muninn` clean; shipped as **v0.1.0**. Muninn should feel unmistakably like huginn's twin.

## Deferred — Roadmap (do NOT build in v0.1)

Capture these in `ROADMAP.md`; they're explicitly out of scope for the first cut:

- **Decision log (the "why")** — `muninn note "…" [--repo x] [--tag decision]` to append a timestamped
  note, and `muninn recall <query>` to search it back. This is the one feature where Muninn *would*
  store its own memory (a flat file / append log). It's the most literally-Muninn idea and a strong
  v0.2 — but the archivist ships first.
- **`--json`** output for `log`/`digest` (scripting).
- **`muninn timeline <repo>`** — one repo's full history as a readable arc.
- **Scheduled/auto digest** — e.g. a weekly digest committed to a log or mailed out.
- **Going public** — like huginn, flip visibility + enable secret scanning once it's solid (Brett's
  call; leave private until then).

## Placeholders / Brett to provide

- **Repo description** — currently empty; set it (`gh repo edit brett-buskirk/muninn --description "…"`)
  once the tagline feels right. Suggestion to react to: *"Memory for your GitHub estate — what you
  shipped, and when."*
- **Default `--since` window** — `1w` assumed; adjust to taste.
