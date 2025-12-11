# Primerjava baz podatkov: PostgreSQL vs MySQL vs MariaDB

Projekt za predmet Sistemska podpora - primerjava performanc PostgreSQL, MySQL in MariaDB baz podatkov na Linux (Fedora) in FreeBSD sistemih.

## Avtor
Arnož Siljan, Univerza v Mariboru - FERI

## Opis
Projekt primerja performanco treh vodilnih odprtokodnih baz podatkov:
- **PostgreSQL** - Napredna relacijska baza z močnimi funkcionalnostmi
- **MySQL** - Najbolj razširjena odprtokodna baza podatkov
- **MariaDB** - Fork MySQL z izboljšavami in dodatnimi funkcionalnostmi

### Testirane operacije
- **INSERT operacije** - Vstavljanje 100,000 zapisov
- **SELECT poizvedbe**:
  - Simple SELECT (iskanje po ID)
  - COUNT (štetje zapisov)
  - AVG agregacija (grupiranje in povprečje)
  - LIKE iskanje (iskanje po delu besedila)
  - Range poizvedbe (iskanje v obsegu vrednosti)
  - ORDER BY (sortiranje)
- **Optimizacija** - Dodajanje indeksov in analiza učinka

## Potrebne knjižnice
```bash
pip install psycopg2-binary mysql-connector-python
```

## Namestitev baz (Fedora)

### PostgreSQL
```bash
sudo dnf install -y postgresql postgresql-server postgresql-contrib
sudo postgresql-setup --initdb
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Konfiguracija avtentikacije
sudo nano /var/lib/pgsql/data/pg_hba.conf
# Spremeni 'ident' v 'md5' za IPv4 in IPv6 povezave
sudo systemctl restart postgresql

# Nastavi geslo
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'testpass';"
sudo -u postgres createdb testdb
```

### MySQL
```bash
sudo dnf install -y mysql-server
sudo systemctl enable mysqld
sudo systemctl start mysqld
sudo mysql_secure_installation

# Ustvari bazo
sudo mysql -u root -p
CREATE DATABASE testdb;
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'testpass';
GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'localhost';
FLUSH PRIVILEGES;
exit;
```

### MariaDB
```bash
# Najprej odstrani MySQL
sudo systemctl stop mysqld
sudo dnf remove -y mysql-server
sudo rm -rf /var/lib/mysql/*

# Namesti MariaDB
sudo dnf install -y mariadb-server
sudo mariadb-install-db --user=mysql
sudo systemctl enable mariadb
sudo systemctl start mariadb
sudo mariadb-secure-installation

# Ustvari bazo
sudo mariadb -u root -p
CREATE DATABASE testdb;
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'testpass';
GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'localhost';
FLUSH PRIVILEGES;
exit;
```

## Uporaba

### PostgreSQL vs MySQL

#### 1. Setup testnih podatkov
```bash
python3 setup_test_data.py
```

#### 2. Benchmark brez optimizacije
```bash
python3 benchmark.py
```

#### 3. Dodajanje indeksov
```bash
python3 optimize.py
```

#### 4. Benchmark po optimizaciji
```bash
python3 benchmark.py
```

### PostgreSQL vs MariaDB

#### 1. Setup testnih podatkov
```bash
python3 setup_mariadb_test.py
```

#### 2. Benchmark brez optimizacije
```bash
python3 benchmark_mariadb.py
```

#### 3. Dodajanje indeksov
```bash
python3 optimize_mariadb.py
```

#### 4. Benchmark po optimizaciji
```bash
python3 benchmark_mariadb.py
```

## Rezultati (Fedora Linux)

### INSERT operacije (100,000 zapisov)
| Baza podatkov | Čas | Records/s | Primerjava |
|---------------|-----|-----------|------------|
| PostgreSQL | 5.22s | 19,167 | baseline |
| MySQL | 1.29s | 77,337 | **75% hitrejši** |
| MariaDB | 0.71s | 141,721 | **90% hitrejši** |

**Ugotovitev:** MariaDB in MySQL sta bistveno hitrejša pri masovnih INSERT operacijah.

### SELECT operacije (brez indeksov)
| Poizvedba | PostgreSQL | MySQL | MariaDB | Najhitrejši |
|-----------|------------|-------|---------|-------------|
| Simple SELECT | 0.52ms | 3.23ms | 0.64ms | PostgreSQL |
| COUNT | 4.91ms | 6.20ms | 9.07ms | PostgreSQL |
| AVG agregacija | 15.61ms | 42.99ms | 30.08ms | PostgreSQL |
| LIKE iskanje | 9.06ms | 26.80ms | 17.31ms | PostgreSQL |
| Range | 25.02ms | 32.99ms | 27.15ms | PostgreSQL |
| ORDER BY | 16.47ms | 28.97ms | 21.42ms | PostgreSQL |

**Ugotovitev:** PostgreSQL je hitrejši pri vseh SELECT operacijah (20-84% hitrejši).

### Izboljšave z indeksi
| Operacija | Baza | Pred | Po | Izboljšava |
|-----------|------|------|-----|-----------|
| ORDER BY | PostgreSQL | 16.47ms | 0.73ms | **13x hitrejši** |
| ORDER BY | MySQL | 28.97ms | 1.76ms | **16x hitrejši** |
| ORDER BY | MariaDB | 21.42ms | 1.61ms | **13x hitrejši** |
| Simple SELECT | MariaDB | 0.64ms | 0.13ms | **5x hitrejši** |
| Range | PostgreSQL | 25.02ms | 18.19ms | 27% hitrejši |

