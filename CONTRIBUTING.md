# Contributing

This portfolio is a static site. Keep changes simple, reviewable, and publish-safe.

## Quality preflight

Run this before opening or updating a pull request:

```bash
python scripts/quality_preflight.py
```

The preflight checks duplicate HTML IDs, missing local `href`/`src` resources, basic CSS brace integrity, and Git diff hygiene. The same script runs in GitHub Actions on pull requests and pushes to `main`.

CI is authoritative. Fix the cause of a failed gate rather than weakening the validator.

## Content changes

- Keep local links and assets valid.
- Do not commit secrets or private data.
- Verify resume links and project links after changing filenames.
- Keep HTML IDs unique so navigation and accessibility hooks remain deterministic.
