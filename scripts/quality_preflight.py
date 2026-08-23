"""Validate the static portfolio before publishing it."""

from __future__ import annotations

import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


class PortfolioHTMLParser(HTMLParser):
    """Collect IDs and local resource references from the portfolio HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            self.ids.append(element_id)
        for key in ("href", "src"):
            value = values.get(key)
            if value:
                self.references.append(value)


def _is_local_reference(value: str) -> bool:
    parsed = urlparse(value)
    return not parsed.scheme and not parsed.netloc and not value.startswith(("#", "mailto:", "tel:"))


def validate_html() -> list[str]:
    """Return static-site validation errors."""
    html_path = ROOT / "index.html"
    parser = PortfolioHTMLParser()
    parser.feed(html_path.read_text(encoding="utf-8"))

    errors: list[str] = []
    seen: set[str] = set()
    for element_id in parser.ids:
        if element_id in seen:
            errors.append(f"duplicate HTML id: {element_id}")
        seen.add(element_id)

    for reference in parser.references:
        if not _is_local_reference(reference):
            continue
        path_text = reference.split("#", 1)[0].split("?", 1)[0]
        if path_text and not (ROOT / path_text).exists():
            errors.append(f"missing local resource: {reference}")
    return errors


def validate_css() -> list[str]:
    """Catch simple truncation/merge damage in the hand-written stylesheet."""
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    if css.count("{") != css.count("}"):
        return ["styles.css has unbalanced braces"]
    return []


def main() -> int:
    """Run static validation and Git diff hygiene."""
    errors = [*validate_html(), *validate_css()]
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    completed = subprocess.run(("git", "diff", "--check"), check=False)  # noqa: S603
    if completed.returncode != 0:
        return completed.returncode

    print("Portfolio quality preflight passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
