"""Offline tests for ingestion.un_sanctions (parser on a hand-written fixture, screening, CLI with a stub fetcher)."""
from pathlib import Path

import pytest

from ingestion import un_sanctions as un

FIXTURE = Path(__file__).parent / "fixtures" / "un_consolidated_sample.xml"


@pytest.fixture(scope="module")
def rows():
    return un.parse_consolidated(FIXTURE.read_bytes())


def test_counts_and_types(rows):
    assert len(rows) == 3
    assert [r["record_type"] for r in rows] == ["individual", "individual", "entity"]


def test_individual_fields(rows):
    r = rows[0]
    assert r["name"] == "JOHN EXAMPLE SMITHSON"
    assert r["reference_number"] == "XXi.001"
    assert r["listed_on"] == "2012-12-31"
    assert r["aliases"] == "Johnny Smithson"          # the empty alias element is dropped
    assert r["countries"] == "Otherland | Testland"    # sorted, de-duplicated
    assert r["birth_years"] == "1971"
    assert r["nationalities"] == "Testland"
    assert r["original_script_name"] == "ジョン"


def test_entity_fields(rows):
    e = rows[2]
    assert e["name"] == "EXAMPLE TRADING CO" and e["aliases"] == "E.T. Company"


def test_wrong_document_rejected():
    with pytest.raises(ValueError):
        un.parse_consolidated(b"<html></html>")


def test_normalise_strips_accents_and_punctuation():
    assert un.normalise("  María-GÓMEZ, Jr. ") == "maria gomez jr"


def test_screen_exact_alias_and_order_insensitive(rows):
    assert un.screen("john example smithson", rows)[0]["score"] == 1.0
    assert un.screen("Smithson, Johnny", rows)[0]["reference_number"] == "XXi.001"   # via alias, reordered
    assert un.screen("Maria Gomez", rows)[0]["reference_number"] == "XXi.002"          # accents ignored


def test_screen_no_hit_for_unrelated_name(rows):
    assert un.screen("Zebediah Quill", rows) == []


def test_screen_threshold_controls_hits(rows):
    assert un.screen("John Smithson", rows, threshold=0.99) == []
    assert un.screen("John Smithson", rows, threshold=0.6)


def test_csv_roundtrip(rows, tmp_path):
    out = tmp_path / "x.csv"
    un.write_csv(rows, out)
    back = un.read_csv(out)
    assert len(back) == 3 and back[0]["source_url"] == un.SOURCE_URL and back[0]["scraped_at"]
    assert list(back[0].keys()) == un.FIELDS


def test_cli_with_stub_fetcher(monkeypatch, tmp_path, capsys):
    class Stub:
        def __init__(self, *a, **k): pass
        def get_html(self, url):
            assert url == un.SOURCE_URL
            return FIXTURE.read_text(encoding="utf-8")
    monkeypatch.setattr(un, "PoliteFetcher", Stub)
    out = tmp_path / "o.csv"
    assert un.main(["--out", str(out), "--screen", "Maria Gomez"]) == 0
    assert "XXi.002" in capsys.readouterr().out and out.exists()


def test_cli_robots_abort_writes_nothing(monkeypatch, tmp_path):
    class Stub:
        def __init__(self, *a, **k): pass
        def get_html(self, url): raise un.RobotsDisallowed("no")
    monkeypatch.setattr(un, "PoliteFetcher", Stub)
    out = tmp_path / "o.csv"
    assert un.main(["--out", str(out)]) == 3 and not out.exists()
