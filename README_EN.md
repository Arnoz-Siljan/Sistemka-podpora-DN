# Database Performance Comparison: PostgreSQL vs MySQL vs MariaDB

System Support course project - Performance comparison of PostgreSQL, MySQL, and MariaDB databases on Linux (Fedora) and FreeBSD systems.

## Author
Arnož Šiljan, University of Maribor - FERI

## Description
This project compares the performance of three leading open-source databases:
- **PostgreSQL** - Advanced relational database with powerful features
- **MySQL** - World's most popular open-source database
- **MariaDB** - MySQL fork with improvements and additional features

### Tested Operations
- **INSERT operations** - Inserting 100,000 records
- **SELECT queries**:
  - Simple SELECT (search by ID)
  - COUNT (counting records)
  - AVG aggregation (grouping and averaging)
  - LIKE search (partial text search)
  - Range queries (searching within value ranges)
  - ORDER BY (sorting)
- **Optimization** - Adding indexes and analyzing their impact

## Required Libraries
```bash
pip install psycopg2-binary mysql-connector-python
```

## Database Installation (Fedora)

### PostgreSQL
```bash
sudo dnf install -y postgresql postgresql-server postgresql-contrib
sudo postgresql-setup --initdb
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Authentication configuration
sudo nano /var/lib/pgsql/data/pg_hba.conf
# Change 'ident' to 'md5' for IPv4 and IPv6 connections
sudo systemctl restart postgresql

# Set password
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'testpass';"
sudo -u postgres createdb testdb
```

### MySQL
```bash
sudo dnf install -y mysql-server
sudo systemctl enable mysqld
sudo systemctl start mysqld
sudo mysql_secure_installation

# Create database
sudo mysql -u root -p
CREATE DATABASE testdb;
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'testpass';
GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'localhost';
FLUSH PRIVILEGES;
exit;
```

### MariaDB
```bash
# First remove MySQL
sudo systemctl stop mysqld
sudo dnf remove -y mysql-server
sudo rm -rf /var/lib/mysql/*

# Install MariaDB
sudo dnf install -y mariadb-server
sudo mariadb-install-db --user=mysql
sudo systemctl enable mariadb
sudo systemctl start mariadb
sudo mariadb-secure-installation

# Create database
sudo mariadb -u root -p
CREATE DATABASE testdb;
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'testpass';
GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'localhost';
FLUSH PRIVILEGES;
exit;
```

## Usage

### PostgreSQL vs MySQL

#### 1. Setup test data
```bash
python3 setup_test_data.py
```

#### 2. Benchmark without optimization
```bash
python3 benchmark.py
```

#### 3. Add indexes
```bash
python3 optimize.py
```

#### 4. Benchmark after optimization
```bash
python3 benchmark.py
```

### PostgreSQL vs MariaDB

#### 1. Setup test data
```bash
python3 setup_mariadb_test.py
```

#### 2. Benchmark without optimization
```bash
python3 benchmark_mariadb.py
```

#### 3. Add indexes
```bash
python3 optimize_mariadb.py
```

#### 4. Benchmark after optimization
```bash
python3 benchmark_mariadb.py
```

## Results (Fedora Linux)

### INSERT Operations (100,000 records)
| Database | Time | Records/s | Comparison |
|----------|------|-----------|------------|
| PostgreSQL | 5.22s | 19,167 | baseline |
| MySQL | 1.29s | 77,337 | **75% faster** |
| MariaDB | 0.71s | 141,721 | **90% faster** |

**Finding:** MariaDB and MySQL are significantly faster for bulk INSERT operations.

### SELECT Operations (without indexes)
| Query | PostgreSQL | MySQL | MariaDB | Fastest |
|-------|------------|-------|---------|---------|
| Simple SELECT | 0.52ms | 3.23ms | 0.64ms | PostgreSQL |
| COUNT | 4.91ms | 6.20ms | 9.07ms | PostgreSQL |
| AVG aggregation | 15.61ms | 42.99ms | 30.08ms | PostgreSQL |
| LIKE search | 9.06ms | 26.80ms | 17.31ms | PostgreSQL |
| Range | 25.02ms | 32.99ms | 27.15ms | PostgreSQL |
| ORDER BY | 16.47ms | 28.97ms | 21.42ms | PostgreSQL |

**Finding:** PostgreSQL is faster for all SELECT operations (20-84% faster).

### Performance Improvements with Indexes
| Operation | Database | Before | After | Improvement |
|-----------|----------|--------|-------|-------------|
| ORDER BY | PostgreSQL | 16.47ms | 0.73ms | **13x faster** |
| ORDER BY | MySQL | 28.97ms | 1.76ms | **16x faster** |
| ORDER BY | MariaDB | 21.42ms | 1.61ms | **13x faster** |
| Simple SELECT | MariaDB | 0.64ms | 0.13ms | **5x faster** |
| Range | PostgreSQL | 25.02ms | 18.19ms | 27% faster |

