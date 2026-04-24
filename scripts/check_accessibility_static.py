#!/usr/bin/env python3
"""Static accessibility checks for generated pages."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path

from manifest_utils import ROOT


SKIP_DIRS = {".git", ".venv", ".pytest_cache"}


class AccessibilityParser(HTMLParser):
    def __init__(self, file_path: Path) -> None:
        super().__init__()
        self.file_path = file_path
        self.errors: list[str] = []
        self._anchor_stack: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag == "img":
            alt = attr.get("alt")
            if alt is None or not alt.strip():
                self.errors.append(f"image missing alt text: {attr.get('src', '(missing src)')}")
        if tag == "a":
            self._anchor_stack.append(
                {
                    "href": attr.get("href", ""),
                    "aria": (attr.get("aria-label") or attr.get("title") or "").strip(),
                    "text": "",
                    "has_labeled_image": False,
                }
            )
        elif self._anchor_stack and tag == "img":
            alt = (attr.get("alt") or "").strip()
            if alt:
                self._anchor_stack[-1]["has_labeled_image"] = True

    def handle_data(self, data: str) -> None:
        if self._anchor_stack:
            self._anchor_stack[-1]["text"] += data.strip()

    def handle_endtag(self, tag: str) -> None:
        if tag != "a" or not self._anchor_stack:
            return
        anchor = self._anchor_stack.pop()
        has_name = bool(anchor["aria"] or anchor["text"].strip() or anchor["has_labeled_image"])
        if anchor["href"] and not has_name:
            self.errors.append(f"link missing accessible name: {anchor['href']}")


def main() -> None:
    errors: list[str] = []
    for path in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        parser = AccessibilityParser(path)
        parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
        errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in parser.errors)

    if errors:
        print("Static accessibility errors:")
        for error in errors:
            print(f"  ERROR: {error}")
        sys.exit(1)

    print("Static accessibility checks passed.")


if __name__ == "__main__":
    main()
