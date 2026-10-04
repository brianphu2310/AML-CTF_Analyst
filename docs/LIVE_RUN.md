# Last live ingestion run (UN consolidated sanctions list)

Written by `live-ingestion.yml` on a GitHub-hosted runner. Run: https://github.com/brianphu2310/AML-CTF_Analyst/actions/runs/37234096784

- Run at (UTC): 2026-10-04T20:57:37Z
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
2026-10-04 20:57:34,535 DEBUG urllib3.connectionpool: Starting new HTTPS connection (1): scsanctions.un.org:443
2026-10-04 20:57:34,757 DEBUG urllib3.connectionpool: https://scsanctions.un.org:443 "GET /robots.txt HTTP/1.1" 404 39
2026-10-04 20:57:36,098 DEBUG urllib3.connectionpool: https://scsanctions.un.org:443 "GET /resources/xml/en/consolidated.xml HTTP/1.1" 302 0
2026-10-04 20:57:36,099 DEBUG urllib3.connectionpool: Starting new HTTPS connection (1): unsolprodfiles.blob.core.windows.net:443
2026-10-04 20:57:36,256 DEBUG urllib3.connectionpool: https://unsolprodfiles.blob.core.windows.net:443 "GET /publiclegacyxmlfiles/EN/consolidatedLegacyByPRN.xml?sv=2024-05-04&st=2026-10-04T20%3A57%3A36Z&se=2026-10-04T21%
2026-10-04 20:57:36,829 DEBUG charset_normalizer: Encoding detection: utf_8 is most likely the one.
2026-10-04 20:57:36,833 INFO ingestion.fetch: fetched https://scsanctions.un.org/resources/xml/en/consolidated.xml (2177850 chars)
2026-10-04 20:57:36,891 INFO ingestion.un_sanctions: wrote data/raw/un_sanctions.csv: 1011 rows (736 individuals, 275 entities)
2026-10-04 20:57:37,104 INFO ingestion.fetch: cache hit https://scsanctions.un.org/resources/xml/en/consolidated.xml
2026-10-04 20:57:37,165 INFO ingestion.un_sanctions: wrote data/raw/un_sanctions.csv: 1011 rows (736 individuals, 275 entities)
```
