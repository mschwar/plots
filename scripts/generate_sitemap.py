#!/usr/bin/env python3
"""Generate sitemap.xml from the published manifest inventory."""

from __future__ import annotations

from datetime import date
from html import escape

from manifest_utils import ROOT, published_entries


BASE_URL = "https://mschwar.github.io/plots/"


def render_sitemap() -> str:
    today = date.today().isoformat()
    urls = [("", today), ("plots_manifest.json", today)]
    urls.extend((entry["interactive"], today) for entry in published_entries(ROOT))
    entries = "\n".join(
        "  <url>\n"
        f"    <loc>{escape(BASE_URL + path)}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        "  </url>"
        for path, lastmod in urls
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>
"""


def main() -> None:
    (ROOT / "sitemap.xml").write_text(render_sitemap(), encoding="utf-8")


if __name__ == "__main__":
    main()
