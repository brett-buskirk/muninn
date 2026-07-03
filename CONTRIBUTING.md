# Contributing

- **No direct commits to `main`** — branch → PR (`gh pr create`) → green checks → merge.
- **AgentGate runs on every PR** — `secrets` + `dangerous_patterns` block; `scope` is advisory.
- Commits are signed & Verified; never commit secrets (`.env`, keys are gitignored).

## Working on the script

`muninn` is a single Bash script. Keep it dependency-light: `bash`, `git`, `gh`, `jq` only.

- **Syntax-check before pushing:** `bash -n muninn`.
- **Run `shellcheck`** if you have it: `shellcheck muninn`.
- Colors go through the `$R/$G/$Y/…` vars (empty when non-TTY / `NO_COLOR`) — don't hardcode escapes.
- Each subcommand is a `cmd_<name>` function with a matching `help_<name>`; wire new ones into the
  `case` dispatcher and the `cmd_help` menu.
- Paths: `$HERE` = where the tool lives; `$ROOT` = the estate it manages (`$MUNINN_ROOT`).
- **Multi-field records use `\x1f` (unit separator), not tab.** `log`/`releases`/`digest` all build
  small per-event or per-repo records (`epoch\x1frepo\x1ftype\x1f...`) and split them back apart with
  `read`. Bash's `read` treats tab as an "IFS whitespace" character and collapses consecutive
  delimiters even when `IFS` is explicitly set to just tab — that silently drops empty fields (an
  unnamed release, a bare commit with no PR) and shifts everything after them out of position.
  `\x1f` doesn't collapse. `gh`/`jq` output still comes out as real TSV (`@tsv` is fixed), so it's
  translated with `tr '\t' '\037'` immediately after — `tr` has no `\x` hex escape, only octal
  (`\037` = 0x1F).
