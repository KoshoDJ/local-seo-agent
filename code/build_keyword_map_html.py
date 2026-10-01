#!/usr/bin/env python3
"""Render keyword-map.md as keyword-map.html - the build-off-it table view.

Reads the markdown (the single source of truth) and rebuilds the whole HTML
file every run, in the same Automatable style as the Google Ads reports
(audit-report.html, search-terms-report.html). Covers the "Written" and
"To build" sections in map order. Skips "Keywords saved for later" - it is
not buildable.

Usage:  python3 code/build_keyword_map_html.py
"""
from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP_MD = ROOT / "keyword-map.md"
MAP_HTML = ROOT / "keyword-map.html"

HEADING_RE = re.compile(r"^## (?:(\d+)\.\s+)?([^:]+):\s*(.+?)\s*$")
ROLE_RE = re.compile(r"^\*\*(Hub|Spoke|Sibling|Standalone)\*\*\s*(?:·\s*(.*))?$")
PRIMARY_RE = re.compile(
    r"^- (?P<kw>.+?) · (?P<vol>[\d,]+) searches a month · "
    r"(?P<label>Easy to rank for|Easy|Medium|Hard) \((?P<score>[^)]+?) out of 100\)"
    r"(?: - (?P<note>.*))?$"
)
SECONDARY_RE = re.compile(
    r"^- (?P<kw>.+?) · (?P<vol>[\d,]+) a month · "
    r"(?P<label>Easy|Medium|Hard) \((?P<score>[^)]+?)\)"
    r"(?: - (?P<note>.*))?$"
)
STOP_HEADINGS = ("## Keywords saved for later",)
DIFFICULTY_CLASS = {"Easy": "good", "Medium": "warn", "Hard": "bad"}

STAR = (
    '<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="currentColor" aria-hidden="true">'
    '<path d="M12 2 L13.4 10.6 L22 12 L13.4 13.4 L12 22 L10.6 13.4 L2 12 L10.6 10.6 Z"/></svg>'
)


@dataclass(frozen=True)
class Keyword:
    text: str
    searches: str
    label: str
    score: str
    note: str = ""


@dataclass
class Cluster:
    number: str
    page_type: str
    topic: str
    section: str
    role: str = ""
    role_detail: str = ""
    status: str = ""
    primary: Keyword | None = None
    secondaries: list[Keyword] = field(default_factory=list)

    @property
    def written(self) -> bool:
        return self.section.lower().startswith("written")


def clean_label(label: str) -> str:
    return "Easy" if label.startswith("Easy") else label