**Ugotovitev:** Indeksi drastično izboljšajo performanco, posebej pri sortiranju.

### Velikost podatkov (100,000 zapisov)
| Baza podatkov | Velikost tabele users |
|---------------|---------------------|
| PostgreSQL | 18 MB |
| MySQL | 19.06 MB |
| MariaDB | 19.06 MB |

**Ugotovitev:** Vse tri baze uporabljajo podobno količino prostora.

## Zaključki

### Kdaj uporabiti PostgreSQL?
- **Kompleksne poizvedbe** in agregacije
- **ACID compliance** je kritična
- **Potrebujete napredne funkcionalnosti** (JSON, arrays, custom types)
- **Read-heavy workloads**

### Kdaj uporabiti MySQL/MariaDB?
- **Masovno vstavljanje podatkov**
- **Preproste, hitre poizvedbe**
- **Write-heavy workloads**
- **Potrebujete visoko kompatibilnost** (MySQL ekosistem)

### MariaDB vs MySQL
- MariaDB je **hitrejši pri INSERT** operacijah
- MariaDB ima **več funkcionalnosti** (dodatni storage engines)
- MariaDB je **fully open-source** (brez Oracle licenc)
- Obe bazi sta **kompatibilni** za večino aplikacij

## Struktura projekta
```
.
├── README.md
├── setup_test_data.py        # PostgreSQL vs MySQL setup
├── benchmark.py               # PostgreSQL vs MySQL benchmark
├── optimize.py                # PostgreSQL vs MySQL optimizacija
├── setup_mariadb_test.py     # PostgreSQL vs MariaDB setup
├── benchmark_mariadb.py       # PostgreSQL vs MariaDB benchmark
└── optimize_mariadb_py       # PostgreSQL vs MariaDB optimizacija
```

## Fedora vs FreeBSD primerjava

Primerjava PostgreSQL performanc med Fedora Linux in FreeBSD operacijskim sistemom.

### Namestitev (FreeBSD)
```bash
# PostgreSQL
pkg install postgresql16-server postgresql16-client
sysrc postgresql_enable="YES"
service postgresql initdb
service postgresql start

# Konfiguracija za oddaljeni dostop
# Uredi /var/db/postgres/data16/postgresql.conf
listen_addresses = '*'

# Uredi /var/db/postgres/data16/pg_hba.conf
host    all     all     192.168.0.0/24    md5

service postgresql restart
```

### Uporaba (iz Fedore)
```bash
# Setup in primerjava
python3 compare_fedora_freebsd.py

# Optimizacija
python3 optimize_freebsd.py

# Benchmark po optimizaciji
python3 benchmark_only_freebsd.py
```

### Rezultati Fedora vs FreeBSD

#### INSERT operacije (100,000 zapisov)
| Platforma | Čas | Records/s |
|-----------|-----|-----------|
| Fedora (lokalno) | 10.30s | 9,705 |
| FreeBSD (preko mreže) | 160.61s | 623 |

**Ugotovitev:** Fedora 93.6% hitrejši - mrežna latenca močno vpliva na INSERT performance.

#### SELECT operacije (brez indeksov)
| Poizvedba | Fedora | FreeBSD | Hitrejši |
|-----------|---------|---------|----------|
| Simple SELECT | 2.55ms | 5.84ms | Fedora (56%) |
| COUNT | 8.67ms | 9.12ms | Fedora (5%) |
| AVG agregacija | 20.39ms | 23.29ms | Fedora (12%) |
| LIKE iskanje | 10.78ms | 18.55ms | Fedora (42%) |
| Range | 31.66ms | 65.01ms | Fedora (51%) |
| ORDER BY | 19.43ms | 17.27ms | **FreeBSD (11%)** |

#### SELECT operacije (z indeksi)
| Poizvedba | Fedora | FreeBSD | Izboljšava Fedora | Izboljšava FreeBSD |
|-----------|---------|---------|-------------------|---------------------|
| Simple SELECT | 0.75ms | 3.38ms | 3.4x hitrejši | 1.7x hitrejši |
| ORDER BY | 0.45ms | 3.50ms | **43x hitrejši** | **5x hitrejši** |
| Range | 16.68ms | 79.74ms | 1.9x hitrejši | - |

#### Ustvarjanje indeksov
| Platforma | Čas za 3 indekse |
|-----------|------------------|
| Fedora | 0.33s |
| FreeBSD | 0.55s |

### Zaključki primerjave OS

**Linux (Fedora) prednosti:**
- Hitrejši pri lokalnih operacijah
- Boljša podpora za networking/remote access
- Večja izboljšava z indeksi (43x vs 5x pri ORDER BY)

**FreeBSD prednosti:**
- Zmeren pri ORDER BY poizvedbah (brez indeksov)
- Stabilen performance
- Boljša izolacija sistema

**Mrežna latenca:**
- INSERT operacije so **16x počasnejše** preko mreže
- SELECT operacije so **2-5x počasnejše** preko mreže
- Za produkcijsko okolje je lokalni dostop kritičen

## Licence
MIT
