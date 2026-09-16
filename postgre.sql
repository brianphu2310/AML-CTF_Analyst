Last login: Thu Sep 10 11:11:13 on ttys000
(base) carrot@brians-MacBook-Pro ~ % /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
==> Checking for `sudo` access (which may request your password)...
Password:
==> This script will install:
/opt/homebrew/bin/brew
/opt/homebrew/share/doc/homebrew
/opt/homebrew/share/man/man1/brew.1
/opt/homebrew/share/zsh/site-functions/_brew
/opt/homebrew/etc/bash_completion.d/brew
/opt/homebrew
/etc/paths.d/homebrew
==> The following new directories will be created:
/opt/homebrew/bin
/opt/homebrew/etc
/opt/homebrew/include
/opt/homebrew/lib
/opt/homebrew/sbin
/opt/homebrew/share
/opt/homebrew/var
/opt/homebrew/opt
/opt/homebrew/share/zsh
/opt/homebrew/share/zsh/site-functions
/opt/homebrew/var/homebrew
/opt/homebrew/var/homebrew/linked
/opt/homebrew/Cellar
/opt/homebrew/Caskroom
/opt/homebrew/Frameworks
==> The Xcode Command Line Tools will be installed.

Press RETURN/ENTER to continue or any other key to abort:
==> /usr/bin/sudo /usr/bin/install -d -o root -g wheel -m 0755 /opt/homebrew
==> /usr/bin/sudo /bin/mkdir -p /opt/homebrew/bin /opt/homebrew/etc /opt/homebrew/include /opt/homebrew/lib /opt/homebrew/sbin /opt/homebrew/share /opt/homebrew/var /opt/homebrew/opt /opt/homebrew/share/zsh /opt/homebrew/share/zsh/site-functions /opt/homebrew/var/homebrew /opt/homebrew/var/homebrew/linked /opt/homebrew/Cellar /opt/homebrew/Caskroom /opt/homebrew/Frameworks
==> /usr/bin/sudo /bin/chmod ug=rwx /opt/homebrew/bin /opt/homebrew/etc /opt/homebrew/include /opt/homebrew/lib /opt/homebrew/sbin /opt/homebrew/share /opt/homebrew/var /opt/homebrew/opt /opt/homebrew/share/zsh /opt/homebrew/share/zsh/site-functions /opt/homebrew/var/homebrew /opt/homebrew/var/homebrew/linked /opt/homebrew/Cellar /opt/homebrew/Caskroom /opt/homebrew/Frameworks
==> /usr/bin/sudo /bin/chmod go-w /opt/homebrew/share/zsh /opt/homebrew/share/zsh/site-functions
==> /usr/bin/sudo /usr/sbin/chown carrot /opt/homebrew/bin /opt/homebrew/etc /opt/homebrew/include /opt/homebrew/lib /opt/homebrew/sbin /opt/homebrew/share /opt/homebrew/var /opt/homebrew/opt /opt/homebrew/share/zsh /opt/homebrew/share/zsh/site-functions /opt/homebrew/var/homebrew /opt/homebrew/var/homebrew/linked /opt/homebrew/Cellar /opt/homebrew/Caskroom /opt/homebrew/Frameworks
==> /usr/bin/sudo /usr/bin/chgrp admin /opt/homebrew/bin /opt/homebrew/etc /opt/homebrew/include /opt/homebrew/lib /opt/homebrew/sbin /opt/homebrew/share /opt/homebrew/var /opt/homebrew/opt /opt/homebrew/share/zsh /opt/homebrew/share/zsh/site-functions /opt/homebrew/var/homebrew /opt/homebrew/var/homebrew/linked /opt/homebrew/Cellar /opt/homebrew/Caskroom /opt/homebrew/Frameworks
==> /usr/bin/sudo /usr/sbin/chown -R carrot:admin /opt/homebrew
==> Searching online for the Command Line Tools
==> /usr/bin/sudo /usr/bin/touch /tmp/.com.apple.dt.CommandLineTools.installondemand.in-progress
==> Installing Command Line Tools for Xcode 26.6-26.6
==> /usr/bin/sudo /usr/sbin/softwareupdate -i Command\ Line\ Tools\ for\ Xcode\ 26.6-26.6
Software Update Tool

Finding available software

Downloading Command Line Tools for Xcode 26.6
Error downloading Command Line Tools for Xcode 26.6: The network connection was lost.
Done.

Error downloading updates.
==> /usr/bin/sudo /usr/bin/xcode-select --switch /Library/Developer/CommandLineTools
xcode-select: error: invalid developer directory '/Library/Developer/CommandLineTools'
Failed during: /usr/bin/sudo /usr/bin/xcode-select --switch /Library/Developer/CommandLineTools
(base) carrot@brians-MacBook-Pro ~ % sudo rm /tmp/.com.apple.dt.CommandLineTools.installondemand.in-progress
Password:
(base) carrot@brians-MacBook-Pro ~ % xcode-select --install
xcode-select: note: install requested for command line developer tools
(base) carrot@brians-MacBook-Pro ~ % /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
==> Checking for `sudo` access (which may request your password)...
==> This script will install:
/opt/homebrew/bin/brew
/opt/homebrew/share/doc/homebrew
/opt/homebrew/share/man/man1/brew.1
/opt/homebrew/share/zsh/site-functions/_brew
/opt/homebrew/etc/bash_completion.d/brew
/opt/homebrew
/etc/paths.d/homebrew

Press RETURN/ENTER to continue or any other key to abort:
==> /usr/bin/sudo /usr/sbin/chown -R carrot:admin /opt/homebrew
==> Downloading and installing Homebrew...
remote: Enumerating objects: 362269, done.
remote: Counting objects: 100% (594/594), done.
remote: Compressing objects: 100% (205/205), done.
remote: Total 362269 (delta 435), reused 447 (delta 389), pack-reused 361675 (from 4)
remote: Enumerating objects: 55, done.
remote: Counting objects: 100% (33/33), done.
remote: Total 55 (delta 33), reused 33 (delta 33), pack-reused 22 (from 1)
==> /usr/bin/sudo /bin/mkdir -p /etc/paths.d
==> /usr/bin/sudo tee /etc/paths.d/homebrew
/opt/homebrew/bin
==> /usr/bin/sudo /usr/sbin/chown root:wheel /etc/paths.d/homebrew
==> /usr/bin/sudo /bin/chmod a+r /etc/paths.d/homebrew
==> Updating Homebrew...
==> Downloading https://ghcr.io/v2/homebrew/core/portable-ruby/blobs/sha256:83a3ff85d83acf0e3dd8105de0fdb01da96b7c0eaf2dfaae2ba6500ec2ae4a64
################################################################################################################# 100.0%
==> Pouring portable-ruby-4.0.6.arm64_big_sur.bottle.tar.gz
==> Installation successful!

==> Homebrew has enabled anonymous aggregate formulae and cask analytics.
Read the analytics documentation (and how to opt-out) here:
  https://docs.brew.sh/Analytics
No analytics data has been sent yet (nor will any be during this install run).

==> Homebrew is run entirely by unpaid volunteers. Please consider donating:
  https://github.com/Homebrew/brew#donations

==> Next steps:
- Run these commands in your terminal to add Homebrew to your PATH:
    echo >> /Users/carrot/.zprofile
    echo 'eval "$(/opt/homebrew/bin/brew shellenv zsh)"' >> /Users/carrot/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv zsh)"
- Run brew help to get started
- Further documentation:
    https://docs.brew.sh

(base) carrot@brians-MacBook-Pro ~ % echo >> /Users/carrot/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv zsh)"' >> /Users/carrot/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv zsh)"
(base) carrot@brians-MacBook-Pro ~ % brew --version
Homebrew 6.0.22
(base) carrot@brians-MacBook-Pro ~ % brew install postgresql@16
==> Downloading bottle manifests
✔︎ Bottle Manifest postgresql@16 (16.15)                                                     Downloaded  118.9KB/118.9KB
==> Would install 1 formula:
postgresql@16
==> Would install 11 dependencies for postgresql@16:
icu4c@78
ca-certificates
openssl@3
krb5
lz4
readline
xz
zstd
json-c
libunistring
gettext
==> Do you want to proceed with the installation? [y/n]
==> Fetching downloads for: postgresql@16
✔︎ Bottle Manifest icu4c@78 (78.3)                                                           Downloaded    9.7KB/  9.7KB
✔︎ Bottle Manifest ca-certificates (2026-08-13)                                              Downloaded   11.9KB/ 11.9KB
✔︎ Bottle Manifest openssl@3 (3.6.4)                                                         Downloaded   20.2KB/ 20.2KB
✔︎ Bottle Manifest lz4 (1.10.0)                                                              Downloaded   13.1KB/ 13.1KB
✔︎ Bottle Manifest zstd (1.5.7_1)                                                            Downloaded   13.2KB/ 13.2KB
✔︎ Bottle Manifest readline (8.3.3)                                                          Downloaded   10.0KB/ 10.0KB
✔︎ Bottle Manifest xz (5.8.3)                                                                Downloaded   11.8KB/ 11.8KB
✔︎ Bottle Manifest krb5 (1.22.2)                                                             Downloaded   16.3KB/ 16.3KB
✔︎ Bottle Manifest json-c (0.19)                                                             Downloaded   12.7KB/ 12.7KB
✔︎ Bottle Manifest libunistring (1.4.2)                                                      Downloaded    7.3KB/  7.3KB
✔︎ Bottle ca-certificates (2026-08-13)                                                       Downloaded  112.2KB/112.2KB
✔︎ Bottle lz4 (1.10.0)                                                                       Downloaded  283.0KB/283.0KB
✔︎ Bottle readline (8.3.3)                                                                   Downloaded  757.9KB/757.9KB
✔︎ Bottle json-c (0.19)                                                                      Downloaded  106.9KB/106.9KB
✔︎ Bottle Manifest gettext (1.0)                                                             Downloaded   21.6KB/ 21.6KB
✔︎ Bottle krb5 (1.22.2)                                                                      Downloaded    1.3MB/  1.3MB
✔︎ Bottle zstd (1.5.7_1)                                                                     Downloaded  793.6KB/793.6KB
✔︎ Bottle xz (5.8.3)                                                                         Downloaded  770.8KB/770.8KB
✔︎ Bottle libunistring (1.4.2)                                                               Downloaded    1.9MB/  1.9MB
✔︎ Bottle openssl@3 (3.6.4)                                                                  Downloaded   11.0MB/ 11.0MB
✔︎ Bottle gettext (1.0)                                                                      Downloaded   10.2MB/ 10.2MB
✔︎ Bottle postgresql@16 (16.15)                                                              Downloaded   19.2MB/ 19.2MB
✔︎ Bottle icu4c@78 (78.3)                                                                    Downloaded   31.8MB/ 31.8MB
==> Installing dependencies for postgresql@16: icu4c@78, ca-certificates, openssl@3, krb5, lz4, readline, xz, zstd, json-c, libunistring and gettext
==> Installing postgresql@16 dependency: icu4c@78
==> Pouring icu4c@78--78.3.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/icu4c@78/78.3: 279 files, 87.5MB
==> Installing postgresql@16 dependency: ca-certificates
==> Pouring ca-certificates--2026-08-13.all.bottle.1.tar.gz
🍺  /opt/homebrew/Cellar/ca-certificates/2026-08-13: 5 files, 204.3KB
==> Installing postgresql@16 dependency: openssl@3
==> Pouring openssl@3--3.6.4.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/openssl@3/3.6.4: 7,639 files, 37.7MB
==> Installing postgresql@16 dependency: krb5
==> Pouring krb5--1.22.2.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/krb5/1.22.2: 163 files, 5.2MB
==> Installing postgresql@16 dependency: lz4
==> Pouring lz4--1.10.0.arm64_tahoe.bottle.2.tar.gz
🍺  /opt/homebrew/Cellar/lz4/1.10.0: 24 files, 759.9KB
==> Installing postgresql@16 dependency: readline
==> Pouring readline--8.3.3.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/readline/8.3.3: 56 files, 2.6MB
==> Installing postgresql@16 dependency: xz
==> Pouring xz--5.8.3.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/xz/5.8.3: 96 files, 2.6MB
==> Installing postgresql@16 dependency: zstd
==> Pouring zstd--1.5.7_1.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/zstd/1.5.7_1: 32 files, 2.3MB
==> Installing postgresql@16 dependency: json-c
==> Pouring json-c--0.19.arm64_tahoe.bottle.1.tar.gz
🍺  /opt/homebrew/Cellar/json-c/0.19: 34 files, 362KB
==> Installing postgresql@16 dependency: libunistring
==> Pouring libunistring--1.4.2.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/libunistring/1.4.2: 59 files, 5.7MB
==> Installing postgresql@16 dependency: gettext
==> Pouring gettext--1.0.arm64_tahoe.bottle.1.tar.gz
🍺  /opt/homebrew/Cellar/gettext/1.0: 2,499 files, 34.9MB
==> Installing postgresql@16
==> Pouring postgresql@16--16.15.arm64_tahoe.bottle.tar.gz
The files belonging to this database system will be owned by user "carrot".
This user must also own the server process.

The database cluster will be initialized with locale "en_US.UTF-8".
The default text search configuration will be set to "english".

Data page checksums are disabled.

fixing permissions on existing directory /opt/homebrew/var/postgresql@16 ... ok
creating subdirectories ... ok
selecting dynamic shared memory implementation ... posix
selecting default max_connections ... 100
selecting default shared_buffers ... 128MB
selecting default time zone ... Australia/Sydney
creating configuration files ... ok
running bootstrap script ... ok
performing post-bootstrap initialization ... ok
syncing data to disk ... ok


Success. You can now start the database server using:

    '/opt/homebrew/Cellar/postgresql@16/16.15/bin/pg_ctl' -D '/opt/homebrew/var/postgresql@16' -l logfile start

initdb: warning: enabling "trust" authentication for local connections
initdb: hint: You can change this by editing pg_hba.conf or using the option -A, or --auth-local and --auth-host, the next time you run initdb.
🍺  /opt/homebrew/Cellar/postgresql@16/16.15: 3,818 files, 72MB
==> Caveats
==> postgresql@16
This formula has created a default database cluster with:
  initdb --locale=en_US.UTF-8 -E UTF-8 /opt/homebrew/var/postgresql@16

To start postgresql@16 now and restart at login:
  brew services start postgresql@16
