#!/usr/bin/env python3
"""Check local relative links in HTML and Markdown files."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from manifest_utils import ROOT


SKIP_DIRS = {".git", ".venv", ".pytest_cache", ".agent-tasks"}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        for key in ("href", "src"):
            value = attr.get(key)
            if value:
                self.links.append(value)


def _iter_files() -> list[Path]:
    paths: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in {".html", ".md"}:
            paths.append(path)
    return paths


def _extract_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() == ".html":
        parser = LinkParser()
        parser.feed(text)
        return parser.links
    md_links = re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text)
    return md_links


def _is_local_link(link: str) -> bool:
    parsed = urlparse(link)
    return not parsed.scheme and not parsed.netloc and not link.startswith("#") and not link.startswith("mailto:")


def _resolve_link(path: Path, link: str) -> Path:
    clean = unquote(link.split("#", 1)[0].split("?", 1)[0])
    return (path.parent / clean).resolve()


def main() -> None:
    errors: list[str] = []
    for path in _iter_files():
        for link in _extract_links(path):
            if not _is_local_link(link):
                continue
            if not link.split("#", 1)[0].split("?", 1)[0]:
                continue
            target = _resolve_link(path, link)
            if not target.exists():
                errors.append(f"{path.relative_to(ROOT)} -> missing {link}")

    if errors:
        print("Broken relative links:")
        for error in errors:
            print(f"  ERROR: {error}")
        sys.exit(1)

    print("All relative links resolved.")


if __name__ == "__main__":
    main()
