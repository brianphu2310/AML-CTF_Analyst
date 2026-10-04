"""UN Security Council Consolidated Sanctions List: fetch, parse, screen.

Source: https://scsanctions.un.org/resources/xml/en/consolidated.xml, published by the UN Security
Council as open data. One XML file with ``<INDIVIDUALS>`` and ``<ENTITIES>``. This module:

  * fetches it politely (robots.txt, identifying User-Agent, rate limit, retries, cache);
  * parses it into one flat CSV row per listed individual / entity, aliases joined with " | ";
  * offers a name screen (normalised exact, token-set and fuzzy matching) for demonstration.

Usage:
    python -m ingestion.un_sanctions --out data/raw/un_sanctions.csv
    python -m ingestion.un_sanctions --out data/raw/un_sanctions.csv --screen "Eric Badege"

This is a demonstration of screening against a real public list. It is NOT a compliance control:
Australian reporting entities must screen against the DFAT Consolidated List and other sources
required by their program, and a fuzzy score is a prompt for human review, not a decision.
"""
from __future__ import annotations

import argparse
import csv
import difflib
import logging
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

from .fetch import FetchError, PoliteFetcher, RobotsDisallowed

log = logging.getLogger("ingestion.un_sanctions")

SOURCE_URL = "https://scsanctions.un.org/resources/xml/en/consolidated.xml"
USER_AGENT = (
    "aml-portfolio-ingest/0.1 (personal portfolio project; "
    "https://github.com/brianphu2310/AML-CTF_Analyst)"
)
FIELDS = [
    "record_type", "data_id", "reference_number", "un_list_type", "listed_on", "name",
    "original_script_name", "aliases", "nationalities", "birth_years", "countries", "source_url",
    "scraped_at",
]


# ---- parsing (pure) -------------------------------------------------------------------------
def _text(el: ET.Element | None) -> str:
    return " ".join((el.text or "").split()) if el is not None else ""


def _full_name(el: ET.Element) -> str:
    parts = [_text(el.find(tag)) for tag in ("FIRST_NAME", "SECOND_NAME", "THIRD_NAME", "FOURTH_NAME")]
    return " ".join(p for p in parts if p)


def _values(el: ET.Element, tag: str) -> list[str]:
    return [v for v in (_text(x) for x in el.findall(f"{tag}/VALUE")) if v]


def _parse_record(el: ET.Element, record_type: str, alias_tag: str, address_tag: str) -> dict:
    aliases = [a for a in (_text(x.find("ALIAS_NAME")) for x in el.findall(alias_tag)) if a]
    countries = sorted({c for c in (_text(x.find("COUNTRY")) for x in el.findall(address_tag)) if c})
    years = sorted({y for y in (_text(x.find("YEAR")) for x in el.findall("INDIVIDUAL_DATE_OF_BIRTH")) if y})
    return {
        "record_type": record_type,
        "data_id": _text(el.find("DATAID")),
        "reference_number": _text(el.find("REFERENCE_NUMBER")),
        "un_list_type": _text(el.find("UN_LIST_TYPE")),
        "listed_on": _text(el.find("LISTED_ON")),
        "name": _full_name(el),
        "original_script_name": _text(el.find("NAME_ORIGINAL_SCRIPT")),
        "aliases": " | ".join(aliases),
        "nationalities": " | ".join(_values(el, "NATIONALITY")),
        "birth_years": " | ".join(years),
        "countries": " | ".join(countries),
    }


def parse_consolidated(xml_bytes: bytes) -> list[dict]:
    """Parse the consolidated list. Raises ValueError if the document is not that list."""
    root = ET.fromstring(xml_bytes)
    if root.tag != "CONSOLIDATED_LIST":
        raise ValueError(f"unexpected root element {root.tag!r}")
    rows = [_parse_record(e, "individual", "INDIVIDUAL_ALIAS", "INDIVIDUAL_ADDRESS") for e in root.iter("INDIVIDUAL")]
    rows += [_parse_record(e, "entity", "ENTITY_ALIAS", "ENTITY_ADDRESS") for e in root.iter("ENTITY")]
    return rows


# ---- screening (pure) -----------------------------------------------------------------------
def normalise(name: str) -> str:
    """Lower-case, strip accents and punctuation, collapse spaces."""
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", s.lower()).split())


def name_score(query: str, candidate: str) -> float:
    """0..1. Exact normalised match = 1.0; otherwise the better of token-set overlap and sequence ratio."""
    q, c = normalise(query), normalise(candidate)
    if not q or not c:
        return 0.0
    if q == c:
        return 1.0
    qt, ct = set(q.split()), set(c.split())
    overlap = len(qt & ct) / max(len(qt), len(ct))
    seq = difflib.SequenceMatcher(None, " ".join(sorted(q.split())), " ".join(sorted(c.split()))).ratio()
    return round(max(overlap, seq), 3)


def screen(query: str, rows: list[dict], threshold: float = 0.85, limit: int = 10) -> list[dict]:
    """Rank listed names (primary name and aliases) against ``query``; keep scores >= threshold."""
    hits = []
    for row in rows:
        names = [row["name"], *[a for a in row["aliases"].split(" | ") if a]]
        best, best_name = max(((name_score(query, n), n) for n in names if n), default=(0.0, ""))
        if best >= threshold:
            hits.append({**row, "score": best, "matched_name": best_name})
    return sorted(hits, key=lambda h: (-h["score"], h["name"]))[:limit]


# ---- IO -------------------------------------------------------------------------------------
def write_csv(rows: list[dict], out: Path, source_url: str = SOURCE_URL) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    scraped_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({**r, "source_url": source_url, "scraped_at": scraped_at})


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="data/raw/un_sanctions.csv", type=Path)
    ap.add_argument("--cache-dir", default="data/raw_html", type=Path)
    ap.add_argument("--min-interval", type=float, default=1.5)
    ap.add_argument("--user-agent", default=USER_AGENT)
    ap.add_argument("--screen", metavar="NAME", help="screen a name against the list after fetching")
    ap.add_argument("--threshold", type=float, default=0.85)
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    fetcher = PoliteFetcher(args.user_agent, cache_dir=args.cache_dir, min_interval=args.min_interval)
    try:
        xml_text = fetcher.get_html(SOURCE_URL)
    except RobotsDisallowed as exc:
        log.error("%s", exc)
        return 3
    except FetchError as exc:
        log.error("fetch failed: %s", exc)
        return 2
    try:
        rows = parse_consolidated(xml_text.encode("utf-8"))
    except (ET.ParseError, ValueError) as exc:
        log.error("could not parse the list: %s", exc)
        return 4
    write_csv(rows, args.out)
    n_ind = sum(r["record_type"] == "individual" for r in rows)
    log.info("wrote %s: %d rows (%d individuals, %d entities)", args.out, len(rows), n_ind, len(rows) - n_ind)
    if args.screen:
        for h in screen(args.screen, rows, args.threshold):
            print(f"{h['score']:.2f}  {h['record_type']:10s} {h['reference_number']:8s} {h['name']}  (matched: {h['matched_name']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