**Finding:** Indexes dramatically improve performance, especially for sorting operations.

### Data Size (100,000 records)
| Database | Users Table Size |
|----------|------------------|
| PostgreSQL | 18 MB |
| MySQL | 19.06 MB |
| MariaDB | 19.06 MB |

**Finding:** All three databases use similar amounts of storage space.

## Conclusions

### When to use PostgreSQL?
- **Complex queries** and aggregations
- **ACID compliance** is critical
- **Need advanced features** (JSON, arrays, custom types)
- **Read-heavy workloads**

### When to use MySQL/MariaDB?
- **Bulk data insertion**
- **Simple, fast queries**
- **Write-heavy workloads**
- **Need high compatibility** (MySQL ecosystem)

### MariaDB vs MySQL
- MariaDB is **faster for INSERT** operations
- MariaDB has **more features** (additional storage engines)
- MariaDB is **fully open-source** (no Oracle licensing)
- Both databases are **compatible** for most applications

## Project Structure
```
.
├── README.md
├── README_EN.md                  # English version
├── setup_test_data.py           # PostgreSQL vs MySQL setup
├── benchmark.py                  # PostgreSQL vs MySQL benchmark
├── optimize.py                   # PostgreSQL vs MySQL optimization
├── setup_mariadb_test.py        # PostgreSQL vs MariaDB setup
├── benchmark_mariadb.py          # PostgreSQL vs MariaDB benchmark
├── optimize_mariadb.py           # PostgreSQL vs MariaDB optimization
├── compare_fedora_freebsd.py    # Fedora vs FreeBSD comparison (setup + benchmark)
├── optimize_freebsd.py           # Fedora vs FreeBSD optimization
└── benchmark_only_freebsd.py    # Fedora vs FreeBSD benchmark (SELECT only)
```

## Fedora vs FreeBSD Comparison

Performance comparison of PostgreSQL between Fedora Linux and FreeBSD operating systems.

### Installation (FreeBSD)
```bash
# PostgreSQL
pkg install postgresql16-server postgresql16-client
sysrc postgresql_enable="YES"
service postgresql initdb
service postgresql start

# Configuration for remote access
# Edit /var/db/postgres/data16/postgresql.conf
listen_addresses = '*'

# Edit /var/db/postgres/data16/pg_hba.conf
host    all     all     192.168.0.0/24    md5

service postgresql restart
```

### Usage (from Fedora)
```bash
# Setup and comparison
python3 compare_fedora_freebsd.py

# Optimization
python3 optimize_freebsd.py

# Benchmark after optimization
python3 benchmark_only_freebsd.py
```

### Fedora vs FreeBSD Results

#### INSERT Operations (100,000 records)
| Platform | Time | Records/s |
|----------|------|-----------|
| Fedora (local) | 10.30s | 9,705 |
| FreeBSD (over network) | 160.61s | 623 |

**Finding:** Fedora is 93.6% faster - network latency heavily impacts INSERT performance.

#### SELECT Operations (without indexes)
| Query | Fedora | FreeBSD | Faster |
|-------|---------|---------|--------|
| Simple SELECT | 2.55ms | 5.84ms | Fedora (56%) |
| COUNT | 8.67ms | 9.12ms | Fedora (5%) |
| AVG aggregation | 20.39ms | 23.29ms | Fedora (12%) |
| LIKE search | 10.78ms | 18.55ms | Fedora (42%) |
| Range | 31.66ms | 65.01ms | Fedora (51%) |
| ORDER BY | 19.43ms | 17.27ms | **FreeBSD (11%)** |

#### SELECT Operations (with indexes)
| Query | Fedora | FreeBSD | Fedora Improvement | FreeBSD Improvement |
|-------|---------|---------|-------------------|---------------------|
| Simple SELECT | 0.75ms | 3.38ms | 3.4x faster | 1.7x faster |
| ORDER BY | 0.45ms | 3.50ms | **43x faster** | **5x faster** |
| Range | 16.68ms | 79.74ms | 1.9x faster | - |

#### Index Creation
| Platform | Time for 3 indexes |
|----------|-------------------|
| Fedora | 0.33s |
| FreeBSD | 0.55s |

### OS Comparison Conclusions

**Linux (Fedora) Advantages:**
- Faster for local operations
- Better networking/remote access support
- Greater improvement with indexes (43x vs 5x for ORDER BY)

**FreeBSD Advantages:**
- Moderate performance for ORDER BY queries (without indexes)
- Stable performance
- Better system isolation

**Network Latency Impact:**
- INSERT operations are **16x slower** over network
- SELECT operations are **2-5x slower** over network
- Local access is critical for production environments

## License
MIT
