#!/usr/bin/env python3
"""Generate the root homepage from plots_manifest.json."""

from __future__ import annotations

from html import escape
from pathlib import Path

from manifest_utils import ROOT, published_entries


BADGES = {
    "high": ["Historical", "High confidence"],
    "medium": ["Historical", "Estimated"],
    "mixed": ["Historical", "Estimated", "Speculative"],
    "speculative": ["Estimated", "Speculative", "Needs source review"],
}


def _card(entry: dict) -> str:
    order = entry["order"]
    title = escape(entry["title"])
    description = escape(entry["description"])
    hero_stat = escape(entry["hero_stat"])
    confidence = escape(entry["confidence"].title())
    badges = "".join(f'<span class="badge">{escape(badge)}</span>' for badge in BADGES[entry["confidence"]])
    aria = f"Open {title} interactive plot" if entry.get("kind") == "plot" else "Open Unified Dashboard"

    if entry.get("png"):
        media = (
            f'<img src="{escape(entry["png"])}" '
            f'alt="{title} chart preview for the Exponential Progress Atlas">'
        )
    else:
        media = (
            '<div class="dashboard-preview" role="img" '
            'aria-label="Unified Dashboard timeline preview">Unified Dashboard</div>'
        )

    links = [
        ("Interactive", entry["interactive"]),
        ("PNG", entry.get("png")),
        ("SVG", entry.get("svg")),
        ("Data", entry.get("data")),
        ("Metadata", entry.get("metadata")),
    ]
    links_html = "\n".join(
        f'                    <a href="{escape(url)}">{escape(label)}</a>'
        for label, url in links
        if url
    )

    return f"""        <article class="card" data-plot-id="{escape(entry["id"])}">
            <a class="card-media" href="{escape(entry["interactive"])}" aria-label="{escape(aria)}">
                {media}
            </a>
            <div class="card-content">
                <div class="card-kicker">{order}. {escape(entry["short_title"])}</div>
                <h2>{title}</h2>
                <div class="badges">{badges}</div>
                <div class="card-stat"><span class="stat-number">{hero_stat}</span><span class="stat-label">Data confidence: {confidence}</span></div>
                <p>{description}</p>
                <div class="links">
{links_html}
                </div>
            </div>
        </article>"""


def render_homepage(entries: list[dict]) -> str:
    cards = "\n\n".join(_card(entry) for entry in entries)
    quick_links = "\n".join(
        f'        <a href="{escape(entry["interactive"])}">{escape(entry["short_title"])}</a>'
        for entry in entries
    )
    rows = "\n".join(
        f"                <tr><td>{entry['order']}</td><td><strong>{escape(entry['title'])}</strong></td><td>{escape(entry['description'])}</td><td>{escape(entry['confidence'])}</td></tr>"
        for entry in entries
    )
    count = len(entries)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exponential Progress Atlas</title>
    <meta name="description" content="Interactive timelines showing how compute, energy, coordination, memory, and adoption compound into civilizational acceleration.">
    <link rel="stylesheet" href="shared/site.css">
    <style>
        body {{ max-width: 1200px; }}
    </style>
</head>
<body data-page="home" data-published-count="{count}">
    <header class="hero">
        <p class="eyebrow">Manifest-driven data visualization atlas</p>
        <h1>Exponential Progress Atlas</h1>
        <p class="subtitle">Interactive timelines showing how compute, energy, coordination, memory, and adoption compound into civilizational acceleration.</p>
        <nav class="quick-links" aria-label="Published atlas entries">
            <strong>{count} published entries:</strong>
{quick_links}
        </nav>
    </header>

    <section class="thesis" aria-labelledby="thesis-title">
        <h2 id="thesis-title">Atlas Thesis</h2>
        <div class="thesis-flow" aria-label="Compute, energy, coordination, memory, and adoption feed capability acceleration">
            <span>Energy</span>
            <span>Compute</span>
            <span>Memory</span>
            <span>Coordination</span>
            <span>Adoption</span>
            <strong>Capability Acceleration</strong>
        </div>
        <p>Each chart is an audit surface: historical observations, estimates, proxies, and speculative projections are labeled so the story remains readable without hiding uncertainty.</p>
    </section>

    <section class="description" aria-labelledby="read-title">
        <h2 id="read-title">How to Read These Charts</h2>
        <p>Log scales turn multiplicative change into visible slopes. Circle markers indicate observed or estimated history; alternate markers and badges identify proxies, forecasts, and source-review needs. Use the interactive links for hover text and the data links to inspect source fields directly.</p>
    </section>

    <main class="cards" aria-label="Published atlas cards">
{cards}
    </main>

    <section class="why-section" aria-labelledby="inventory-title">
        <h2 id="inventory-title">Canonical Inventory</h2>
        <table>
            <thead>
                <tr><th>#</th><th>Entry</th><th>Scope</th><th>Confidence</th></tr>
            </thead>
            <tbody>
{rows}
            </tbody>
        </table>
    </section>

    <footer>
        <p>
            Inventory: <a href="plots_manifest.json">plots_manifest.json</a> |
            Built with Plotly, Matplotlib, D3.js |
            <a href="https://github.com/mschwar/plots">GitHub</a> |
            MIT License
        </p>
    </footer>

    <script src="shared/site.js"></script>
</body>
</html>
"""


def main() -> None:
    (ROOT / "index.html").write_text(render_homepage(published_entries(ROOT)), encoding="utf-8")


if __name__ == "__main__":
    main()
