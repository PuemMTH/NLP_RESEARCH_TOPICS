#!/usr/bin/env python3
"""Render workspace Markdown files to static HTML without external deps."""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "rendered-md"

def collect_inputs() -> list[Path]:
    """Render every research Markdown note plus POC README files."""
    paths = list((ROOT / "research").glob("**/*.md"))
    paths.extend((ROOT / "poc").glob("*/README.md"))
    return sorted({p.resolve() for p in paths if p.is_file()})


STYLE = """
:root {
  --bg: #f5f7fa;
  --paper: #ffffff;
  --ink: #172027;
  --muted: #61707d;
  --line: #d8dee5;
  --accent: #0f766e;
  --blue: #38598b;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: Arial, "Noto Sans Thai", Tahoma, sans-serif;
  line-height: 1.65;
}
main {
  width: min(980px, calc(100% - 32px));
  margin: 0 auto;
  padding: 36px 0 56px;
}
nav {
  margin-bottom: 18px;
  color: var(--muted);
  font-size: 0.9rem;
}
article {
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 28px;
}
h1, h2, h3, h4, h5, h6 { line-height: 1.25; letter-spacing: 0; }
h1 { margin-top: 0; font-size: 2.1rem; color: var(--accent); }
h2 { margin-top: 2rem; padding-top: 0.35rem; border-top: 1px solid var(--line); }
p { margin: 0.75rem 0; }
ul, ol { padding-left: 1.5rem; }
li + li { margin-top: 0.25rem; }
a { color: var(--blue); text-decoration-thickness: 1px; overflow-wrap: anywhere; }
code {
  background: #edf1f5;
  padding: 2px 5px;
  border-radius: 4px;
  font-family: Consolas, "SFMono-Regular", monospace;
  font-size: 0.92em;
}
pre {
  overflow-x: auto;
  background: #10131f;
  color: #e2e8f0;
  border-radius: 8px;
  padding: 14px 16px;
}
pre code { background: transparent; color: inherit; padding: 0; }
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  font-size: 0.94rem;
}
th, td {
  padding: 9px 8px;
  border: 1px solid var(--line);
  text-align: left;
  vertical-align: top;
}
th { background: #eef2f5; }
blockquote {
  margin: 1rem 0;
  padding: 0.7rem 1rem;
  border-left: 4px solid var(--accent);
  background: #f2f7f6;
  color: #29343d;
}
hr { border: 0; border-top: 1px solid var(--line); margin: 1.5rem 0; }
.source-path {
  margin-top: 20px;
  color: var(--muted);
  font-size: 0.85rem;
}
@media (max-width: 760px) {
  main { width: min(100% - 20px, 980px); padding-top: 20px; }
  article { padding: 18px; }
  table { display: block; overflow-x: auto; white-space: nowrap; }
}
"""


def slug_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return rel.replace("/", "__").replace(".md", ".html")


def inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)

    def repl_link(match: re.Match[str]) -> str:
        label = match.group(1)
        href = html.unescape(match.group(2))
        if href.startswith("/"):
            href = "../.." + href
        return f'<a href="{html.escape(href, quote=True)}">{label}</a>'

    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl_link, escaped)
    escaped = re.sub(
        r"(https?://[^\s<]+)",
        lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>',
        escaped,
    )
    return escaped


def is_table_sep(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and set(stripped.replace("|", "").replace(":", "").replace("-", "").strip()) == set()


def render_table(lines: list[str]) -> str:
    rows: list[list[str]] = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return ""
    header = rows[0]
    body = rows[2:] if is_table_sep(lines[1]) else rows[1:]
    out = ["<table><thead><tr>"]
    out.extend(f"<th>{inline(cell)}</th>" for cell in header)
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>")
        out.extend(f"<td>{inline(cell)}</td>" for cell in row)
        out.append("</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def render_markdown(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    in_ul = False
    in_ol = False

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            close_lists()
            i += 1
            continue

        if stripped.startswith("```"):
            close_lists()
            lang = stripped.strip("`").strip()
            block: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(block))}</code></pre>")
            continue

        if "|" in stripped and i + 1 < len(lines) and "|" in lines[i + 1] and is_table_sep(lines[i + 1]):
            close_lists()
            table_lines = [line, lines[i + 1]]
            i += 2
            while i < len(lines) and "|" in lines[i].strip() and lines[i].strip():
                table_lines.append(lines[i])
                i += 1
            out.append(render_table(table_lines))
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            close_lists()
            if heading.group(2).lower().startswith("last updated"):
                out.append(f'<p class="source-path">{inline(heading.group(2))}</p>')
                i += 1
                continue
            level = len(heading.group(1))
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            i += 1
            continue

        if stripped == "---":
            close_lists()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith(">"):
            close_lists()
            out.append(f"<blockquote>{inline(stripped.lstrip('>').strip())}</blockquote>")
            i += 1
            continue

        ordered = re.match(r"^\d+\.\s+(.*)$", stripped)
        if ordered:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{inline(ordered.group(1))}</li>")
            i += 1
            continue

        if stripped.startswith(("- ", "* ")):
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline(stripped[2:])}</li>")
            i += 1
            continue

        close_lists()
        para = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (
                not nxt
                or nxt.startswith(("#", "```", "- ", "* ", ">"))
                or re.match(r"^\d+\.\s+", nxt)
                or (("|" in nxt) and i + 1 < len(lines) and is_table_sep(lines[i + 1]))
            ):
                break
            para.append(nxt)
            i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")

    close_lists()
    return "\n".join(out)