Or, if you don't want/need a background service you can just run:
  LC_ALL="en_US.UTF-8" /opt/homebrew/opt/postgresql@16/bin/postgres -D /opt/homebrew/var/postgresql@16
(base) carrot@brians-MacBook-Pro ~ % brew services start postgresql@16
==> Successfully started `postgresql@16` (label: sh.brew.postgresql@16)
(base) carrot@brians-MacBook-Pro ~ % psql --version
psql (PostgreSQL) 18.4 (Postgres.app)
(base) carrot@brians-MacBook-Pro ~ % echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> /Users/carrot/.zprofile
export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"
(base) carrot@brians-MacBook-Pro ~ % createdb aml_platform
(base) carrot@brians-MacBook-Pro ~ % psql aml_platform
psql (16.15 (Homebrew), server 18.4 (Postgres.app))
WARNING: psql major version 16, server major version 18.
         Some psql features might not work.
Type "help" for help.

aml_platform=# CREATE TABLE customers (
    customer_id       VARCHAR(10) PRIMARY KEY,
    customer_type      VARCHAR(20),
    full_name          VARCHAR(150),
    date_of_birth       DATE,
    country             VARCHAR(100),
    residency_country    VARCHAR(100),
    industry            VARCHAR(100),
    occupation          VARCHAR(100),
    annual_income        NUMERIC(14,2),
    account_open_date     DATE,
    customer_status      VARCHAR(20),
    risk_profile        VARCHAR(10)
);
CREATE TABLE
aml_platform=# CREATE TABLE kyc_records (
    kyc_id             SERIAL PRIMARY KEY,
    customer_id         VARCHAR(10) REFERENCES customers(customer_id),
    kyc_status           VARCHAR(20),
    identity_verified     BOOLEAN,
    document_type         VARCHAR(50),
    document_expiry       DATE,
    address_verified      BOOLEAN,
    verification_date      DATE
);
CREATE TABLE
aml_platform=# \dt
           List of relations
 Schema |    Name     | Type  | Owner  
--------+-------------+-------+--------
 public | customers   | table | carrot
 public | kyc_records | table | carrot
(2 rows)

aml_platform=# INSERT INTO customers (customer_id, customer_type, full_name, country, account_open_date, customer_status)
VALUES ('CUST0001', 'Individual', 'Test Nguyen', 'Australia', '2024-01-15', 'Active');
INSERT 0 1
aml_platform=# SELECT * FROM customers;
 customer_id | customer_type |  full_name  | date_of_birth |  country  | residency_country | industry | occupation | annual_income | account_open_date | customer_status | risk_profile 
-------------+---------------+-------------+---------------+-----------+-------------------+----------+------------+---------------+-------------------+-----------------+--------------
 CUST0001    | Individual    | Test Nguyen |               | Australia |                   |          |            |               | 2024-01-15        | Active          | 
(1 row)

...skipping...
 customer_id | customer_type |  full_name  | date_of_birth |  country  | residency_country | industry | occupation | annual_income | account_open_date | customer_status | risk_profile 
-------------+---------------+-------------+---------------+-----------+-------------------+----------+------------+---------------+-------------------+-----------------+--------------
 CUST0001    | Individual    | Test Nguyen |               | Australia |                   |          |            |               | 2024-01-15        | Active          | 
(1 row)

