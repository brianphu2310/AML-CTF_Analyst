# Ingestion: UN Security Council Consolidated List

## Status (read first)

- **Live run verified on a GitHub-hosted runner (4 Oct 2026).** [`LIVE_RUN.md`](LIVE_RUN.md) is written by the workflow itself: 1,011 rows (736 individuals, 275 entities), 14 UN list programmes, latest listing date in the file 22 Jul 2026. Screening "Eric Badege" (a listed name) returns an exact hit; an invented name returns none.
- **Source:** `https://scsanctions.un.org/resources/xml/en/consolidated.xml`, published by the UN Security Council as open data. It redirects to a signed blob URL; `requests` follows the redirect.
- **`robots.txt`:** the host returns 404 (no restrictions); the fetcher still checks and would stop if disallowed.
- **Simulated app data is unchanged.** The Streamlit app and warehouse do not read this file.
- **Sources tried and not used:** the DFAT Consolidated List and AUSTRAC pages returned no data to the runner, so they are not used. Reporting entities in Australia must use the DFAT list; this module is a demonstration on a comparable public list.

## Design

| Concern | Where | How |
|---|---|---|
| Fetching | `ingestion/fetch.py` | `PoliteFetcher`: robots.txt, identifying User-Agent, >= 1 s between requests, retries with back-off, on-disk cache |
| Parsing (pure) | `ingestion/un_sanctions.py` | `parse_consolidated(bytes)` to one row per individual / entity; aliases, nationalities, birth years, countries |
| Screening (pure) | `ingestion/un_sanctions.py` | `normalise`, `name_score`, `screen` over names and aliases |
| CLI | `python -m ingestion.un_sanctions` | exit codes: 2 fetch failed, 3 robots disallowed, 4 unparseable |
| Output | `data/raw/un_sanctions.csv` (git-ignored) | includes `source_url` and `scraped_at` |

## Tests (offline)

`tests/test_ingestion_un_sanctions.py` (parser, screening, CSV, CLI with a stub fetcher) and `tests/test_ingestion_fetch.py` (robots, rate limit, retries, cache). The XML fixture is hand-written to follow the structure seen in the real file; it is not a captured copy and the names in it are invented.

## Limits

- Fuzzy name matching produces false positives and misses (transliteration, partial names). It is a screening aid, not a decision.
- The list covers UN Security Council designations only.
- No dates of birth or document numbers are used in scoring yet.
