# Primerjava baz podatkov: PostgreSQL vs MySQL

Projekt za predmet Sistemska podpora - primerjava performanc PostgreSQL in MySQL baz podatkov na Linux (Fedora) in FreeBSD sistemih.

## Avtor
Arnož Siljan, Univerza v Mariboru - FERI

## Opis
Projekt primerja performanco PostgreSQL in MySQL baz podatkov pri:
- INSERT operacijah
- SELECT poizvedbah (Simple, COUNT, agregacija, LIKE, range, ORDER BY)
- Optimizaciji z indeksi

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
```

### MySQL
```bash
sudo dnf install -y mysql-server
sudo systemctl enable mysqld
sudo systemctl start mysqld
sudo mysql_secure_installation
```

## Uporaba

### 1. Setup testnih podatkov (100,000 zapisov)
```bash
python3 setup_test_data.py
```

### 2. Benchmark brez optimizacije
```bash
python3 benchmark.py
```

### 3. Dodajanje indeksov in optimizacija
```bash
python3 optimize.py
```

### 4. Benchmark po optimizaciji
```bash
python3 benchmark.py
```

## Rezultati

### INSERT operacije
- MySQL: ~75% hitrejši od PostgreSQL

### SELECT operacije (brez indeksov)
- PostgreSQL: 20-84% hitrejši od MySQL pri večini poizvedb

### Izboljšave z indeksi
- ORDER BY: do 16x hitrejši (obe bazi)
- Range poizvedbe: ~27% izboljšava

## Struktura projekta
```
.
├── setup_test_data.py   # Ustvari tabele in vstavi testne podatke
├── benchmark.py         # Primerja performanco različnih poizvedb
└── optimize.py          # Doda indekse in optimizira tabele
```

## Licence
MIT
