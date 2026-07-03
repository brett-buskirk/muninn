# Changelog

All notable changes to muninn are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Config-driven** — settings resolve env → config file → smart defaults: `MUNINN_OWNER`,
  `MUNINN_ROOT`, `MUNINN_FAMILY`, `MUNINN_SINCE`. Config lives at `~/.config/muninn/config`. Falls
  back to `~/.config/huginn/config`'s `HUGINN_ROOT`/`HUGINN_OWNER`/`HUGINN_FAMILY` when its own
  config is unset, so a huginn user gets a working muninn with zero setup.
- **`init`** — writes a config file with detected defaults.
- **`log`** — unified, reverse-chronological activity timeline across the estate: merged PRs,
  releases/tags, and commits, interleaved, newest first. `--since` window (`1w`/`3d`/`2mo`/`1h`),
  optional `repo` scope. A repo with more than 5 non-merge commits in the window collapses to a
  single count line.
- **`releases`** — every tag/release across the estate, one block per repo (repos with none
  omitted), newest first within each: version, date, title. Folds in plain git tags a GitHub
  release doesn't cover; flags pre-releases.
- **`digest`** — a written summary of what shipped in the window: per repo, releases cut, merged
  PRs (a repo with more than 8 collapses to a count), and a commit count; plus an estate-level
  headline of totals. `--md` emits clean Markdown — a contractor's "what I shipped" report for
  client updates, invoicing notes, or a brag-doc.
- Two-level help: `muninn help` overview + `muninn <command> help` per-command detail.
