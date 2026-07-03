# Roadmap

## Toward v0.2 — the decision log

- [ ] **`muninn note "…" [--repo x] [--tag decision]`** — append a timestamped note to a flat log.
- [ ] **`muninn recall <query>`** — search that log back. The one feature where Muninn *would* store
      its own memory (a flat file / append log) — the most literally-Muninn idea, and a strong v0.2.

## Command ideas

- [ ] **`--json`** output for `log`/`digest` — scripting.
- [ ] **`muninn timeline <repo>`** — one repo's full history as a readable arc.
- [ ] Scheduled/auto digest — e.g. a weekly digest committed to a log or mailed out.

## Going public

- [ ] Like huginn, flip visibility + enable secret scanning once it's solid (Brett's call; leave
      private until then).

## Polish

- [ ] `shellcheck` in CI.
- [ ] Bats tests for the pure-logic helpers (`since_to_gitdate`, `age_short`, `digest_daterange`).
- [ ] Tab completion (bash/zsh).
