# Last live ingestion run (UN consolidated sanctions list)

Written by `live-ingestion.yml` on a GitHub-hosted runner. Run: https://github.com/brianphu2310/AML-CTF_Analyst/actions/runs/37234053918

- Run at (UTC): 2026-10-04T20:56:56Z
- Rows: 1011 (736 individuals, 275 entities)
- Distinct UN list programmes: 14
- Most recent listing date in the file: 2026-07-22

## Screening a listed name ("Eric Badege")
```
1.00  individual CDi.001  ERIC BADEGE  (matched: ERIC BADEGE)
```

## Screening an unlisted name ("Zebediah Quillfeather")
```
(no output = no hit above the threshold)
```

## Run log (tail)
```
2026-10-04 20:56:53,594 DEBUG urllib3.connectionpool: Starting new HTTPS connection (1): scsanctions.un.org:443
2026-10-04 20:56:53,978 DEBUG urllib3.connectionpool: https://scsanctions.un.org:443 "GET /robots.txt HTTP/1.1" 404 39
2026-10-04 20:56:55,177 DEBUG urllib3.connectionpool: https://scsanctions.un.org:443 "GET /resources/xml/en/consolidated.xml HTTP/1.1" 302 0
2026-10-04 20:56:55,178 DEBUG urllib3.connectionpool: Starting new HTTPS connection (1): unsolprodfiles.blob.core.windows.net:443
2026-10-04 20:56:55,474 DEBUG urllib3.connectionpool: https://unsolprodfiles.blob.core.windows.net:443 "GET /publiclegacyxmlfiles/EN/consolidatedLegacyByPRN.xml?sv=2024-05-04&st=2026-10-04T20%3A56%3A55Z&se=2026-10-04T21%
2026-10-04 20:56:56,232 DEBUG charset_normalizer: Encoding detection: utf_8 is most likely the one.
2026-10-04 20:56:56,237 INFO ingestion.fetch: fetched https://scsanctions.un.org/resources/xml/en/consolidated.xml (2177850 chars)
2026-10-04 20:56:56,309 INFO ingestion.un_sanctions: wrote data/raw/un_sanctions.csv: 1011 rows (736 individuals, 275 entities)
2026-10-04 20:56:56,596 INFO ingestion.fetch: cache hit https://scsanctions.un.org/resources/xml/en/consolidated.xml
2026-10-04 20:56:56,682 INFO ingestion.un_sanctions: wrote data/raw/un_sanctions.csv: 1011 rows (736 individuals, 275 entities)
```