def page(title: str, body: str, source: Path) -> str:
    rel = source.relative_to(ROOT).as_posix()
    return f"""<!doctype html>
<html lang="th">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>{STYLE}</style>
</head>
<body>
  <main>
    <nav><a href="../index.html">← Back to index</a></nav>
    <article>
      {body}
      <p class="source-path">Source: <code>{html.escape(rel)}</code></p>
    </article>
  </main>
</body>
</html>
"""


def extract_urls(text: str) -> list[str]:
    urls = re.findall(r"https?://[^\s<>)]+", text)
    return sorted(set(url.rstrip(".,;") for url in urls))


def rendered_href(src: Path) -> str:
    return "rendered-md/" + slug_for(src)


def generate_references_index(inputs: list[Path]) -> None:
    refs = sorted((ROOT / "research" / "references").glob("*.md"))
    sections: list[str] = []
    total_urls = 0

    for ref in refs:
        text = ref.read_text(encoding="utf-8")
        title = next(
            (
                line.lstrip("#").strip()
                for line in text.splitlines()
                if line.startswith("#") and not line.lstrip("#").strip().lower().startswith("last updated")
            ),
            ref.name,
        )
        urls = extract_urls(text)
        total_urls += len(urls)
        link = rendered_href(ref)
        rel = ref.relative_to(ROOT).as_posix()
        items = "\n".join(f'<li><a href="{html.escape(url, quote=True)}">{html.escape(url)}</a></li>' for url in urls)
        if not items:
            items = '<li><span class="muted">No external URLs found; see rendered note for local bibliography entries.</span></li>'
        sections.append(
            f"""
            <section>
              <h2>{html.escape(title)}</h2>
              <p><a href="{html.escape(link, quote=True)}">Open rendered reference note</a> · <code>{html.escape(rel)}</code> · {len(urls)} external URLs</p>
              <ul>{items}</ul>
            </section>
            """
        )

    refs_body = "\n".join(sections)
    out = f"""<!doctype html>
<html lang="th">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>References Index</title>
  <style>{STYLE}
  .summary {{
    margin-bottom: 18px;
    padding: 18px;
    border: 1px solid var(--line);
    border-radius: 8px;
    background: var(--paper);
  }}
  section {{
    margin-top: 18px;
    padding: 20px;
    border: 1px solid var(--line);
    border-radius: 8px;
    background: var(--paper);
  }}
  .muted {{ color: var(--muted); }}
  </style>
</head>
<body>
  <main>
    <nav><a href="index.html">← Back to index</a></nav>
    <div class="summary">
      <h1>References Index</h1>
      <p>รวม reference files ทั้งหมดใน <code>research/references/</code> และ external URLs ที่ extract ได้จากแต่ละไฟล์</p>
      <p><strong>{len(refs)}</strong> reference files · <strong>{total_urls}</strong> external URLs</p>
    </div>
    {refs_body}
  </main>
</body>
</html>
"""
    (ROOT / "output" / "references.html").write_text(out, encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    inputs = collect_inputs()
    for src in inputs:
        if not src.exists():
            continue
        text = src.read_text(encoding="utf-8")
        first_heading = next(
            (
                line.lstrip("#").strip()
                for line in text.splitlines()
                if line.startswith("#") and not line.lstrip("#").strip().lower().startswith("last updated")
            ),
            src.name,
        )
        body = render_markdown(text)
        target = OUT_DIR / slug_for(src)
        target.write_text(page(first_heading, body, src), encoding="utf-8")
        print(target.relative_to(ROOT))
    generate_references_index(inputs)
    print((ROOT / "output" / "references.html").relative_to(ROOT))


if __name__ == "__main__":
    main()
