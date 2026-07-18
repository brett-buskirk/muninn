# muninn cheat sheet

Quick reference for every command, option, and behavior. `muninn` is **memory for your GitHub
estate** — a read-only archivist that reports what shipped, and when, across every repo under the
estate root. Estate-scoped and config-driven; it derives everything from `git` history and the
GitHub API and stores nothing.

For the narrative version see the [README](README.md); for per-command detail in the terminal, run
`muninn <command> help`.

---

## At a glance

| Command | Aliases | What it does | Options |
|---------|---------|--------------|---------|
| [`log`](#log) | | Reverse-chronological activity timeline: merged PRs, releases, commits | `--since <window>`, `[repo]` |
| [`releases`](#releases) | | Every tag/release across the estate — a changelog-of-changelogs | |
| [`digest`](#digest) | | A written summary of what shipped in the window | `--since <window>`, `--md` |
| [`init`](#init) | | Write a muninn config with detected defaults | `--force` |
| [`help`](#help) | `-h`, `--help` | The command menu | |

- **Everything is read-only.** `log`, `releases`, and `digest` only *report* — nothing is fetched
  into your tree, no branch or PR is touched, no state is stored.
- The one exception is [`init`](#init), which writes muninn's own **config file** (never a repo).
- Running `muninn` with no command prints the [menu](#help).

---

## Requirements & global behavior

- **Requires** `bash` + `git` + `gh` (GitHub CLI, authenticated) + `jq`. Commits read from local
  `git`; PRs and releases come through `gh`, so an unauthenticated `gh` yields empty GitHub sections.
- **Estate-scoped & config-driven.** muninn operates on every repo under `MUNINN_ROOT` (directories
  containing a `.git`, sorted). Settings resolve **env var → config file → smart default**:
  - Config file: `${XDG_CONFIG_HOME:-~/.config}/muninn/config` (override with `MUNINN_CONFIG`). Write
    one with [`muninn init`](#init).
  - Keys: `MUNINN_ROOT` (estate dir, default `~/github-repos`), `MUNINN_OWNER` (default: your `gh`
    login, resolved lazily), `MUNINN_FAMILY` (space-separated repos to **exclude**), `MUNINN_SINCE`
    (default `--since` window, default `1w`).
  - **Free config for huginn users** — if a `MUNINN_*` value is unset and `~/.config/huginn/config`
    exists, muninn falls back to its `HUGINN_ROOT` / `HUGINN_OWNER` / `HUGINN_FAMILY`. A huginn user
    gets a working muninn with zero setup. (This `FAMILY` list — `MUNINN_FAMILY`, or huginn's
    `HUGINN_FAMILY` — is muninn's exclusion mechanism; it does not read the estate's `exemptions.json`
    directly.)
- **`NO_COLOR`** — set it (`NO_COLOR=1 muninn …`) to disable color. Output is also automatically plain
  when piped or redirected (not a TTY).
- **Two-level help** — `muninn help` for the menu, `muninn <command> help` (or `-h`/`--help`) for one
  command.
- **`--since <window>`** — how far back `log` and `digest` look. Format `<n><unit>`, unit ∈ `h` `d`
  `w` `mo` (e.g. `6h` · `3d` · `1w` · `2mo`). Default `1w`, overridable per-invocation or via
  `MUNINN_SINCE`. A malformed window errors (exit 1); an unrecognized `-flag` is ignored with a note.
- **`--md`** — [`digest`](#digest) only. Emits clean Markdown to stdout instead of the terminal view;
  redirect it to a file. Backtick / asterisk / underscore in PR and release titles are escaped so they
  render clean.
- **Network cost** — `git log`/tags are local and instant. Merged PRs are **one** estate-wide
  `gh search prs`; releases/tags are looked up **per repo** — the network cost of a full sweep, the
  same cost class as huginn's `doctor`.
- **Exit codes** — `0` on success; `1` on error (unknown command, a bad `--since` window, or no
  resolvable GitHub owner).

---

## `log`

A unified, reverse-chronological activity **timeline across the whole estate** — merged PRs (`⑃`),
releases/tags (`⚑`), and commits (`●`), interleaved, newest first. An optional `repo` argument scopes
the timeline to one repo. A repo with more than **5** non-merge commits in the window collapses to a
single `● N commits` line, so a busy week doesn't scroll forever.

Commits are local & fast; merged PRs are one estate-wide search; releases/tags are looked up per repo.

```sh
muninn log                 # default window: 1w
muninn log --since 6h
muninn log --since 3d
muninn log --since 2mo
muninn log huginn          # scope to a single repo
muninn log --since 1mo geri
```

| Option | Effect |
|--------|--------|
| `--since <window>` | How far back to look. Format `<n><unit>`, unit ∈ `h` `d` `w` `mo`. Default `1w`. |
| `[repo]` | Positional — scope the timeline to a single repo (in any position). |

---

## `releases`

Every tag/release across the estate — a **changelog-of-changelogs**. One block per repo (repos with
none are omitted), newest first within each: version, date, release title. Plain `git` tags without a
matching GitHub release are folded in too; pre-releases are flagged `(pre)`. Takes no options.

Network — pulls `gh release list` (up to 100 per repo) plus `git` tags, once per repo in the estate.

```sh
muninn releases
NO_COLOR=1 muninn releases   # plain text for a pipe or a log
```

*(No options.)*

---

## `digest`

A **written summary of what shipped** in the window — the headline feature. Repos with nothing in the
window are omitted; for each repo touched, in order: releases cut, merged PRs (joined on one line,
oldest first — a repo with more than **8** collapses to a count), then a commit count. `on <branch>`
is added only when commits are the sole event (no PRs or releases). Closes with an estate-level
headline of totals.

Same sources as [`log`](#log), summarized. Doubles as a contractor's *"what I shipped"* report — client
updates, invoicing notes, a brag-doc.

```sh
muninn digest                       # terminal view, default window 1w
muninn digest --since 2w
muninn digest --since 1mo
muninn digest --md                  # clean Markdown to stdout
muninn digest --since 1mo --md > shipped.md
```

| Option | Effect |
|--------|--------|
| `--since <window>` | How far back to summarize. Format `<n><unit>`, unit ∈ `h` `d` `w` `mo`. Default `1w`. |
| `--md` | Emit clean Markdown to stdout (redirect to a file); titles are escaped so they render clean. |

---

## `init`

Write a muninn **config file** at `${XDG_CONFIG_HOME:-~/.config}/muninn/config` (or `$MUNINN_CONFIG`)
with detected defaults — your `gh` login as `MUNINN_OWNER` and `~/github-repos` as `MUNINN_ROOT`. Edit
it afterward. If a config already exists it declines and points you at the file; `--force` overwrites.
Env `MUNINN_*` vars still override the file, and any key you leave unset falls back to
`~/.config/huginn/config` when present — so the file only needs the keys you want to diverge on.

```sh
muninn init                # write config with detected defaults (no-op if one exists)
muninn init --force        # overwrite an existing config
```

| Option | Effect |
|--------|--------|
| `--force` | Overwrite an existing config file instead of declining. |

---

## `help`

```sh
muninn                 # no command → the menu
muninn help            # the command menu
muninn -h              # same
muninn <command> help  # detail for one command (e.g. muninn digest help)
```

---

## Recipes

```sh
# What happened across the estate this week? (the default window)
muninn log

# Just today, everywhere
muninn log --since 1d

# One repo's recent arc
muninn log --since 1mo huginn

# What versions are out there, and when did they ship?
muninn releases

# A written "what shipped" summary for the last two weeks
muninn digest --since 2w

# Generate a shareable Markdown report for a client update / work-log
muninn digest --since 1mo --md > shipped.md

# First-run setup: write a config, then edit to taste
muninn init

# Point muninn at a different estate root for one call
MUNINN_ROOT=~/clients/acme muninn digest --since 1w

# Exclude noisy repos from a digest without editing the config
MUNINN_FAMILY="scratch throwaway" muninn digest

# Plain output for a pipe or a log (no color)
NO_COLOR=1 muninn log
```
