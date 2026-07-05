#!/usr/bin/env python3
# screenshot.py — regenerate the README hero (docs/muninn-digest.png).
#
# Renders a REPRESENTATIVE `muninn digest` (illustrative fake acme-* data, not a
# live run — muninn queries GitHub by owner, so a demo can't be faked) into a
# clean terminal-window PNG that matches the rest of the toolkit's shots.
#
# Dev-only.  pip3 install --user rich cairosvg  &&  python3 scripts/screenshot.py
import os, tempfile
from rich.console import Console
from rich.text import Text
import cairosvg

LINES = [
    "",
    "  [bold]muninn digest[/]  [dim]· Jun 20 – Jul 4, 2026[/]",
    "",
    "  [bold]Across 6 repos: 84 commits · 19 PRs merged · 3 releases[/]",
    "",
    "  [bold]acme-web[/]",
    "    [magenta]⚑[/] Released [bold]v1.4.0[/] — dark mode + a11y pass",
    "    [cyan]⇄[/] Merged #212 feat: theme switcher · #210 fix: focus traps",
    "    [dim]● 22 commits[/]",
    "",
    "  [bold]acme-api[/]",
    "    [cyan]⇄[/] Merged #88 feat: rate limiting · #86 chore(deps): bump fastify",
    "    [dim]● 17 commits[/]",
    "",
    "  [bold]acme-infra[/]",
    "    [magenta]⚑[/] Released [bold]v0.9.0[/] — Terraform VPC + observability",
    "    [dim]● 9 commits on main[/]",
    "",
    "  [bold]acme-mobile[/]",
    "    [cyan]⇄[/] Merged #54 feat: offline sync",
    "    [dim]● 6 commits[/]",
    "",
]

texts = [Text.from_markup(l) for l in LINES]
con = Console(record=True, width=max(t.cell_len for t in texts) + 2)
for t in texts:
    con.print(t)
svg = tempfile.mktemp(suffix=".svg")
con.save_svg(svg, title="muninn digest")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "muninn-digest.png")
cairosvg.svg2png(url=svg, write_to=out, scale=2)
os.unlink(svg)
print("wrote", out)