~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
zsh:1: bad pattern: (customer_id,
zsh:1: parse error near `)'
aml_platform=# rified', TRUE, 'Passport', '2024-01-16');INSERT INTO kyc_records (customer_id, kyc_status)
VALUES ('CUST9999', 'Verified');
aml_platform'# ^C
aml_platform=# \pset pager off
Pager usage is off.
aml_platform=# SELECT 1;
 ?column? 
----------
        1
(1 row)

aml_platform=# INSERT INTO kyc_records (customer_id, kyc_status, identity_verified, document_type, verification_date)
VALUES ('CUST0001', 'Verified', TRUE, 'Passport', '2024-01-16');
INSERT 0 1
aml_platform=# INSERT INTO kyc_records (customer_id, kyc_status)
VALUES ('CUST9999', 'Verified');
ERROR:  insert or update on table "kyc_records" violates foreign key constraint "kyc_records_customer_id_fkey"
DETAIL:  Key (customer_id)=(CUST9999) is not present in table "customers".
aml_platform=# DELETE FROM kyc_records WHERE customer_id = 'CUST0001';
DELETE FROM customers WHERE customer_id = 'CUST0001';
DELETE 1
DELETE 1
aml_platform=# \copy customers FROM '/Users/carrot/Downloads/customers.csv' DELIMITER ',' CSV HEADER;
\copy kyc_records FROM '/Users/carrot/Downloads/kyc_records.csv' DELIMITER ',' CSV HEADER;
ERROR:  syntax error at or near "\"
LINE 2: \copy kyc_records FROM '/Users/carrot/Downloads/kyc_records....
        ^
aml_platform=# SELECT COUNT(*) FROM customers;
 count 
-------
     0
(1 row)

aml_platform=# ls -la ~/Downloads/*.csv
aml_platform*# head -3 ~/Downloads/customers.csv
aml_platform*# ^C
aml_platform=# \q
(base) carrot@brians-MacBook-Pro ~ % head -3 ~/Downloads/customers.csv
customer_id,customer_type,full_name,date_of_birth,country,residency_country,industry,occupation,annual_income,account_open_date,customer_status,risk_profile
CUST0001,Individual,William Snyder,1964-08-20,Australia,Australia,Transport,"Engineer, production",87651.75,2026-06-14,Active,
CUST0002,Individual,Hannah Burton,1971-06-18,China,China,Professional Services,Financial planner,53691.85,2024-09-15,Active,
(base) carrot@brians-MacBook-Pro ~ % psql aml_platform
psql (16.15 (Homebrew), server 18.4 (Postgres.app))
WARNING: psql major version 16, server major version 18.
         Some psql features might not work.
Type "help" for help.

aml_platform=# \copy customers FROM '/Users/carrot/Downloads/customers.csv' DELIMITER ',' CSV HEADER;
COPY 500
aml_platform=# SELECT COUNT(*) FROM customers;
 count 
-------
   500
(1 row)

aml_platform=# \copy kyc_records FROM '/Users/carrot/Downloads/kyc_records.csv' DELIMITER ',' CSV HEADER;
ERROR:  invalid input syntax for type integer: "CUST0001"
CONTEXT:  COPY kyc_records, line 2, column kyc_id: "CUST0001"
aml_platform=# SELECT COUNT(*) FROM kyc_records;
 count 
-------
     0
(1 row)

aml_platform=# \copy kyc_records (customer_id, kyc_status, identity_verified, document_type, document_expiry, address_verified, verification_date) FROM '/Users/carrot/Downloads/kyc_records.csv' DELIMITER ',' CSV HEADER;
COPY 500
aml_platform=# SELECT COUNT(*) FROM kyc_records;
 count 
-------
   500
(1 row)

aml_platform=# SELECT industry, COUNT(*) 
FROM customers 
GROUP BY industry 
ORDER BY COUNT(*) DESC;
       industry        | count 
-----------------------+-------
 Construction          |    58
 Retail                |    54
 Manufacturing         |    50
 IT Services           |    48
 Agriculture           |    47
 Hospitality           |    47
 Education             |    44
 Healthcare            |    44
 Professional Services |    41
 Transport             |    36
 Import-Export         |     9
 Money Remittance      |     7
 Real Estate           |     6
 Cryptocurrency        |     5
 Casino/Gaming         |     4
(15 rows)

aml_platform=# SELECT kyc_status, COUNT(*) 
FROM kyc_records 
GROUP BY kyc_status;
 kyc_status | count 
------------+-------
 Failed     |    20
 Verified   |   450
 Pending    |    30
(3 rows)

aml_platform=# SELECT c.customer_id, c.full_name, c.industry, c.country, k.kyc_status, k.document_expiry
FROM customers c
JOIN kyc_records k ON c.customer_id = k.customer_id
WHERE c.industry IN ('Money Remittance', 'Casino/Gaming', 'Real Estate', 'Cryptocurrency', 'Import-Export')
LIMIT 10;
 customer_id |        full_name        |     industry     |    country     | kyc_status | document_expiry 
-------------+-------------------------+------------------+----------------+------------+-----------------
 CUST0006    | Christopher Perez       | Casino/Gaming    | Australia      | Verified   | 2030-09-03
 CUST0008    | Sara Serrano            | Real Estate      | Australia      | Verified   | 2030-11-14
 CUST0014    | John Carter             | Import-Export    | Australia      | Verified   | 2029-07-09
 CUST0028    | Cynthia Gonzales        | Money Remittance | United States  | Verified   | 2031-09-04
 CUST0045    | Donna Matthews          | Import-Export    | Singapore      | Verified   | 2030-09-05
 CUST0049    | Robin Sanford           | Casino/Gaming    | China          | Verified   | 2029-06-14
 CUST0058    | Gary Valencia           | Import-Export    | United Kingdom | Verified   | 2031-02-11
 CUST0070    | Christopher Long        | Real Estate      | UAE            | Pending    | 2031-01-27
 CUST0072    | Michelle Johnson        | Real Estate      | Australia      | Pending    | 2030-11-10
 CUST0079    | Mrs. Veronica Hernandez | Real Estate      | Australia      | Pending    | 2026-10-12
(10 rows)

aml_platform=# CREATE TABLE businesses (
    business_id          VARCHAR(10) PRIMARY KEY,
    company_name          VARCHAR(150),
    industry              VARCHAR(100),
    country                VARCHAR(100),
    incorporation_date      DATE,
    annual_revenue          NUMERIC(14,2),
    annual_expenses         NUMERIC(14,2),
    customer_id            VARCHAR(10) REFERENCES customers(customer_id),
    acn                    VARCHAR(20),
    company_status          VARCHAR(20),   -- Verified / Pending / Review Required
    registered_address       VARCHAR(200),
    business_activity        VARCHAR(150)
);
CREATE TABLE
aml_platform=# SELECT customer_id, full_name, country, account_open_date 
FROM customers 
WHERE customer_type = 'Business';
 customer_id |     full_name      |    country     | account_open_date 
-------------+--------------------+----------------+-------------------
 CUST0020    | Lori Lewis         | Australia      | 2023-10-08
 CUST0023    | Patrick Hayes      | Nigeria        | 2025-09-29
 CUST0046    | Laura Davis        | Nigeria        | 2025-10-07
 CUST0048    | Ashley Barber      | Australia      | 2023-10-26
 CUST0061    | Cheryl Williams    | Singapore      | 2025-11-23
 CUST0070    | Christopher Long   | UAE            | 2026-04-29
 CUST0072    | Michelle Johnson   | Australia      | 2023-12-06
 CUST0073    | David Mendoza      | Australia      | 2025-04-10
 CUST0081    | Larry Moses        | Australia      | 2025-10-28
 CUST0086    | Adam Lozano        | Russia         | 2026-02-13
 CUST0089    | Denise Rice        | Singapore      | 2024-05-13
 CUST0124    | Elizabeth Cantu    | Australia      | 2025-06-01
 CUST0135    | Kevin Jones        | China          | 2023-11-27
 CUST0143    | Maureen Bullock    | United States  | 2024-06-02
 CUST0146    | Cynthia Hall       | Singapore      | 2024-12-13
 CUST0148    | Patrick Wiggins    | Australia      | 2024-09-17
 CUST0153    | Ryan Olson         | Australia      | 2025-11-28
 CUST0154    | Andrew Kerr        | Australia      | 2025-10-29
 CUST0159    | Andre Young        | Australia      | 2026-09-09
 CUST0171    | Tommy Anderson     | Australia      | 2023-10-29
 CUST0189    | Kimberly Schultz   | Australia      | 2023-09-17
 CUST0194    | Joseph Sims        | Australia      | 2025-12-29
 CUST0203    | Mrs. Andrea Davis  | Nigeria        | 2025-02-11
 CUST0207    | Patricia Patterson | UAE            | 2025-06-09
 CUST0216    | Taylor Jennings    | Nigeria        | 2025-05-19
 CUST0221    | Heidi Lynch        | Australia      | 2025-11-07
 CUST0223    | Tiffany Owens      | Australia      | 2026-03-03
aml_platform=# \pset pager off
Pager usage is off.
aml_platform=# \copy (SELECT customer_id, country, account_open_date FROM customers WHERE customer_type = 'Business') TO '/Users/carrot/Downloads/business_customers.csv' DELIMITER ',' CSV HEADER;
COPY 65
aml_platform=# \q
(base) carrot@brians-MacBook-Pro ~ % ls -la ~/Downloads/*.csv
-rw-r--r--@ 1 carrot  staff      1318 12 Jun 14:24 /Users/carrot/Downloads/01_chart_of_accounts.csv
-rw-r--r--@ 1 carrot  staff      3515 12 Jun 14:24 /Users/carrot/Downloads/02_sales_invoices.csv
-rw-r--r--@ 1 carrot  staff      4154 12 Jun 14:24 /Users/carrot/Downloads/03_supplier_bills.csv
-rw-r--r--@ 1 carrot  staff      7183 12 Jun 14:24 /Users/carrot/Downloads/04_bank_statement.csv
-rw-r--r--@ 1 carrot  staff      1811 12 Jun 14:24 /Users/carrot/Downloads/05_contacts.csv
-rw-r--r--@ 1 carrot  staff       519 12 Jun 14:24 /Users/carrot/Downloads/06_payroll_summary.csv
-rw-r--r--@ 1 carrot  staff    107424  1 May 12:54 /Users/carrot/Downloads/advertising.csv
-rw-r--r--  1 carrot  staff      1959 10 Sep 11:47 /Users/carrot/Downloads/business_customers.csv
-rw-r--r--@ 1 carrot  staff  15995117 21 Mar 22:25 /Users/carrot/Downloads/cafes-and-restaurants-with-seating-capacity.csv
-rw-r--r--@ 1 carrot  staff    260602 23 Sep  2025 /Users/carrot/Downloads/Coffe_sales.csv
-rw-r--r--@ 1 carrot  staff     11953 19 May 14:33 /Users/carrot/Downloads/coffee_beans_clean.csv
-rw-r--r--@ 1 carrot  staff      1754 19 May 15:41 /Users/carrot/Downloads/coffee_beans_complete.csv
-rw-r--r--@ 1 carrot  staff     24291 19 May 14:23 /Users/carrot/Downloads/coffee_beans_raw.csv
-rw-r--r--@ 1 carrot  staff      1978 12 May 18:41 /Users/carrot/Downloads/coffee_brewing_data.csv
-rw-r--r--@ 1 carrot  staff      2023 13 Apr 21:20 /Users/carrot/Downloads/coffee_data_clean.csv
-rw-r--r--@ 1 carrot  staff      4960 30 Apr 09:34 /Users/carrot/Downloads/coffee_data.csv
-rw-r--r--@ 1 carrot  staff      3442 19 May 16:18 /Users/carrot/Downloads/coffee_dataset.csv
-rw-r--r--@ 1 carrot  staff    391796 12 Mar  2026 /Users/carrot/Downloads/confirmed_cases_table1_location_0721.csv
-rw-r--r--@ 1 carrot  staff    349818 12 Mar  2026 /Users/carrot/Downloads/confirmed_cases_table1_location.csv
-rw-r--r--@ 1 carrot  staff     60956 10 Sep 11:36 /Users/carrot/Downloads/customers.csv
-rw-r--r--@ 1 carrot  staff     11330  2 May 17:38 /Users/carrot/Downloads/fighters_male_rows.csv
-rw-r--r--@ 1 carrot  staff    530089 11 Mar  2026 /Users/carrot/Downloads/jordan_market_dataset_2026.csv
-rw-r--r--@ 1 carrot  staff     31435 10 Sep 11:36 /Users/carrot/Downloads/kyc_records.csv
-rw-r--r--@ 1 carrot  staff   2947656 23 Mar 10:18 /Users/carrot/Downloads/listings_berlin.csv
-rw-r--r--@ 1 carrot  staff   3881605 14 Apr 10:25 /Users/carrot/Downloads/listings.csv
-rw-r--r--@ 1 carrot  staff     38322 13 Aug 20:34 /Users/carrot/Downloads/matter_360.csv
-rw-r--r--@ 1 carrot  staff       539  3 May 15:49 /Users/carrot/Downloads/spotlight_group4.csv
-rw-r--r--@ 1 carrot  staff      3319  3 May 17:33 /Users/carrot/Downloads/Supabase Snippet UFC Fighters Clean & Enriched Dataset-2.csv
-rw-r--r--@ 1 carrot  staff        46  3 May 17:44 /Users/carrot/Downloads/Supabase Snippet UFC Fighters Clean & Enriched Dataset-3.csv
-rw-r--r--@ 1 carrot  staff      4839  3 May 17:46 /Users/carrot/Downloads/Supabase Snippet UFC Fighters Clean & Enriched Dataset-4.csv
-rw-r--r--@ 1 carrot  staff      6264  3 May 17:48 /Users/carrot/Downloads/Supabase Snippet UFC Fighters Clean & Enriched Dataset-5.csv
-rw-r--r--@ 1 carrot  staff       555  3 May 17:32 /Users/carrot/Downloads/Supabase Snippet UFC Fighters Clean & Enriched Dataset.csv
-rw-r--r--@ 1 carrot  staff      6010  7 May 13:03 /Users/carrot/Downloads/ufc_complete_data-2.csv
-rw-r--r--@ 1 carrot  staff      2356  7 May 13:08 /Users/carrot/Downloads/ufc_complete_data-3.csv
-rw-r--r--@ 1 carrot  staff      7144  7 May 14:42 /Users/carrot/Downloads/ufc_complete_data-4.csv
-rw-r--r--@ 1 carrot  staff     17939  7 May 12:41 /Users/carrot/Downloads/ufc_complete_data.csv
-rw-r--r--@ 1 carrot  staff     10709 21 May 09:21 /Users/carrot/Downloads/ufc_data_new.csv
-rw-r--r--@ 1 carrot  staff     11647 21 May 09:45 /Users/carrot/Downloads/ufc_data_with_coords.csv
-rw-r--r--@ 1 carrot  staff      1241  4 May 22:06 /Users/carrot/Downloads/ufc_data-2.csv
-rw-r--r--@ 1 carrot  staff      2560 20 May 23:28 /Users/carrot/Downloads/ufc_data-3.csv
-rw-r--r--@ 1 carrot  staff      3251  3 May 17:19 /Users/carrot/Downloads/ufc_data.csv
-rw-r--r--@ 1 carrot  staff      6290 28 Apr 19:02 /Users/carrot/Downloads/UFC_Fighter_Data.csv
-rw-r--r--@ 1 carrot  staff     13344  3 May 15:49 /Users/carrot/Downloads/ufc_fighters_processed.csv
-rw-r--r--@ 1 carrot  staff      6668  3 May 16:10 /Users/carrot/Downloads/ufc_fighters.csv
-rw-r--r--@ 1 carrot  staff       192  7 May 15:28 /Users/carrot/Downloads/ufc_statistics.csv
-rw-r--r--@ 1 carrot  staff      5753  3 May 16:45 /Users/carrot/Downloads/ufc_supabase_ready.csv
(base) carrot@brians-MacBook-Pro ~ % ls -la ~/Downloads/businesses.csv
-rw-r--r--@ 1 carrot  staff  12444 10 Sep 11:54 /Users/carrot/Downloads/businesses.csv
(base) carrot@brians-MacBook-Pro ~ % head -3 ~/Downloads/businesses.csv
business_id,company_name,industry,country,incorporation_date,annual_revenue,annual_expenses,customer_id,acn,company_status,registered_address,business_activity
BUS0001,"Brady, Brewer and Smith",Hospitality,Australia,2020-10-05,222552.7,150918.27,CUST0020,854 204 792,Verified,"Apt. 005 57 Laura Foreshore, Lake Michaelchester, TAS, 2611",Extend global systems
BUS0002,Kelly-Robinson,IT Services,Nigeria,2023-03-12,2993413.31,3213201.12,CUST0023,338 617 716,Verified,"Level 6 878 Luna Gully, Fishermouth, NT, 2619",Leverage magnetic functionalities
(base) carrot@brians-MacBook-Pro ~ % psql aml_platform
psql (16.15 (Homebrew), server 18.4 (Postgres.app))
WARNING: psql major version 16, server major version 18.
         Some psql features might not work.
Type "help" for help.

aml_platform=# \copy businesses (business_id, company_name, industry, country, incorporation_date, annual_revenue, annual_expenses, customer_id, acn, company_status, registered_address, business_activity) FROM '/Users/carrot/Downloads/businesses.csv' DELIMITER ',' CSV HEADER;
COPY 65
aml_platform=# SELECT COUNT(*) FROM businesses;
 count 
-------
    65
(1 row)

aml_platform=# CREATE TABLE ownership (
    ownership_id         SERIAL PRIMARY KEY,
    business_id           VARCHAR(10) REFERENCES businesses(business_id),
    owner_id              VARCHAR(10),
    owner_name            VARCHAR(150),
    owner_type            VARCHAR(20),   -- 'Individual' hoặc 'Company'
    ownership_percentage    NUMERIC(5,2),
    is_ubo                BOOLEAN
);
CREATE TABLE
aml_platform=# CREATE TABLE ownership (
    ownership_id         SERIAL PRIMARY KEY,
    business_id           VARCHAR(10) REFERENCES businesses(business_id),
    chain_id              INT,            -- gom toàn bộ các dòng thuộc cùng 1 chuỗi sở hữu của 1 business
    level                 INT,            -- 1 = sở hữu trực tiếp business, 2 = sở hữu owner ở level 1, ...
    owner_id              VARCHAR(20),
    owner_name            VARCHAR(150),
    owner_type            VARCHAR(20),    -- 'Individual' hoặc 'Company'
    ownership_percentage    NUMERIC(5,2),
    is_ubo                BOOLEAN,
    parent_owner_id        VARCHAR(20)    -- owner_id của entity mà owner này đang sở hữu; NULL nếu level = 1 (vì level 1 sở hữu thẳng business)
);
ERROR:  relation "ownership" already exists
aml_platform=# \d ownership
                                                Table "public.ownership"
        Column        |          Type          | Collation | Nullable |                     Default                     
----------------------+------------------------+-----------+----------+-------------------------------------------------
 ownership_id         | integer                |           | not null | nextval('ownership_ownership_id_seq'::regclass)
 business_id          | character varying(10)  |           |          | 
 owner_id             | character varying(10)  |           |          | 
 owner_name           | character varying(150) |           |          | 
 owner_type           | character varying(20)  |           |          | 
 ownership_percentage | numeric(5,2)           |           |          | 
 is_ubo               | boolean                |           |          | 
Indexes:
    "ownership_pkey" PRIMARY KEY, btree (ownership_id)
Foreign-key constraints:
    "ownership_business_id_fkey" FOREIGN KEY (business_id) REFERENCES businesses(business_id)

aml_platform=# \copy ownership (business_id, chain_id, level, owner_id, owner_name, owner_type, ownership_percentage, is_ubo, parent_owner_id) FROM '/Users/carrot/Downloads/ownership.csv' DELIMITER ',' CSV HEADER;
ERROR:  column "chain_id" of relation "ownership" does not exist
aml_platform=# SELECT COUNT(*) FROM ownership;
 count 
-------
     0
(1 row)

aml_platform=# DROP TABLE ownership;
DROP TABLE
aml_platform=# CREATE TABLE ownership (
    ownership_id         SERIAL PRIMARY KEY,
    business_id           VARCHAR(10) REFERENCES businesses(business_id),
    chain_id              INT,
    level                 INT,
    owner_id              VARCHAR(20),
    owner_name            VARCHAR(150),
    owner_type            VARCHAR(20),
    ownership_percentage    NUMERIC(5,2),
    is_ubo                BOOLEAN,
    parent_owner_id        VARCHAR(20)
);
CREATE TABLE
aml_platform=# \copy ownership (business_id, chain_id, level, owner_id, owner_name, owner_type, ownership_percentage, is_ubo, parent_owner_id) FROM '/Users/carrot/Downloads/ownership.csv' DELIMITER ',' CSV HEADER;
COPY 163
aml_platform=# SELECT COUNT(DISTINCT business_id) FROM ownership;
 count 
-------
    65
(1 row)

aml_platform=# WITH RECURSIVE ubo_chain AS (
    SELECT business_id, chain_id, level, owner_id, owner_name, owner_type, is_ubo, parent_owner_id
    FROM ownership
    WHERE level = 1
    UNION ALL
    SELECT o.business_id, o.chain_id, o.level, o.owner_id, o.owner_name, o.owner_type, o.is_ubo, o.parent_owner_id
    FROM ownership o
    JOIN ubo_chain uc ON o.parent_owner_id = uc.owner_id
)
SELECT business_id, owner_name AS ultimate_beneficial_owner
FROM ubo_chain
WHERE is_ubo = TRUE
LIMIT 15;CREATE TABLE screening_results (
    screening_id       SERIAL PRIMARY KEY,
    customer_id         VARCHAR(10) REFERENCES customers(customer_id),
    screening_type       VARCHAR(20),   -- 'PEP' / 'Sanctions' / 'Adverse Media'
    status               VARCHAR(20),   -- Clear / Potential Match / Confirmed Match
    screening_date        DATE,
    match_status          VARCHAR(20),
    match_details          VARCHAR(200)
);
 business_id | ultimate_beneficial_owner 
-------------+---------------------------
 BUS0001     | Kevin Carr
 BUS0002     | Danielle Hobbs
 BUS0003     | Zachary Foster
 BUS0004     | Brianna Ortiz
 BUS0004     | Christopher Lewis
 BUS0004     | Jack Phillips
 BUS0005     | Cynthia Martinez
 BUS0007     | Frank Berger
 BUS0007     | Wendy Washington
 BUS0007     | Peter Braun
 BUS0008     | Cheryl Pierce
 BUS0008     | Sandra Garcia
 BUS0009     | Alan Taylor
 BUS0010     | Nathaniel Edwards
 BUS0010     | Juan Hall
(15 rows)

CREATE TABLE
aml_platform=# \copy screening_results (customer_id, screening_type, status, screening_date, match_status, match_details) FROM '/Users/carrot/Downloads/screening_results.csv' DELIMITER ',' CSV HEADER;
COPY 1500
aml_platform=# SELECT COUNT(*) FROM screening_results;
 count 
-------
  1500
(1 row)

aml_platform=# SELECT screening_type, status, COUNT(*) 
FROM screening_results 
GROUP BY screening_type, status 
ORDER BY screening_type, status;
 screening_type |     status      | count 
----------------+-----------------+-------
 Adverse Media  | Clear           |   447
 Adverse Media  | Confirmed Match |    11
 Adverse Media  | Potential Match |    42
 PEP            | Clear           |   455
 PEP            | Confirmed Match |    14
 PEP            | Potential Match |    31
 Sanctions      | Clear           |   482
 Sanctions      | Confirmed Match |     3
 Sanctions      | Potential Match |    15
(9 rows)

aml_platform=# CREATE TABLE transactions (
    transaction_id       SERIAL PRIMARY KEY,
    customer_id           VARCHAR(10) REFERENCES customers(customer_id),
    transaction_date       DATE,
    transaction_type        VARCHAR(20),   -- Deposit / Withdrawal / Wire Transfer / Cash Deposit
    amount                 NUMERIC(12,2),
    currency               VARCHAR(3) DEFAULT 'AUD',
    counterparty_country    VARCHAR(50),
    channel                VARCHAR(20)    -- Branch / Online / ATM / International Wire
);
CREATE TABLE
aml_platform=# \copy transactions (transaction_id, customer_id, transaction_date, transaction_type, amount, currency, counterparty_country, channel) FROM '/Users/carrot/Downloads/transactions.csv' DELIMITER ',' CSV HEADER;
COPY 13196
aml_platform=# SELECT COUNT(*) FROM transactions;
 count 
-------
 13196
(1 row)

aml_platform=# SELECT COUNT(DISTINCT customer_id) FROM transactions;
 count 
-------
   500
(1 row)

aml_platform=# SELECT customer_id,
       COUNT(*) AS cash_deposit_count,
       SUM(amount) AS total_amount,
       MIN(transaction_date) AS window_start,
       MAX(transaction_date) AS window_end
FROM transactions
WHERE transaction_type = 'Cash Deposit'
  AND amount BETWEEN 9000 AND 9999
GROUP BY customer_id
HAVING COUNT(*) >= 3
   AND MAX(transaction_date) - MIN(transaction_date) <= 7
ORDER BY total_amount DESC;
 customer_id | cash_deposit_count | total_amount | window_start | window_end 
-------------+--------------------+--------------+--------------+------------
 CUST0128    |                  5 |     48800.44 | 2026-07-08   | 2026-07-12
 CUST0427    |                  5 |     48449.99 | 2026-02-07   | 2026-02-11
 CUST0237    |                  5 |     48368.85 | 2026-06-11   | 2026-06-15
 CUST0024    |                  5 |     48025.35 | 2025-11-16   | 2025-11-20
 CUST0212    |                  5 |     47853.66 | 2025-12-25   | 2025-12-29
 CUST0206    |                  5 |     47698.41 | 2026-07-24   | 2026-07-28
 CUST0081    |                  5 |     47629.44 | 2026-05-01   | 2026-05-05
 CUST0049    |                  5 |     47621.71 | 2026-07-02   | 2026-07-06
 CUST0429    |                  5 |     47556.14 | 2025-10-30   | 2025-11-03
 CUST0266    |                  5 |     47549.55 | 2026-05-04   | 2026-05-08
 CUST0333    |                  5 |     47391.89 | 2026-07-20   | 2026-07-24
 CUST0392    |                  5 |     47234.90 | 2026-02-06   | 2026-02-10
 CUST0387    |                  5 |     47209.08 | 2026-03-10   | 2026-03-14
 CUST0297    |                  5 |     47206.50 | 2025-12-18   | 2025-12-22
 CUST0353    |                  5 |     47029.77 | 2026-02-05   | 2026-02-09
 CUST0394    |                  5 |     46956.31 | 2026-02-24   | 2026-02-28
 CUST0253    |                  5 |     46830.80 | 2026-06-12   | 2026-06-16
 CUST0141    |                  5 |     46575.70 | 2025-10-12   | 2025-10-16
 CUST0313    |                  5 |     46564.99 | 2025-11-25   | 2025-11-29
 CUST0140    |                  5 |     46559.63 | 2026-04-23   | 2026-04-27
 CUST0184    |                  5 |     46346.11 | 2025-10-06   | 2025-10-10
 CUST0462    |                  5 |     46302.11 | 2026-02-07   | 2026-02-11
 CUST0428    |                  5 |     46090.39 | 2025-12-14   | 2025-12-18
 CUST0125    |                  5 |     45947.58 | 2026-09-01   | 2026-09-05
 CUST0493    |                  4 |     39139.46 | 2026-08-22   | 2026-08-25
 CUST0465    |                  4 |     38921.09 | 2026-08-20   | 2026-08-23
 CUST0345    |                  4 |     38872.82 | 2026-05-29   | 2026-06-01
 CUST0211    |                  4 |     38653.93 | 2026-07-27   | 2026-07-30
 CUST0377    |                  4 |     38439.10 | 2026-09-08   | 2026-09-11
 CUST0346    |                  4 |     38427.49 | 2026-01-12   | 2026-01-15
 CUST0378    |                  4 |     38383.00 | 2026-08-12   | 2026-08-15
 CUST0294    |                  4 |     38248.81 | 2025-09-23   | 2025-09-26
 CUST0473    |                  4 |     38036.83 | 2026-08-25   | 2026-08-28
 CUST0257    |                  4 |     37999.76 | 2026-01-11   | 2026-01-14
 CUST0259    |                  4 |     37964.30 | 2025-12-25   | 2025-12-28
 CUST0406    |                  4 |     37942.12 | 2026-01-02   | 2026-01-05
 CUST0057    |                  4 |     37907.64 | 2026-04-24   | 2026-04-27
 CUST0127    |                  4 |     37905.88 | 2026-06-19   | 2026-06-22
 CUST0175    |                  4 |     37870.20 | 2025-09-20   | 2025-09-23
 CUST0246    |                  4 |     37847.11 | 2025-12-03   | 2025-12-06
 CUST0214    |                  4 |     37814.64 | 2026-01-06   | 2026-01-09
 CUST0402    |                  4 |     37793.68 | 2026-08-09   | 2026-08-12
 CUST0047    |                  4 |     37722.67 | 2025-11-17   | 2025-11-20
 CUST0398    |                  4 |     37618.01 | 2025-09-20   | 2025-09-23
 CUST0368    |                  4 |     37596.21 | 2026-03-18   | 2026-03-21
 CUST0370    |                  4 |     37595.79 | 2025-12-01   | 2025-12-04
 CUST0255    |                  4 |     37509.72 | 2025-11-28   | 2025-12-01
 CUST0022    |                  4 |     37508.80 | 2025-10-23   | 2025-10-26
 CUST0209    |                  4 |     37479.54 | 2026-04-13   | 2026-04-16
 CUST0409    |                  4 |     37319.06 | 2025-10-23   | 2025-10-26
 CUST0070    |                  4 |     37304.94 | 2026-07-15   | 2026-07-18
 CUST0389    |                  4 |     37175.72 | 2026-07-22   | 2026-07-25
 CUST0384    |                  4 |     37157.55 | 2026-03-28   | 2026-03-31
 CUST0442    |                  3 |     29557.06 | 2026-08-04   | 2026-08-06
 CUST0243    |                  3 |     29539.75 | 2026-03-11   | 2026-03-13
 CUST0375    |                  3 |     29282.31 | 2026-07-16   | 2026-07-18
 CUST0119    |                  3 |     29226.76 | 2025-12-30   | 2026-01-01
 CUST0356    |                  3 |     29194.28 | 2026-02-06   | 2026-02-08
 CUST0138    |                  3 |     29183.64 | 2026-01-29   | 2026-01-31
 CUST0239    |                  3 |     29145.42 | 2026-01-21   | 2026-01-23
 CUST0374    |                  3 |     29098.75 | 2026-07-20   | 2026-07-22
 CUST0423    |                  3 |     29064.31 | 2025-12-25   | 2025-12-27
 CUST0169    |                  3 |     29026.53 | 2026-05-22   | 2026-05-24
 CUST0066    |                  3 |     28920.83 | 2026-06-23   | 2026-06-25
 CUST0361    |                  3 |     28866.47 | 2026-04-22   | 2026-04-24
 CUST0484    |                  3 |     28846.50 | 2025-12-02   | 2025-12-04
 CUST0329    |                  3 |     28801.84 | 2025-11-13   | 2025-11-15
 CUST0244    |                  3 |     28781.81 | 2026-03-30   | 2026-04-01
 CUST0222    |                  3 |     28661.50 | 2026-01-20   | 2026-01-22
 CUST0149    |                  3 |     28659.46 | 2026-06-04   | 2026-06-06
 CUST0170    |                  3 |     28633.64 | 2026-07-18   | 2026-07-20
 CUST0147    |                  3 |     28413.05 | 2025-12-22   | 2025-12-24
 CUST0146    |                  3 |     28375.15 | 2025-10-04   | 2025-10-06
 CUST0010    |                  3 |     28318.89 | 2026-01-23   | 2026-01-25
 CUST0089    |                  3 |     28221.34 | 2026-08-19   | 2026-08-21
 CUST0496    |                  3 |     28125.07 | 2025-11-27   | 2025-11-29
 CUST0383    |                  3 |     28085.30 | 2026-04-11   | 2026-04-13
 CUST0276    |                  3 |     27962.77 | 2026-07-01   | 2026-07-03
 CUST0156    |                  3 |     27902.94 | 2026-04-03   | 2026-04-05
 CUST0103    |                  3 |     27802.31 | 2026-05-27   | 2026-05-29
 CUST0416    |                  3 |     27776.59 | 2026-04-22   | 2026-04-24
 CUST0162    |                  3 |     27771.76 | 2026-02-01   | 2026-02-03
 CUST0020    |                  3 |     27734.44 | 2025-09-14   | 2025-09-16
 CUST0187    |                  3 |     27722.07 | 2026-05-22   | 2026-05-24
 CUST0185    |                  3 |     27447.38 | 2026-05-05   | 2026-05-07
(85 rows)

aml_platform=#  t1.transaction_date AS deposit_date,
aml_platform-#        t1.amount AS deposit_amount,
aml_platform-#        t2.transaction_date AS outflow_date,
aml_platform-#        t2.amount AS outflow_amount,
aml_platform-#        t2.counterparty_country
aml_platform-# FROM transactions t1
aml_platform-# JOIN transactions t2
aml_platform-#   ON t1.customer_id = t2.customer_id
aml_platform-#  AND t2.transaction_type IN ('Wire Transfer', 'Withdrawal')
aml_platform-#  AND t2.transaction_date > t1.transaction_date
aml_platform-#  AND t2.transaction_date <= t1.transaction_date + INTERVAL '2 days'
aml_platform-# WHERE t1.transaction_type = 'Deposit'
aml_platform-#   AND t1.amount >= 8000
aml_platform-# SELECT t1.customer_id,
       t1.transaction_date AS deposit_date,
       t1.amount AS deposit_amount,
       t2.transaction_date AS outflow_date,
       t2.amount AS outflow_amount,
       t2.counterparty_country
FROM transactions t1
JOIN transactions t2
  ON t1.customer_id = t2.customer_id
 AND t2.transaction_type IN ('Wire Transfer', 'Withdrawal')
 AND t2.transaction_date > t1.transaction_date
 AND t2.transaction_date <= t1.transaction_date + INTERVAL '2 days'
WHERE t1.transaction_type = 'Deposit'
  AND t1.amount >= 8000
ORDER BY t1.customer_id, t1.transaction_date;
ERROR:  syntax error at or near "t1"
LINE 1: t1.transaction_date AS deposit_date,
        ^
aml_platform=# SELECT t1.customer_id, t1.transaction_date AS deposit_date, t1.amount AS deposit_amount, t2.transaction_date AS outflow_date, t2.amount AS outflow_amount, t2.counterparty_country FROM transactions t1 JOIN transactions t2 ON t1.customer_id = t2.customer_id AND t2.transaction_type IN ('Wire Transfer', 'Withdrawal') AND t2.transaction_date > t1.transaction_date AND t2.transaction_date <= t1.transaction_date + INTERVAL '2 days' WHERE t1.transaction_type = 'Deposit' AND t1.amount >= 8000 ORDER BY t1.customer_id, t1.transaction_date;
 customer_id | deposit_date | deposit_amount | outflow_date | outflow_amount | counterparty_country 
-------------+--------------+----------------+--------------+----------------+----------------------
 CUST0006    | 2026-07-08   |       17772.17 | 2026-07-10   |       16623.17 | New Zealand
 CUST0018    | 2026-05-29   |       33878.15 | 2026-05-31   |       29422.23 | Iran
 CUST0022    | 2025-12-24   |       19145.61 | 2025-12-26   |       17448.22 | North Korea
 CUST0024    | 2025-10-22   |       29264.28 | 2025-10-24   |       25086.81 | Yemen
 CUST0036    | 2026-07-12   |       25188.87 | 2026-07-14   |       22485.02 | Japan
 CUST0039    | 2025-10-27   |       29558.33 | 2025-10-29   |       25439.20 | United Kingdom
 CUST0041    | 2026-06-09   |       21212.92 | 2026-06-11   |       18572.70 | Singapore
 CUST0047    | 2025-12-26   |       11497.67 | 2025-12-27   |       10551.56 | Syria
 CUST0051    | 2026-04-26   |       36688.40 | 2026-04-27   |       34538.50 | Australia
 CUST0056    | 2025-11-23   |       38361.33 | 2025-11-25   |       34498.67 | Myanmar
 CUST0057    | 2026-09-06   |       23727.35 | 2026-09-07   |       21206.19 | Iran
 CUST0068    | 2026-08-02   |       11550.29 | 2026-08-04   |       10738.01 | North Korea
 CUST0098    | 2026-08-21   |       21159.33 | 2026-08-23   |       19245.00 | Singapore
 CUST0112    | 2026-09-08   |       29387.40 | 2026-09-10   |       28105.67 | United Kingdom
 CUST0128    | 2026-03-08   |       16185.03 | 2026-03-09   |       15708.62 | Iran
 CUST0129    | 2026-08-17   |       35451.06 | 2026-08-18   |       34407.59 | New Zealand
 CUST0134    | 2026-05-03   |       27737.55 | 2026-05-05   |       26879.99 | Singapore
 CUST0136    | 2026-01-10   |       32917.28 | 2026-01-11   |       32427.47 | New Zealand
 CUST0140    | 2026-07-07   |       11848.88 | 2026-07-09   |       11138.22 | North Korea
 CUST0141    | 2026-04-13   |       10714.47 | 2026-04-14   |        9424.98 | United Kingdom
 CUST0145    | 2026-04-29   |       26652.77 | 2026-05-01   |       24158.06 | Syria
 CUST0147    | 2025-10-20   |        8340.52 | 2025-10-22   |        7881.16 | New Zealand
 CUST0158    | 2025-10-23   |       27061.77 | 2025-10-25   |       25899.34 | Yemen
 CUST0160    | 2026-05-27   |       21604.85 | 2026-05-28   |       20956.39 | Japan
 CUST0162    | 2026-07-09   |       32717.63 | 2026-07-11   |       28002.17 | Syria
 CUST0178    | 2026-08-21   |       39701.62 | 2026-08-22   |       37645.45 | Iran
 CUST0180    | 2026-04-05   |       39279.95 | 2026-04-06   |       36078.46 | Syria
Cancel request sent
aml_platform=# SELECT customer_id, COUNT(*) AS cash_deposit_count, SUM(amount) AS total_amount, MIN(transaction_date) AS window_start, MAX(transaction_date) AS window_end FROM transactions WHERE transaction_type = 'Cash Deposit' AND amount BETWEEN 9000 AND 9999 GROUP BY customer_id HAVING COUNT(*) >= 3 AND MAX(transaction_date) - MIN(transaction_date) <= 7 ORDER BY total_amount DESC;
 customer_id | cash_deposit_count | total_amount | window_start | window_end 
-------------+--------------------+--------------+--------------+------------
 CUST0128    |                  5 |     48800.44 | 2026-07-08   | 2026-07-12
 CUST0427    |                  5 |     48449.99 | 2026-02-07   | 2026-02-11
 CUST0237    |                  5 |     48368.85 | 2026-06-11   | 2026-06-15
 CUST0024    |                  5 |     48025.35 | 2025-11-16   | 2025-11-20
 CUST0212    |                  5 |     47853.66 | 2025-12-25   | 2025-12-29
 CUST0206    |                  5 |     47698.41 | 2026-07-24   | 2026-07-28
 CUST0081    |                  5 |     47629.44 | 2026-05-01   | 2026-05-05
 CUST0049    |                  5 |     47621.71 | 2026-07-02   | 2026-07-06
 CUST0429    |                  5 |     47556.14 | 2025-10-30   | 2025-11-03
 CUST0266    |                  5 |     47549.55 | 2026-05-04   | 2026-05-08
 CUST0333    |                  5 |     47391.89 | 2026-07-20   | 2026-07-24
 CUST0392    |                  5 |     47234.90 | 2026-02-06   | 2026-02-10
 CUST0387    |                  5 |     47209.08 | 2026-03-10   | 2026-03-14
 CUST0297    |                  5 |     47206.50 | 2025-12-18   | 2025-12-22
 CUST0353    |                  5 |     47029.77 | 2026-02-05   | 2026-02-09
 CUST0394    |                  5 |     46956.31 | 2026-02-24   | 2026-02-28
 CUST0253    |                  5 |     46830.80 | 2026-06-12   | 2026-06-16
 CUST0141    |                  5 |     46575.70 | 2025-10-12   | 2025-10-16
 CUST0313    |                  5 |     46564.99 | 2025-11-25   | 2025-11-29
 CUST0140    |                  5 |     46559.63 | 2026-04-23   | 2026-04-27
 CUST0184    |                  5 |     46346.11 | 2025-10-06   | 2025-10-10
 CUST0462    |                  5 |     46302.11 | 2026-02-07   | 2026-02-11
 CUST0428    |                  5 |     46090.39 | 2025-12-14   | 2025-12-18
 CUST0125    |                  5 |     45947.58 | 2026-09-01   | 2026-09-05
 CUST0493    |                  4 |     39139.46 | 2026-08-22   | 2026-08-25
 CUST0465    |                  4 |     38921.09 | 2026-08-20   | 2026-08-23
 CUST0345    |                  4 |     38872.82 | 2026-05-29   | 2026-06-01
Cancel request sent
aml_platform=# WITH structuring AS (SELECT customer_id, 1 AS structuring_flag FROM transactions WHERE transaction_type = 'Cash Deposit' AND amount BETWEEN 9000 AND 9999 GROUP BY customer_id HAVING COUNT(*) >= 3), rapid AS (SELECT DISTINCT t1.customer_id, 1 AS rapid_flag FROM transactions t1 JOIN transactions t2 ON t1.customer_id = t2.customer_id AND t2.transaction_type IN ('Wire Transfer','Withdrawal') AND t2.transaction_date > t1.transaction_date AND t2.transaction_date <= t1.transaction_date + INTERVAL '2 days' WHERE t1.transaction_type = 'Deposit' AND t1.amount >= 8000), highrisk AS (SELECT DISTINCT customer_id, 1 AS highrisk_flag FROM transactions WHERE transaction_type = 'Wire Transfer' AND counterparty_country IN ('Iran','North Korea','Myanmar','Syria','Yemen')), screening_flag AS (SELECT DISTINCT customer_id, 1 AS screening_hit_flag FROM screening_results WHERE status IN ('Potential Match','Confirmed Match')) SELECT c.customer_id, COALESCE(s.structuring_flag,0) AS structuring, COALESCE(r.rapid_flag,0) AS rapid_movement, COALESCE(h.highrisk_flag,0) AS high_risk_country, COALESCE(sc.screening_hit_flag,0) AS screening_hit, (COALESCE(s.structuring_flag,0) + COALESCE(r.rapid_flag,0) + COALESCE(h.highrisk_flag,0) + COALESCE(sc.screening_hit_flag,0)) AS risk_score FROM customers c LEFT JOIN structuring s ON c.customer_id = s.customer_id LEFT JOIN rapid r ON c.customer_id = r.customer_id LEFT JOIN highrisk h ON c.customer_id = h.customer_id LEFT JOIN screening_flag sc ON c.customer_id = sc.customer_id ORDER BY risk_score DESC LIMIT 15;
 customer_id | structuring | rapid_movement | high_risk_country | screening_hit | risk_score 
-------------+-------------+----------------+-------------------+---------------+------------
 CUST0185    |           1 |              1 |                 1 |             1 |          4
 CUST0370    |           1 |              1 |                 1 |             1 |          4
 CUST0162    |           1 |              1 |                 1 |             1 |          4
 CUST0184    |           1 |              1 |                 1 |             1 |          4
 CUST0276    |           1 |              1 |                 1 |             1 |          4
 CUST0368    |           1 |              1 |                 1 |             1 |          4
 CUST0140    |           1 |              1 |                 1 |             1 |          4
 CUST0022    |           1 |              1 |                 1 |             1 |          4
 CUST0128    |           1 |              1 |                 1 |             1 |          4
 CUST0024    |           1 |              1 |                 1 |             1 |          4
 CUST0057    |           1 |              1 |                 1 |             1 |          4
 CUST0239    |           1 |              1 |                 1 |             1 |          4
 CUST0047    |           1 |              1 |                 1 |             1 |          4
 CUST0361    |           1 |              1 |                 1 |             1 |          4
 CUST0406    |           1 |              1 |                 1 |             1 |          4
(15 rows)

aml_platform=# WITH structuring AS (SELECT customer_id, 1 AS structuring_flag FROM transactions WHERE transaction_type = 'Cash Deposit' AND amount BETWEEN 9000 AND 9999 GROUP BY customer_id HAVING COUNT(*) >= 3), rapid AS (SELECT DISTINCT t1.customer_id, 1 AS rapid_flag FROM transactions t1 JOIN transactions t2 ON t1.customer_id = t2.customer_id AND t2.transaction_type IN ('Wire Transfer','Withdrawal') AND t2.transaction_date > t1.transaction_date AND t2.transaction_date <= t1.transaction_date + INTERVAL '2 days' WHERE t1.transaction_type = 'Deposit' AND t1.amount >= 8000), highrisk AS (SELECT DISTINCT customer_id, 1 AS highrisk_flag FROM transactions WHERE transaction_type = 'Wire Transfer' AND counterparty_country IN ('Iran','North Korea','Myanmar','Syria','Yemen')), screening_flag AS (SELECT DISTINCT customer_id, 1 AS screening_hit_flag FROM screening_results WHERE status IN ('Potential Match','Confirmed Match')) SELECT c.customer_id, COALESCE(s.structuring_flag,0) AS structuring, COALESCE(r.rapid_flag,0) AS rapid_movement, COALESCE(h.highrisk_flag,0) AS high_risk_country, COALESCE(sc.screening_hit_flag,0) AS screening_hit, (COALESCE(s.structuring_flag,0) + COALESCE(r.rapid_flag,0) + COALESCE(h.highrisk_flag,0) + COALESCE(sc.screening_hit_flag,0)) AS risk_score FROM customers c LEFT JOIN structuring s ON c.customer_id = s.customer_id LEFT JOIN rapid r ON c.customer_id = r.customer_id LEFT JOIN highrisk h ON c.customer_id = h.customer_id LEFT JOIN screening_flag sc ON c.customer_id = sc.customer_id ORDER BY risk_score DESC LIMIT 15;
 customer_id | structuring | rapid_movement | high_risk_country | screening_hit | risk_score 
-------------+-------------+----------------+-------------------+---------------+------------
 CUST0185    |           1 |              1 |                 1 |             1 |          4
 CUST0370    |           1 |              1 |                 1 |             1 |          4
 CUST0162    |           1 |              1 |                 1 |             1 |          4
 CUST0184    |           1 |              1 |                 1 |             1 |          4
 CUST0276    |           1 |              1 |                 1 |             1 |          4
 CUST0368    |           1 |              1 |                 1 |             1 |          4
 CUST0140    |           1 |              1 |                 1 |             1 |          4
 CUST0022    |           1 |              1 |                 1 |             1 |          4
 CUST0128    |           1 |              1 |                 1 |             1 |          4
 CUST0024    |           1 |              1 |                 1 |             1 |          4
 CUST0057    |           1 |              1 |                 1 |             1 |          4
 CUST0239    |           1 |              1 |                 1 |             1 |          4
 CUST0047    |           1 |              1 |                 1 |             1 |          4
 CUST0361    |           1 |              1 |                 1 |             1 |          4
 CUST0406    |           1 |              1 |                 1 |             1 |          4
(15 rows)

aml_platform=# SELECT * FROM customers WHERE customer_id = 'CUST0128';
 customer_id | customer_type |    full_name    | date_of_birth | country | residency_country |   industry    |    occupation     | annual_income | account_open_date | customer_status | risk_profile 
-------------+---------------+-----------------+---------------+---------+-------------------+---------------+-------------------+---------------+-------------------+-----------------+--------------
 CUST0128    | Individual    | Michael Mendoza | 1953-06-15    | Nigeria | Nigeria           | Manufacturing | Systems developer |     140393.37 | 2026-04-10        | Active          | 
(1 row)

Cancel request sent
aml_platform=# SELECT * FROM screening_results WHERE customer_id = 'CUST0128';
 screening_id | customer_id | screening_type |     status      | screening_date |  match_status   |                         match_details                         
--------------+-------------+----------------+-----------------+----------------+-----------------+---------------------------------------------------------------
          382 | CUST0128    | PEP            | Potential Match | 2026-07-22     | Potential Match | Possible name match to PEP register: State Government Advisor
          383 | CUST0128    | Sanctions      | Clear           | 2026-04-28     | Clear           | 
          384 | CUST0128    | Adverse Media  | Clear           | 2026-06-22     | Clear           | 
(3 rows)

Cancel request sent
aml_platform=# SELECT * FROM transactions WHERE customer_id = 'CUST0128' ORDER BY transaction_date;
 transaction_id | customer_id | transaction_date | transaction_type |  amount  | currency | counterparty_country |      channel       
----------------+-------------+------------------+------------------+----------+----------+----------------------+--------------------
           3243 | CUST0128    | 2025-09-10       | Deposit          |  2501.25 | AUD      | Australia            | ATM
           3246 | CUST0128    | 2025-09-18       | Deposit          |  1514.13 | AUD      | New Zealand          | Branch
           3233 | CUST0128    | 2025-12-03       | Deposit          |  1750.10 | AUD      | Japan                | Branch
           3242 | CUST0128    | 2026-01-03       | Cash Deposit     |   820.72 | AUD      | Japan                | Branch
           3238 | CUST0128    | 2026-01-18       | Withdrawal       |  3711.57 | AUD      | Japan                | ATM
           3229 | CUST0128    | 2026-02-06       | Withdrawal       |  4080.43 | AUD      | United States        | ATM
           3244 | CUST0128    | 2026-02-13       | Withdrawal       |  3791.21 | AUD      | United Kingdom       | Branch
           3239 | CUST0128    | 2026-02-28       | Cash Deposit     |   628.76 | AUD      | Japan                | Online
           3255 | CUST0128    | 2026-03-08       | Deposit          | 16185.03 | AUD      | Australia            | Online
           3256 | CUST0128    | 2026-03-09       | Wire Transfer    | 15708.62 | AUD      | Iran                 | International Wire
           3236 | CUST0128    | 2026-03-31       | Deposit          |  4126.04 | AUD      | Australia            | ATM
           3248 | CUST0128    | 2026-04-14       | Wire Transfer    |  3324.85 | AUD      | Australia            | ATM
           3230 | CUST0128    | 2026-06-14       | Cash Deposit     |  1833.63 | AUD      | United States        | Branch
           3245 | CUST0128    | 2026-06-14       | Deposit          |  4760.18 | AUD      | New Zealand          | Branch
           3237 | CUST0128    | 2026-06-15       | Deposit          |  2621.87 | AUD      | Singapore            | Branch
Cancel request sent
aml_platform=# \pset pager off
SELECT * FROM transactions WHERE customer_id = 'CUST0128' ORDER BY transaction_date;
Pager usage is off.
\pset: extra argument "SELECT" ignored
\pset: extra argument "*" ignored
\pset: extra argument "FROM" ignored
\pset: extra argument "transactions" ignored
\pset: extra argument "WHERE" ignored
\pset: extra argument "customer_id" ignored
\pset: extra argument "=" ignored
\pset: extra argument "CUST0128" ignored
\pset: extra argument "ORDER" ignored
\pset: extra argument "BY" ignored
\pset: extra argument "transaction_date;" ignored
aml_platform=# SELECT * FROM transactions WHERE customer_id = 'CUST0128' ORDER BY transaction_date;
 transaction_id | customer_id | transaction_date | transaction_type |  amount  | currency | counterparty_country |      channel       
----------------+-------------+------------------+------------------+----------+----------+----------------------+--------------------
           3243 | CUST0128    | 2025-09-10       | Deposit          |  2501.25 | AUD      | Australia            | ATM
           3246 | CUST0128    | 2025-09-18       | Deposit          |  1514.13 | AUD      | New Zealand          | Branch
           3233 | CUST0128    | 2025-12-03       | Deposit          |  1750.10 | AUD      | Japan                | Branch
           3242 | CUST0128    | 2026-01-03       | Cash Deposit     |   820.72 | AUD      | Japan                | Branch
           3238 | CUST0128    | 2026-01-18       | Withdrawal       |  3711.57 | AUD      | Japan                | ATM
           3229 | CUST0128    | 2026-02-06       | Withdrawal       |  4080.43 | AUD      | United States        | ATM
           3244 | CUST0128    | 2026-02-13       | Withdrawal       |  3791.21 | AUD      | United Kingdom       | Branch
           3239 | CUST0128    | 2026-02-28       | Cash Deposit     |   628.76 | AUD      | Japan                | Online
           3255 | CUST0128    | 2026-03-08       | Deposit          | 16185.03 | AUD      | Australia            | Online
           3256 | CUST0128    | 2026-03-09       | Wire Transfer    | 15708.62 | AUD      | Iran                 | International Wire
           3236 | CUST0128    | 2026-03-31       | Deposit          |  4126.04 | AUD      | Australia            | ATM
           3248 | CUST0128    | 2026-04-14       | Wire Transfer    |  3324.85 | AUD      | Australia            | ATM
           3230 | CUST0128    | 2026-06-14       | Cash Deposit     |  1833.63 | AUD      | United States        | Branch
           3245 | CUST0128    | 2026-06-14       | Deposit          |  4760.18 | AUD      | New Zealand          | Branch
           3237 | CUST0128    | 2026-06-15       | Deposit          |  2621.87 | AUD      | Singapore            | Branch
           3240 | CUST0128    | 2026-06-17       | Cash Deposit     |  2639.45 | AUD      | United States        | Branch
           3235 | CUST0128    | 2026-06-30       | Withdrawal       |  4887.30 | AUD      | New Zealand          | ATM
           3241 | CUST0128    | 2026-07-02       | Wire Transfer    |  3761.64 | AUD      | Japan                | Branch
           3250 | CUST0128    | 2026-07-08       | Cash Deposit     |  9918.64 | AUD      | Australia            | Branch
           3251 | CUST0128    | 2026-07-09       | Cash Deposit     |  9634.58 | AUD      | Australia            | Branch
           3252 | CUST0128    | 2026-07-10       | Cash Deposit     |  9592.74 | AUD      | Australia            | Branch
           3253 | CUST0128    | 2026-07-11       | Cash Deposit     |  9678.44 | AUD      | Australia            | Branch
           3249 | CUST0128    | 2026-07-12       | Wire Transfer    |  1748.69 | AUD      | United Kingdom       | Branch
           3254 | CUST0128    | 2026-07-12       | Cash Deposit     |  9976.04 | AUD      | Australia            | Branch
           3234 | CUST0128    | 2026-07-13       | Wire Transfer    |  2724.04 | AUD      | Japan                | Branch
           3231 | CUST0128    | 2026-07-15       | Wire Transfer    |  4429.62 | AUD      | United Kingdom       | Online
           3232 | CUST0128    | 2026-08-06       | Cash Deposit     |  2281.31 | AUD      | Singapore            | ATM
           3247 | CUST0128    | 2026-08-24       | Deposit          |   381.76 | AUD      | United States        | Branch
(28 rows)

aml_platform=# cd ~/Downloads
aml_platform-# ls aml_dashboard.py
aml_platform-# \q
(base) carrot@brians-MacBook-Pro ~ % cd ~/Downloads
ls aml_dashboard.py
ls: aml_dashboard.py: No such file or directory
(base) carrot@brians-MacBook-Pro Downloads % find ~ -name "aml_dashboard.py" 2>/dev/null
(base) carrot@brians-MacBook-Pro Downloads % cd ~/Downloads
ls aml_dashboard.py
aml_dashboard.py
(base) carrot@brians-MacBook-Pro Downloads % cd ~/Downloads
ls aml_dashboard.py
aml_dashboard.py
(base) carrot@brians-MacBook-Pro Downloads % pip install streamlit sqlalchemy psycopg2-binary pandas plotly
Requirement already satisfied: streamlit in /opt/anaconda3/lib/python3.13/site-packages (1.51.0)
Requirement already satisfied: sqlalchemy in /opt/anaconda3/lib/python3.13/site-packages (2.0.43)
Requirement already satisfied: psycopg2-binary in /opt/anaconda3/lib/python3.13/site-packages (2.9.12)
Requirement already satisfied: pandas in /opt/anaconda3/lib/python3.13/site-packages (2.3.3)
Requirement already satisfied: plotly in /opt/anaconda3/lib/python3.13/site-packages (6.3.0)
Requirement already satisfied: altair!=5.4.0,!=5.4.1,<6,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (5.5.0)
Requirement already satisfied: blinker<2,>=1.5.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (1.9.0)
Requirement already satisfied: cachetools<7,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (5.5.1)
Requirement already satisfied: click<9,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (8.2.1)
Requirement already satisfied: numpy<3,>=1.23 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (2.3.5)
Requirement already satisfied: packaging<26,>=20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (25.0)
Requirement already satisfied: pillow<13,>=7.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (12.0.0)
Requirement already satisfied: protobuf<7,>=3.20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (5.29.3)
Requirement already satisfied: pyarrow<22,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (21.0.0)
Requirement already satisfied: requests<3,>=2.27 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (2.32.5)
Requirement already satisfied: tenacity<10,>=8.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (9.1.2)
Requirement already satisfied: toml<2,>=0.10.1 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (0.10.2)
Requirement already satisfied: typing-extensions<5,>=4.4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (4.15.0)
Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (3.1.45)
Requirement already satisfied: tornado!=6.5.0,<7,>=6.0.3 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (6.5.1)
Requirement already satisfied: python-dateutil>=2.8.2 in /opt/anaconda3/lib/python3.13/site-packages (from pandas) (2.9.0.post0)
Requirement already satisfied: pytz>=2020.1 in /opt/anaconda3/lib/python3.13/site-packages (from pandas) (2025.2)
Requirement already satisfied: tzdata>=2022.7 in /opt/anaconda3/lib/python3.13/site-packages (from pandas) (2025.2)
Requirement already satisfied: jinja2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (3.1.6)
Requirement already satisfied: jsonschema>=3.0 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (4.25.0)
Requirement already satisfied: narwhals>=1.14.2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (2.7.0)
Requirement already satisfied: gitdb<5,>=4.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.12)
Requirement already satisfied: smmap<6,>=3.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.0)
Requirement already satisfied: charset_normalizer<4,>=2 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit) (3.4.4)
Requirement already satisfied: idna<4,>=2.5 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit) (3.11)
Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit) (2.5.0)
Requirement already satisfied: certifi>=2017.4.17 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit) (2025.11.12)
Requirement already satisfied: attrs>=22.2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (25.4.0)
Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (2025.9.1)
Requirement already satisfied: referencing>=0.28.4 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (0.37.0)
Requirement already satisfied: rpds-py>=0.7.1 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (0.28.0)
Requirement already satisfied: six>=1.5 in /opt/anaconda3/lib/python3.13/site-packages (from python-dateutil>=2.8.2->pandas) (1.17.0)
Requirement already satisfied: MarkupSafe>=2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jinja2->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (3.0.2)
(base) carrot@brians-MacBook-Pro Downloads % streamlit run aml_dashboard.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.37.10.103:8501

2026-09-10 12:47:04.513 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:04.524 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:04.530 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:04.530 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:04.533 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:04.547 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:04.548 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:23.135 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:23.147 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:23.154 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:23.154 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:23.155 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:23.178 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:23.179 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:28.495 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:28.512 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:28.521 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:28.522 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:28.523 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:28.541 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:47:28.542 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:50:52.837 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:50:52.853 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:50:52.861 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:50:52.862 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:50:52.863 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:50:52.882 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:50:52.884 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
^C  Stopping...
(base) carrot@brians-MacBook-Pro Downloads % unzip aml_dashboard.zip
cd aml_dashboard
pip install -r requirements.txt
unzip:  cannot find or open aml_dashboard.zip, aml_dashboard.zip.zip or aml_dashboard.zip.ZIP.
Requirement already satisfied: streamlit in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 1)) (1.51.0)
Requirement already satisfied: sqlalchemy in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 2)) (2.0.43)
Requirement already satisfied: psycopg2-binary in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 3)) (2.9.12)
Requirement already satisfied: pandas in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 4)) (2.3.3)
Requirement already satisfied: plotly in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 5)) (6.3.0)
Collecting python-docx (from -r requirements.txt (line 6))
  Downloading python_docx-1.2.0-py3-none-any.whl.metadata (2.0 kB)
Requirement already satisfied: altair!=5.4.0,!=5.4.1,<6,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (5.5.0)
Requirement already satisfied: blinker<2,>=1.5.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (1.9.0)
Requirement already satisfied: cachetools<7,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (5.5.1)
Requirement already satisfied: click<9,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (8.2.1)
Requirement already satisfied: numpy<3,>=1.23 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (2.3.5)
Requirement already satisfied: packaging<26,>=20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (25.0)
Requirement already satisfied: pillow<13,>=7.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (12.0.0)
Requirement already satisfied: protobuf<7,>=3.20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (5.29.3)
Requirement already satisfied: pyarrow<22,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (21.0.0)
Requirement already satisfied: requests<3,>=2.27 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (2.32.5)
Requirement already satisfied: tenacity<10,>=8.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (9.1.2)
Requirement already satisfied: toml<2,>=0.10.1 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (0.10.2)
Requirement already satisfied: typing-extensions<5,>=4.4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (4.15.0)
Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (3.1.45)
Requirement already satisfied: tornado!=6.5.0,<7,>=6.0.3 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (6.5.1)
Requirement already satisfied: python-dateutil>=2.8.2 in /opt/anaconda3/lib/python3.13/site-packages (from pandas->-r requirements.txt (line 4)) (2.9.0.post0)
Requirement already satisfied: pytz>=2020.1 in /opt/anaconda3/lib/python3.13/site-packages (from pandas->-r requirements.txt (line 4)) (2025.2)
Requirement already satisfied: tzdata>=2022.7 in /opt/anaconda3/lib/python3.13/site-packages (from pandas->-r requirements.txt (line 4)) (2025.2)
Requirement already satisfied: jinja2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit->-r requirements.txt (line 1)) (3.1.6)
Requirement already satisfied: jsonschema>=3.0 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit->-r requirements.txt (line 1)) (4.25.0)
Requirement already satisfied: narwhals>=1.14.2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit->-r requirements.txt (line 1)) (2.7.0)
Requirement already satisfied: gitdb<5,>=4.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit->-r requirements.txt (line 1)) (4.0.12)
Requirement already satisfied: smmap<6,>=3.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit->-r requirements.txt (line 1)) (4.0.0)
Requirement already satisfied: charset_normalizer<4,>=2 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit->-r requirements.txt (line 1)) (3.4.4)
Requirement already satisfied: idna<4,>=2.5 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit->-r requirements.txt (line 1)) (3.11)
Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit->-r requirements.txt (line 1)) (2.5.0)
Requirement already satisfied: certifi>=2017.4.17 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit->-r requirements.txt (line 1)) (2025.11.12)
Requirement already satisfied: lxml>=3.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from python-docx->-r requirements.txt (line 6)) (5.3.0)
Requirement already satisfied: attrs>=22.2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit->-r requirements.txt (line 1)) (25.4.0)
Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit->-r requirements.txt (line 1)) (2025.9.1)
Requirement already satisfied: referencing>=0.28.4 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit->-r requirements.txt (line 1)) (0.37.0)
Requirement already satisfied: rpds-py>=0.7.1 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit->-r requirements.txt (line 1)) (0.28.0)
Requirement already satisfied: six>=1.5 in /opt/anaconda3/lib/python3.13/site-packages (from python-dateutil>=2.8.2->pandas->-r requirements.txt (line 4)) (1.17.0)
Requirement already satisfied: MarkupSafe>=2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jinja2->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit->-r requirements.txt (line 1)) (3.0.2)
Downloading python_docx-1.2.0-py3-none-any.whl (252 kB)
Installing collected packages: python-docx
Successfully installed python-docx-1.2.0
(base) carrot@brians-MacBook-Pro aml_dashboard % streamlit run Home.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.37.10.103:8501

2026-09-10 12:51:56.285 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:51:56.292 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:52:06.167 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:52:06.188 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:52:06.190 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:52:10.644 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:52:16.276 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:52:17.676 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:52:31.097 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:52:35.341 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:52:35.354 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:52:44.840 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:52:44.858 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:52:44.861 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:52:49.183 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:52:49.195 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:52:49.196 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:53:02.114 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:53:02.128 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:53:02.130 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:53:06.502 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:53:06.517 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:53:06.519 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:53:11.027 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:53:11.030 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:53:11.047 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:53:11.048 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:53:11.066 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:53:11.067 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:53:11.072 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:54:40.154 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:54:40.164 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:54:51.955 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:55:16.709 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:55:20.302 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:55:21.322 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:57:05.377 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:57:05.389 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:58:18.810 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:58:18.829 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:58:18.831 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:58:20.214 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:58:20.217 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:58:20.235 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:58:20.237 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:58:20.258 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:58:20.259 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:58:20.266 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:58:20.866 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:58:29.225 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 12:58:31.894 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:05:44.867 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:05:44.876 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
^C  Stopping...
(base) carrot@brians-MacBook-Pro aml_dashboard % unzip aml_dashboard.zip && cd aml_dashboard
pip install -r requirements.txt
streamlit run Home.py
unzip:  cannot find or open aml_dashboard.zip, aml_dashboard.zip.zip or aml_dashboard.zip.ZIP.
Requirement already satisfied: streamlit in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 1)) (1.51.0)
Requirement already satisfied: sqlalchemy in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 2)) (2.0.43)
Requirement already satisfied: psycopg2-binary in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 3)) (2.9.12)
Requirement already satisfied: pandas in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 4)) (2.3.3)
Requirement already satisfied: plotly in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 5)) (6.3.0)
Requirement already satisfied: python-docx in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 6)) (1.2.0)
Requirement already satisfied: altair!=5.4.0,!=5.4.1,<6,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (5.5.0)
Requirement already satisfied: blinker<2,>=1.5.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (1.9.0)
Requirement already satisfied: cachetools<7,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (5.5.1)
Requirement already satisfied: click<9,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (8.2.1)
Requirement already satisfied: numpy<3,>=1.23 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (2.3.5)
Requirement already satisfied: packaging<26,>=20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (25.0)
Requirement already satisfied: pillow<13,>=7.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (12.0.0)
Requirement already satisfied: protobuf<7,>=3.20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (5.29.3)
Requirement already satisfied: pyarrow<22,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (21.0.0)
Requirement already satisfied: requests<3,>=2.27 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (2.32.5)
Requirement already satisfied: tenacity<10,>=8.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (9.1.2)
Requirement already satisfied: toml<2,>=0.10.1 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (0.10.2)
Requirement already satisfied: typing-extensions<5,>=4.4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (4.15.0)
Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (3.1.45)
Requirement already satisfied: tornado!=6.5.0,<7,>=6.0.3 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit->-r requirements.txt (line 1)) (6.5.1)
Requirement already satisfied: python-dateutil>=2.8.2 in /opt/anaconda3/lib/python3.13/site-packages (from pandas->-r requirements.txt (line 4)) (2.9.0.post0)
Requirement already satisfied: pytz>=2020.1 in /opt/anaconda3/lib/python3.13/site-packages (from pandas->-r requirements.txt (line 4)) (2025.2)
Requirement already satisfied: tzdata>=2022.7 in /opt/anaconda3/lib/python3.13/site-packages (from pandas->-r requirements.txt (line 4)) (2025.2)
Requirement already satisfied: jinja2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit->-r requirements.txt (line 1)) (3.1.6)
Requirement already satisfied: jsonschema>=3.0 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit->-r requirements.txt (line 1)) (4.25.0)
Requirement already satisfied: narwhals>=1.14.2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit->-r requirements.txt (line 1)) (2.7.0)
Requirement already satisfied: gitdb<5,>=4.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit->-r requirements.txt (line 1)) (4.0.12)
Requirement already satisfied: smmap<6,>=3.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit->-r requirements.txt (line 1)) (4.0.0)
Requirement already satisfied: charset_normalizer<4,>=2 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit->-r requirements.txt (line 1)) (3.4.4)
Requirement already satisfied: idna<4,>=2.5 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit->-r requirements.txt (line 1)) (3.11)
Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit->-r requirements.txt (line 1)) (2.5.0)
Requirement already satisfied: certifi>=2017.4.17 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit->-r requirements.txt (line 1)) (2025.11.12)
Requirement already satisfied: lxml>=3.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from python-docx->-r requirements.txt (line 6)) (5.3.0)
Requirement already satisfied: attrs>=22.2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit->-r requirements.txt (line 1)) (25.4.0)
Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit->-r requirements.txt (line 1)) (2025.9.1)
Requirement already satisfied: referencing>=0.28.4 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit->-r requirements.txt (line 1)) (0.37.0)
Requirement already satisfied: rpds-py>=0.7.1 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit->-r requirements.txt (line 1)) (0.28.0)
Requirement already satisfied: six>=1.5 in /opt/anaconda3/lib/python3.13/site-packages (from python-dateutil>=2.8.2->pandas->-r requirements.txt (line 4)) (1.17.0)
Requirement already satisfied: MarkupSafe>=2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jinja2->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit->-r requirements.txt (line 1)) (3.0.2)

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.37.10.103:8501

2026-09-10 13:41:10.606 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:41:10.615 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:41:13.659 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:41:13.680 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:41:13.682 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:41:16.650 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
^C  Stopping...
(base) carrot@brians-MacBook-Pro aml_dashboard % cd ~/Downloads/aml_dashboard-2
pip install -r requirements.txt
streamlit run Home.py
Requirement already satisfied: streamlit>=1.36 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 1)) (1.51.0)
Requirement already satisfied: pandas>=2.2 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 2)) (2.3.3)
Requirement already satisfied: numpy>=1.26 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 3)) (2.3.5)
Requirement already satisfied: plotly>=5.22 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 4)) (6.3.0)
Requirement already satisfied: sqlalchemy>=2.0 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 5)) (2.0.43)
Requirement already satisfied: psycopg2-binary>=2.9 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 6)) (2.9.12)
Requirement already satisfied: networkx>=3.3 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 7)) (3.5)
Requirement already satisfied: python-docx>=1.1 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 8)) (1.2.0)
Requirement already satisfied: altair!=5.4.0,!=5.4.1,<6,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.5.0)
Requirement already satisfied: blinker<2,>=1.5.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (1.9.0)
Requirement already satisfied: cachetools<7,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.5.1)
Requirement already satisfied: click<9,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (8.2.1)
Requirement already satisfied: packaging<26,>=20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (25.0)
Requirement already satisfied: pillow<13,>=7.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (12.0.0)
Requirement already satisfied: protobuf<7,>=3.20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.29.3)
Requirement already satisfied: pyarrow<22,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (21.0.0)
Requirement already satisfied: requests<3,>=2.27 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (2.32.5)
Requirement already satisfied: tenacity<10,>=8.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (9.1.2)
Requirement already satisfied: toml<2,>=0.10.1 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (0.10.2)
Requirement already satisfied: typing-extensions<5,>=4.4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (4.15.0)
Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (3.1.45)
Requirement already satisfied: tornado!=6.5.0,<7,>=6.0.3 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (6.5.1)
Requirement already satisfied: python-dateutil>=2.8.2 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2.9.0.post0)
Requirement already satisfied: pytz>=2020.1 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2025.2)
Requirement already satisfied: tzdata>=2022.7 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2025.2)
Requirement already satisfied: jinja2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (3.1.6)
Requirement already satisfied: jsonschema>=3.0 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (4.25.0)
Requirement already satisfied: narwhals>=1.14.2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (2.7.0)
Requirement already satisfied: gitdb<5,>=4.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit>=1.36->-r requirements.txt (line 1)) (4.0.12)
Requirement already satisfied: smmap<6,>=3.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit>=1.36->-r requirements.txt (line 1)) (4.0.0)
Requirement already satisfied: charset_normalizer<4,>=2 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (3.4.4)
Requirement already satisfied: idna<4,>=2.5 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (3.11)
Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (2.5.0)
Requirement already satisfied: certifi>=2017.4.17 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (2025.11.12)
Requirement already satisfied: lxml>=3.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from python-docx>=1.1->-r requirements.txt (line 8)) (5.3.0)
Requirement already satisfied: attrs>=22.2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (25.4.0)
Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (2025.9.1)
Requirement already satisfied: referencing>=0.28.4 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (0.37.0)
Requirement already satisfied: rpds-py>=0.7.1 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (0.28.0)
Requirement already satisfied: six>=1.5 in /opt/anaconda3/lib/python3.13/site-packages (from python-dateutil>=2.8.2->pandas>=2.2->-r requirements.txt (line 2)) (1.17.0)
Requirement already satisfied: MarkupSafe>=2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jinja2->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (3.0.2)
2026-09-10 13:42:46.301 
Warning: the config option 'server.enableCORS=false' is not compatible with
'server.enableXsrfProtection=true'.
As a result, 'server.enableCORS' is being overridden to 'true'.

More information:
In order to protect against CSRF attacks, we send a cookie with each request.
To do so, we must specify allowable origins, which places a restriction on
cross-origin resource sharing.

If cross origin resource sharing is required, please disable server.enableXsrfProtection.
            

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.37.10.103:8501
  External URL: http://192.148.228.43:8501

2026-09-10 13:43:11.303 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:43:11.319 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:43:11.334 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:43:11.344 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:43:16.416 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:43:21.191 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:43:21.202 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:43:22.901 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:43:22.908 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:43:47.969 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:43:47.983 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:43:48.000 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:43:48.012 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:43:58.465 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:00.061 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:00.128 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:00.178 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:00.188 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:00.201 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:00.202 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:11.287 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:11.302 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:11.317 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:11.330 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:28.209 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:28.212 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:34.481 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:36.906 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:36.921 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:36.936 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:36.946 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:39.601 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:42.158 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:42.226 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:42.272 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:42.283 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:42.297 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:44:42.298 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:45:33.461 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:45:33.476 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:45:33.491 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:45:33.501 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:47:21.819 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:47:28.336 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:47:30.560 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:47:36.201 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:48:27.971 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:48:27.988 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:48:28.003 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:48:28.015 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
^C  Stopping...
(base) carrot@brians-MacBook-Pro aml_dashboard-2 % cd ~/Downloads/aml_dashboard-3                               
(base) carrot@brians-MacBook-Pro aml_dashboard-3 % pip install -r requirements.txt
streamlit run Home.py
Requirement already satisfied: streamlit>=1.36 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 1)) (1.51.0)
Requirement already satisfied: pandas>=2.2 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 2)) (2.3.3)
Requirement already satisfied: numpy>=1.26 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 3)) (2.3.5)
Requirement already satisfied: plotly>=5.22 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 4)) (6.3.0)
Requirement already satisfied: sqlalchemy>=2.0 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 5)) (2.0.43)
Requirement already satisfied: psycopg2-binary>=2.9 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 6)) (2.9.12)
Requirement already satisfied: networkx>=3.3 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 7)) (3.5)
Requirement already satisfied: python-docx>=1.1 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 8)) (1.2.0)
Requirement already satisfied: altair!=5.4.0,!=5.4.1,<6,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.5.0)
Requirement already satisfied: blinker<2,>=1.5.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (1.9.0)
Requirement already satisfied: cachetools<7,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.5.1)
Requirement already satisfied: click<9,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (8.2.1)
Requirement already satisfied: packaging<26,>=20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (25.0)
Requirement already satisfied: pillow<13,>=7.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (12.0.0)
Requirement already satisfied: protobuf<7,>=3.20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.29.3)
Requirement already satisfied: pyarrow<22,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (21.0.0)
Requirement already satisfied: requests<3,>=2.27 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (2.32.5)
Requirement already satisfied: tenacity<10,>=8.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (9.1.2)
Requirement already satisfied: toml<2,>=0.10.1 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (0.10.2)
Requirement already satisfied: typing-extensions<5,>=4.4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (4.15.0)
Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (3.1.45)
Requirement already satisfied: tornado!=6.5.0,<7,>=6.0.3 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (6.5.1)
Requirement already satisfied: python-dateutil>=2.8.2 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2.9.0.post0)
Requirement already satisfied: pytz>=2020.1 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2025.2)
Requirement already satisfied: tzdata>=2022.7 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2025.2)
Requirement already satisfied: jinja2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (3.1.6)
Requirement already satisfied: jsonschema>=3.0 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (4.25.0)
Requirement already satisfied: narwhals>=1.14.2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (2.7.0)
Requirement already satisfied: gitdb<5,>=4.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit>=1.36->-r requirements.txt (line 1)) (4.0.12)
Requirement already satisfied: smmap<6,>=3.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit>=1.36->-r requirements.txt (line 1)) (4.0.0)
Requirement already satisfied: charset_normalizer<4,>=2 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (3.4.4)
Requirement already satisfied: idna<4,>=2.5 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (3.11)
Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (2.5.0)
Requirement already satisfied: certifi>=2017.4.17 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (2025.11.12)
Requirement already satisfied: lxml>=3.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from python-docx>=1.1->-r requirements.txt (line 8)) (5.3.0)
Requirement already satisfied: attrs>=22.2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (25.4.0)
Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (2025.9.1)
Requirement already satisfied: referencing>=0.28.4 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (0.37.0)
Requirement already satisfied: rpds-py>=0.7.1 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (0.28.0)
Requirement already satisfied: six>=1.5 in /opt/anaconda3/lib/python3.13/site-packages (from python-dateutil>=2.8.2->pandas>=2.2->-r requirements.txt (line 2)) (1.17.0)
Requirement already satisfied: MarkupSafe>=2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jinja2->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (3.0.2)
2026-09-10 13:51:44.309 
Warning: the config option 'server.enableCORS=false' is not compatible with
'server.enableXsrfProtection=true'.
As a result, 'server.enableCORS' is being overridden to 'true'.

More information:
In order to protect against CSRF attacks, we send a cookie with each request.
To do so, we must specify allowable origins, which places a restriction on
cross-origin resource sharing.

If cross origin resource sharing is required, please disable server.enableXsrfProtection.
            

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.37.10.103:8501
  External URL: http://192.148.228.43:8501

2026-09-10 13:52:08.485 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:52:08.498 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:52:08.512 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:52:08.522 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:52:10.859 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:52:16.706 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
^C  Stopping...
(base) carrot@brians-MacBook-Pro aml_dashboard-3 % cd ~/Downloads/aml_dashboard-3
pip install -r requirements.txt
streamlit run Home.py
Requirement already satisfied: streamlit>=1.36 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 1)) (1.51.0)
Requirement already satisfied: pandas>=2.2 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 2)) (2.3.3)
Requirement already satisfied: numpy>=1.26 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 3)) (2.3.5)
Requirement already satisfied: plotly>=5.22 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 4)) (6.3.0)
Requirement already satisfied: sqlalchemy>=2.0 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 5)) (2.0.43)
Requirement already satisfied: psycopg2-binary>=2.9 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 6)) (2.9.12)
Requirement already satisfied: networkx>=3.3 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 7)) (3.5)
Requirement already satisfied: python-docx>=1.1 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 8)) (1.2.0)
Requirement already satisfied: altair!=5.4.0,!=5.4.1,<6,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.5.0)
Requirement already satisfied: blinker<2,>=1.5.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (1.9.0)
Requirement already satisfied: cachetools<7,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.5.1)
Requirement already satisfied: click<9,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (8.2.1)
Requirement already satisfied: packaging<26,>=20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (25.0)
Requirement already satisfied: pillow<13,>=7.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (12.0.0)
Requirement already satisfied: protobuf<7,>=3.20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.29.3)
Requirement already satisfied: pyarrow<22,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (21.0.0)
Requirement already satisfied: requests<3,>=2.27 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (2.32.5)
Requirement already satisfied: tenacity<10,>=8.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (9.1.2)
Requirement already satisfied: toml<2,>=0.10.1 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (0.10.2)
Requirement already satisfied: typing-extensions<5,>=4.4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (4.15.0)
Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (3.1.45)
Requirement already satisfied: tornado!=6.5.0,<7,>=6.0.3 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (6.5.1)
Requirement already satisfied: python-dateutil>=2.8.2 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2.9.0.post0)
Requirement already satisfied: pytz>=2020.1 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2025.2)
Requirement already satisfied: tzdata>=2022.7 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2025.2)
Requirement already satisfied: jinja2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (3.1.6)
Requirement already satisfied: jsonschema>=3.0 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (4.25.0)
Requirement already satisfied: narwhals>=1.14.2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (2.7.0)
Requirement already satisfied: gitdb<5,>=4.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit>=1.36->-r requirements.txt (line 1)) (4.0.12)
Requirement already satisfied: smmap<6,>=3.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit>=1.36->-r requirements.txt (line 1)) (4.0.0)
Requirement already satisfied: charset_normalizer<4,>=2 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (3.4.4)
Requirement already satisfied: idna<4,>=2.5 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (3.11)
Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (2.5.0)
Requirement already satisfied: certifi>=2017.4.17 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (2025.11.12)
Requirement already satisfied: lxml>=3.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from python-docx>=1.1->-r requirements.txt (line 8)) (5.3.0)
Requirement already satisfied: attrs>=22.2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (25.4.0)
Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (2025.9.1)
Requirement already satisfied: referencing>=0.28.4 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (0.37.0)
Requirement already satisfied: rpds-py>=0.7.1 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (0.28.0)
Requirement already satisfied: six>=1.5 in /opt/anaconda3/lib/python3.13/site-packages (from python-dateutil>=2.8.2->pandas>=2.2->-r requirements.txt (line 2)) (1.17.0)
Requirement already satisfied: MarkupSafe>=2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jinja2->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (3.0.2)
2026-09-10 13:53:58.938 
Warning: the config option 'server.enableCORS=false' is not compatible with
'server.enableXsrfProtection=true'.
As a result, 'server.enableCORS' is being overridden to 'true'.

More information:
In order to protect against CSRF attacks, we send a cookie with each request.
To do so, we must specify allowable origins, which places a restriction on
cross-origin resource sharing.

If cross origin resource sharing is required, please disable server.enableXsrfProtection.
            

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.37.10.103:8501
  External URL: http://192.148.228.43:8501

2026-09-10 13:54:07.077 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:54:07.091 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:54:07.105 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:54:07.114 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:54:44.758 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:54:44.775 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:54:44.793 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:54:44.807 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:55:35.496 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:55:40.498 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:55:41.273 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:55:45.073 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:56:09.881 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:56:11.681 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:56:11.684 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:56:26.335 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:56:26.351 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:56:26.365 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:56:26.376 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:57:35.772 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:57:36.617 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:57:36.630 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:57:37.853 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:57:37.855 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:57:39.331 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:57:39.345 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:57:39.362 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:57:39.373 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:57:40.422 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:57:40.425 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:57:47.324 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:57:47.325 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:58:58.826 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:59:36.466 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:59:36.481 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:59:36.496 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:59:36.506 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:59:39.521 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:59:47.845 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:59:47.858 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:59:57.311 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:59:57.377 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:59:57.428 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:59:57.439 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:59:57.454 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 13:59:57.455 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 14:00:47.629 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 14:00:47.631 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 14:00:59.409 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 14:00:59.414 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 14:01:00.092 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 14:07:29.032 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 14:07:29.047 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 14:07:29.063 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 14:07:29.077 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 14:09:40.670 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
^C  Stopping...
(base) carrot@brians-MacBook-Pro aml_dashboard-3 % cd ~/Downloads/aml_dasboard-4
pip install -r requirements.txt
streamlit run Home.py
cd: no such file or directory: /Users/carrot/Downloads/aml_dasboard-4
Requirement already satisfied: streamlit>=1.36 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 1)) (1.51.0)
Requirement already satisfied: pandas>=2.2 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 2)) (2.3.3)
Requirement already satisfied: numpy>=1.26 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 3)) (2.3.5)
Requirement already satisfied: plotly>=5.22 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 4)) (6.3.0)
Requirement already satisfied: sqlalchemy>=2.0 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 5)) (2.0.43)
Requirement already satisfied: psycopg2-binary>=2.9 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 6)) (2.9.12)
Requirement already satisfied: networkx>=3.3 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 7)) (3.5)
Requirement already satisfied: python-docx>=1.1 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 8)) (1.2.0)
Requirement already satisfied: altair!=5.4.0,!=5.4.1,<6,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.5.0)
Requirement already satisfied: blinker<2,>=1.5.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (1.9.0)
Requirement already satisfied: cachetools<7,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.5.1)
Requirement already satisfied: click<9,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (8.2.1)
Requirement already satisfied: packaging<26,>=20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (25.0)
Requirement already satisfied: pillow<13,>=7.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (12.0.0)
Requirement already satisfied: protobuf<7,>=3.20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.29.3)
Requirement already satisfied: pyarrow<22,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (21.0.0)
Requirement already satisfied: requests<3,>=2.27 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (2.32.5)
Requirement already satisfied: tenacity<10,>=8.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (9.1.2)
Requirement already satisfied: toml<2,>=0.10.1 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (0.10.2)
Requirement already satisfied: typing-extensions<5,>=4.4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (4.15.0)
Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (3.1.45)
Requirement already satisfied: tornado!=6.5.0,<7,>=6.0.3 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (6.5.1)
Requirement already satisfied: python-dateutil>=2.8.2 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2.9.0.post0)
Requirement already satisfied: pytz>=2020.1 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2025.2)
Requirement already satisfied: tzdata>=2022.7 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2025.2)
Requirement already satisfied: jinja2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (3.1.6)
Requirement already satisfied: jsonschema>=3.0 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (4.25.0)
Requirement already satisfied: narwhals>=1.14.2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (2.7.0)
Requirement already satisfied: gitdb<5,>=4.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit>=1.36->-r requirements.txt (line 1)) (4.0.12)
Requirement already satisfied: smmap<6,>=3.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit>=1.36->-r requirements.txt (line 1)) (4.0.0)
Requirement already satisfied: charset_normalizer<4,>=2 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (3.4.4)
Requirement already satisfied: idna<4,>=2.5 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (3.11)
Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (2.5.0)
Requirement already satisfied: certifi>=2017.4.17 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (2025.11.12)
Requirement already satisfied: lxml>=3.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from python-docx>=1.1->-r requirements.txt (line 8)) (5.3.0)
Requirement already satisfied: attrs>=22.2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (25.4.0)
Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (2025.9.1)
Requirement already satisfied: referencing>=0.28.4 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (0.37.0)
Requirement already satisfied: rpds-py>=0.7.1 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (0.28.0)
Requirement already satisfied: six>=1.5 in /opt/anaconda3/lib/python3.13/site-packages (from python-dateutil>=2.8.2->pandas>=2.2->-r requirements.txt (line 2)) (1.17.0)
Requirement already satisfied: MarkupSafe>=2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jinja2->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (3.0.2)
2026-09-10 21:15:34.069 
Warning: the config option 'server.enableCORS=false' is not compatible with
'server.enableXsrfProtection=true'.
As a result, 'server.enableCORS' is being overridden to 'true'.

More information:
In order to protect against CSRF attacks, we send a cookie with each request.
To do so, we must specify allowable origins, which places a restriction on
cross-origin resource sharing.

If cross origin resource sharing is required, please disable server.enableXsrfProtection.
            

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.223:8501
  External URL: http://120.19.108.14:8501

2026-09-10 21:15:52.331 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:15:52.343 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:15:52.357 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:15:52.367 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:15:54.377 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:15:55.377 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:15:55.389 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:15:58.085 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:15:58.101 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:15:58.116 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:15:58.127 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:16:00.666 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:16:00.667 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:16:02.465 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:16:02.537 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:16:02.587 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:16:02.599 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:16:02.615 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:16:02.616 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:16:03.414 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:16:03.427 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:16:13.549 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:16:13.563 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:16:13.581 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:16:13.592 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
^C  Stopping...
(base) carrot@brians-MacBook-Pro aml_dashboard-3 % cd ~/Downloads/aml_dashboard-5
pip install -r requirements.txt
streamlit run Home.py
Requirement already satisfied: streamlit>=1.36 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 1)) (1.51.0)
Requirement already satisfied: pandas>=2.2 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 2)) (2.3.3)
Requirement already satisfied: numpy>=1.26 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 3)) (2.3.5)
Requirement already satisfied: plotly>=5.22 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 4)) (6.3.0)
Requirement already satisfied: sqlalchemy>=2.0 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 5)) (2.0.43)
Requirement already satisfied: psycopg2-binary>=2.9 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 6)) (2.9.12)
Requirement already satisfied: networkx>=3.3 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 7)) (3.5)
Requirement already satisfied: python-docx>=1.1 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 8)) (1.2.0)
Requirement already satisfied: altair!=5.4.0,!=5.4.1,<6,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.5.0)
Requirement already satisfied: blinker<2,>=1.5.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (1.9.0)
Requirement already satisfied: cachetools<7,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.5.1)
Requirement already satisfied: click<9,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (8.2.1)
Requirement already satisfied: packaging<26,>=20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (25.0)
Requirement already satisfied: pillow<13,>=7.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (12.0.0)
Requirement already satisfied: protobuf<7,>=3.20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.29.3)
Requirement already satisfied: pyarrow<22,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (21.0.0)
Requirement already satisfied: requests<3,>=2.27 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (2.32.5)
Requirement already satisfied: tenacity<10,>=8.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (9.1.2)
Requirement already satisfied: toml<2,>=0.10.1 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (0.10.2)
Requirement already satisfied: typing-extensions<5,>=4.4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (4.15.0)
Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (3.1.45)
Requirement already satisfied: tornado!=6.5.0,<7,>=6.0.3 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (6.5.1)
Requirement already satisfied: python-dateutil>=2.8.2 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2.9.0.post0)
Requirement already satisfied: pytz>=2020.1 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2025.2)
Requirement already satisfied: tzdata>=2022.7 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2025.2)
Requirement already satisfied: jinja2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (3.1.6)
Requirement already satisfied: jsonschema>=3.0 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (4.25.0)
Requirement already satisfied: narwhals>=1.14.2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (2.7.0)
Requirement already satisfied: gitdb<5,>=4.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit>=1.36->-r requirements.txt (line 1)) (4.0.12)
Requirement already satisfied: smmap<6,>=3.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit>=1.36->-r requirements.txt (line 1)) (4.0.0)
Requirement already satisfied: charset_normalizer<4,>=2 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (3.4.4)
Requirement already satisfied: idna<4,>=2.5 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (3.11)
Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (2.5.0)
Requirement already satisfied: certifi>=2017.4.17 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (2025.11.12)
Requirement already satisfied: lxml>=3.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from python-docx>=1.1->-r requirements.txt (line 8)) (5.3.0)
Requirement already satisfied: attrs>=22.2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (25.4.0)
Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (2025.9.1)
Requirement already satisfied: referencing>=0.28.4 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (0.37.0)
Requirement already satisfied: rpds-py>=0.7.1 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (0.28.0)
Requirement already satisfied: six>=1.5 in /opt/anaconda3/lib/python3.13/site-packages (from python-dateutil>=2.8.2->pandas>=2.2->-r requirements.txt (line 2)) (1.17.0)
Requirement already satisfied: MarkupSafe>=2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jinja2->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (3.0.2)

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.223:8501

2026-09-10 21:37:00.759 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:37:00.771 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:37:00.785 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:37:00.794 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:37:06.838 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:37:08.041 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:37:08.054 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:37:09.147 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:37:09.222 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:37:09.271 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:37:09.284 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:37:09.300 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:37:09.301 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:38:15.909 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:38:15.978 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:38:16.028 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:38:16.038 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:38:16.053 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:38:16.054 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
^C  Stopping...
(base) carrot@brians-MacBook-Pro aml_dashboard-5 % cd ~/Download/aml_dashboard-6
cd: no such file or directory: /Users/carrot/Download/aml_dashboard-6
(base) carrot@brians-MacBook-Pro aml_dashboard-5 % cd ~/Downloads/aml_dashboard-6
pip install -r requirements.txt
streamlit run Home.py
Requirement already satisfied: streamlit>=1.36 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 1)) (1.51.0)
Requirement already satisfied: pandas>=2.2 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 2)) (2.3.3)
Requirement already satisfied: numpy>=1.26 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 3)) (2.3.5)
Requirement already satisfied: plotly>=5.22 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 4)) (6.3.0)
Requirement already satisfied: sqlalchemy>=2.0 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 5)) (2.0.43)
Requirement already satisfied: psycopg2-binary>=2.9 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 6)) (2.9.12)
Requirement already satisfied: networkx>=3.3 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 7)) (3.5)
Requirement already satisfied: python-docx>=1.1 in /opt/anaconda3/lib/python3.13/site-packages (from -r requirements.txt (line 8)) (1.2.0)
Requirement already satisfied: altair!=5.4.0,!=5.4.1,<6,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.5.0)
Requirement already satisfied: blinker<2,>=1.5.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (1.9.0)
Requirement already satisfied: cachetools<7,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.5.1)
Requirement already satisfied: click<9,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (8.2.1)
Requirement already satisfied: packaging<26,>=20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (25.0)
Requirement already satisfied: pillow<13,>=7.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (12.0.0)
Requirement already satisfied: protobuf<7,>=3.20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (5.29.3)
Requirement already satisfied: pyarrow<22,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (21.0.0)
Requirement already satisfied: requests<3,>=2.27 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (2.32.5)
Requirement already satisfied: tenacity<10,>=8.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (9.1.2)
Requirement already satisfied: toml<2,>=0.10.1 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (0.10.2)
Requirement already satisfied: typing-extensions<5,>=4.4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (4.15.0)
Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (3.1.45)
Requirement already satisfied: tornado!=6.5.0,<7,>=6.0.3 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit>=1.36->-r requirements.txt (line 1)) (6.5.1)
Requirement already satisfied: python-dateutil>=2.8.2 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2.9.0.post0)
Requirement already satisfied: pytz>=2020.1 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2025.2)
Requirement already satisfied: tzdata>=2022.7 in /opt/anaconda3/lib/python3.13/site-packages (from pandas>=2.2->-r requirements.txt (line 2)) (2025.2)
Requirement already satisfied: jinja2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (3.1.6)
Requirement already satisfied: jsonschema>=3.0 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (4.25.0)
Requirement already satisfied: narwhals>=1.14.2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (2.7.0)
Requirement already satisfied: gitdb<5,>=4.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit>=1.36->-r requirements.txt (line 1)) (4.0.12)
Requirement already satisfied: smmap<6,>=3.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit>=1.36->-r requirements.txt (line 1)) (4.0.0)
Requirement already satisfied: charset_normalizer<4,>=2 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (3.4.4)
Requirement already satisfied: idna<4,>=2.5 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (3.11)
Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (2.5.0)
Requirement already satisfied: certifi>=2017.4.17 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit>=1.36->-r requirements.txt (line 1)) (2025.11.12)
Requirement already satisfied: lxml>=3.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from python-docx>=1.1->-r requirements.txt (line 8)) (5.3.0)
Requirement already satisfied: attrs>=22.2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (25.4.0)
Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (2025.9.1)
Requirement already satisfied: referencing>=0.28.4 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (0.37.0)
Requirement already satisfied: rpds-py>=0.7.1 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (0.28.0)
Requirement already satisfied: six>=1.5 in /opt/anaconda3/lib/python3.13/site-packages (from python-dateutil>=2.8.2->pandas>=2.2->-r requirements.txt (line 2)) (1.17.0)
Requirement already satisfied: MarkupSafe>=2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jinja2->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit>=1.36->-r requirements.txt (line 1)) (3.0.2)

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.223:8501

2026-09-10 21:42:55.938 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:42:55.951 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:42:55.965 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:42:55.975 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:43:02.355 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:49:27.521 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:49:27.532 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:49:31.639 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:49:31.653 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:49:35.397 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:49:38.795 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 21:49:38.801 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 22:26:13.257 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-09-10 22:26:13.260 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.