def parse_map(text: str) -> list[Cluster]:
    clusters: list[Cluster] = []
    current: Cluster | None = None
    section = ""
    mode = ""

    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith(STOP_HEADINGS):
            break
        if line.startswith("# "):
            section = line[2:].split("·")[0].strip()
            current = None
            mode = ""
            continue
        heading = HEADING_RE.match(line)
        if heading and line.startswith("## "):
            number, page_type, topic = heading.groups()
            current = Cluster(number or "", page_type.strip(), topic, section)
            clusters.append(current)
            mode = ""
            continue
        if current is None:
            continue
        role = ROLE_RE.match(line)
        if role:
            current.role = role.group(1)
            current.role_detail = (role.group(2) or "").strip()
            continue
        if line.startswith("**Status:**") and not current.status:
            current.status = line[len("**Status:**"):].strip()
            continue
        if line == "**Primary keyword**":
            mode = "primary"
            continue
        if line == "**Secondary keywords**":
            mode = "secondary"
            continue
        if not line.startswith("- "):
            if line.startswith("**"):
                mode = ""
            continue
        if mode == "primary":
            m = PRIMARY_RE.match(line)
            if not m:
                sys.exit(f"Could not parse primary keyword line: {line!r}")
            current.primary = Keyword(m["kw"], m["vol"], clean_label(m["label"]), m["score"], m["note"] or "")
        elif mode == "secondary":
            m = SECONDARY_RE.match(line)
            if not m:
                sys.exit(f"Could not parse secondary keyword line: {line!r}")
            current.secondaries.append(
                Keyword(m["kw"], m["vol"], clean_label(m["label"]), m["score"], m["note"] or "")
            )
    return clusters


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def strip_md(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    return value.replace("**", "").replace("`", "")


def to_int(value: str) -> int:
    return int(value.replace(",", ""))


def difficulty_cell(kw: Keyword) -> str:
    score = "under 5" if kw.score.lower().startswith("under") else kw.score
    css = DIFFICULTY_CLASS.get(kw.label, "")
    return (
        f'<td class="diff"><span class="st {css}">{esc(score)}</span>'
        f'<span class="dl">{esc(kw.label)}</span></td>'
    )


def keyword_cell(kw: Keyword, primary: bool) -> str:
    note = f'<span class="note">{esc(kw.note)}</span>' if kw.note else ""
    css = "kw primary" if primary else "kw"
    return f'<td class="{css}">{esc(kw.text)}{note}</td>'


def render_cluster(order: int, cluster: Cluster) -> str:
    primary = cluster.primary
    if primary is None:
        sys.exit(f"Cluster has no primary keyword: {cluster.topic}")
    note = f'<span class="note">{esc(primary.note)}</span>' if primary.note else ""
    rows = [
        f'<tr class="p"><td class="n display">{order}</td>'
        f'<td class="kw primary"><span class="k">{esc(cluster.page_type)}</span>{esc(primary.text)}{note}</td>'
        f'<td class="vol primary">{esc(primary.searches)}</td>'
        f"{difficulty_cell(primary)}</tr>"
    ]
    for kw in cluster.secondaries:
        rows.append(
            f'<tr class="s"><td class="n"></td>{keyword_cell(kw, False)}'
            f'<td class="vol">{esc(kw.searches)}</td>{difficulty_cell(kw)}</tr>'
        )
    return "\n".join(rows)


def render_table(clusters: list[Cluster]) -> str:
    body = chr(10).join(render_cluster(i, c) for i, c in enumerate(clusters, start=1))
    return (
        '<table><thead><tr><th class="c">#</th><th>Keyword</th>'
        '<th class="r">Searches a month</th><th>Difficulty (out of 100)</th></tr></thead>'
        f"<tbody>{body}</tbody></table>"
    )


CSS = """
  * { box-sizing:border-box; margin:0; padding:0; }
  :root { --canvas:#f5f4ed; --ivory:#faf9f5; --sand:#eeece3; --ink:#141413; --body:#5e5d59; --muted:#87867f;
    --hairline:#f0eee6; --hairline-soft:#e8e6dc; --ring:#d1cfc5; --coral:#d97757;
    --good:#3d7a4a; --good-bg:rgba(61,122,74,.08); --good-ring:rgba(61,122,74,.25);
    --warn-bg:rgba(212,160,23,.10); --warn-ring:rgba(212,160,23,.30);
    --bad:#b53333; --bad-bg:rgba(181,51,51,.07); --bad-ring:rgba(181,51,51,.22); }
  body { background:var(--canvas); color:var(--ink); font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Helvetica,Arial,sans-serif; -webkit-font-smoothing:antialiased; padding:32px; }
  .display { font-family:"Tiempos Text",Georgia,serif; font-weight:500; }
  .k, .st { font-family:"JetBrains Mono",ui-monospace,Menlo,monospace; }
  .wrap { overflow-x:auto; background:var(--ivory); border:1px solid var(--hairline); border-radius:16px; box-shadow:rgba(0,0,0,.04) 0 4px 24px; max-width:960px; margin:0 auto; }
  table { width:100%; border-collapse:collapse; font-size:14px; }
  th { font-family:"JetBrains Mono",ui-monospace,monospace; font-size:10px; text-transform:uppercase; letter-spacing:1.5px; color:#6e6d66; text-align:left; padding:14px 20px; border-bottom:1px solid var(--hairline-soft); font-weight:500; white-space:nowrap; }
  th.r { text-align:right; } th.c { text-align:center; }
  td { padding:9px 20px; border-bottom:1px solid var(--hairline); vertical-align:middle; }
  tr.p td { background:var(--sand); border-top:1px solid var(--ring); border-bottom:1px solid var(--hairline-soft); padding-top:12px; padding-bottom:12px; }
  td.n { width:64px; font-size:22px; letter-spacing:-.5px; text-align:center; color:var(--ink); }
  td.kw.primary { font-size:15px; font-weight:600; }
  td.kw .k { display:block; font-size:9.5px; text-transform:uppercase; letter-spacing:1.5px; color:var(--coral); margin-bottom:3px; font-weight:500; }
  tr.s td.kw { padding-left:44px; color:var(--body); }
  tr.s td.kw::before { content:"\\21B3"; color:var(--ring); margin-right:10px; }
  td.kw .note { display:block; font-size:12px; color:var(--muted); font-weight:400; margin-top:2px; }
  tr.s td.kw .note { margin-left:26px; }
  td.vol { width:150px; text-align:right; font-family:"JetBrains Mono",ui-monospace,monospace; font-size:13px; white-space:nowrap; color:var(--body); }
  td.vol.primary { color:var(--ink); font-weight:600; font-size:14px; }
  td.diff { width:180px; white-space:nowrap; } td.diff .dl { font-size:12px; color:var(--body); margin-left:8px; }
  .st { display:inline-block; font-size:10px; letter-spacing:.5px; padding:2px 0; border-radius:99px; width:46px; text-align:center; }
  .st.good { background:var(--good-bg); color:var(--good); box-shadow:inset 0 0 0 1px var(--good-ring); }
  .st.warn { background:var(--warn-bg); color:#8a6a0c; box-shadow:inset 0 0 0 1px var(--warn-ring); }
  .st.bad { background:var(--bad-bg); color:var(--bad); box-shadow:inset 0 0 0 1px var(--bad-ring); }
"""


def render_html(clusters: list[Cluster]) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Keyword map</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">{render_table(clusters)}</div>
</body>
</html>
"""


def main() -> None:
    if not MAP_MD.exists():
        sys.exit(f"Missing {MAP_MD}")
    clusters = parse_map(MAP_MD.read_text(encoding="utf-8"))
    if not clusters:
        sys.exit("No clusters found in keyword-map.md")
    MAP_HTML.write_text(render_html(clusters), encoding="utf-8")
    print(f"Wrote {MAP_HTML} - {len(clusters)} clusters")
    print(f"file://{MAP_HTML}")


if __name__ == "__main__":
    main()
