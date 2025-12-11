import psycopg2
import time
import statistics
import random

NUM_RECORDS = 100000

print("Povezovanje z bazami...")

# Fedora PostgreSQL (local)
fedora_conn = psycopg2.connect(
    host="localhost",
    database="testdb",
    user="postgres",
    password="testpass"
)

# FreeBSD PostgreSQL (remote)
freebsd_conn = psycopg2.connect(
    host="192.168.0.12",
    database="testdb",
    user="postgres",
    password="testpass"
)

print("✓ Povezava uspešna\n")

def create_table(conn, name):
    """Ustvari tabelo"""
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users CASCADE")
    cursor.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20),
            balance DECIMAL(10,2)
        )
    """)
    conn.commit()
    cursor.close()
    print(f"✓ {name} tabela ustvarjena")

def generate_test_data(num_records):
    """Generira testne podatke"""
    users = []
    for i in range(num_records):
        username = f"user_{i}"
        email = f"user_{i}@example.com"
        status = random.choice(['active', 'inactive', 'suspended'])
        balance = round(random.uniform(0, 10000), 2)
        users.append((username, email, status, balance))
    return users

def insert_data(conn, data, name):
    """Vstavi podatke"""
    start_time = time.time()
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO users (username, email, status, balance) VALUES (%s, %s, %s, %s)",
        data
    )
    conn.commit()
    cursor.close()
    elapsed = time.time() - start_time
    print(f"✓ {name} INSERT: {elapsed:.2f}s ({len(data)/elapsed:.0f} records/s)")
    return elapsed

def benchmark_query(conn, query, name, iterations=10):
    """Benchmark poizvedbe"""
    times = []
    for i in range(iterations):
        cursor = conn.cursor()
        start = time.time()
        cursor.execute(query)
        results = cursor.fetchall()
        elapsed = time.time() - start
        times.append(elapsed)
        cursor.close()
    
    avg_time = statistics.mean(times)
    print(f"{name:15} | Avg: {avg_time*1000:7.2f}ms")
    return avg_time

# SETUP
print("="*60)
print("SETUP - Fedora vs FreeBSD PostgreSQL")
print("="*60)
print("\nUstvarjam tabele...")
create_table(fedora_conn, "Fedora")
create_table(freebsd_conn, "FreeBSD")

print(f"\nGeneriram {NUM_RECORDS} testnih zapisov...")
test_data = generate_test_data(NUM_RECORDS)

print("\nVstavljam podatke...")
fedora_insert = insert_data(fedora_conn, test_data, "Fedora")
freebsd_insert = insert_data(freebsd_conn, test_data, "FreeBSD")

# BENCHMARK
queries = {
    "Simple SELECT": "SELECT * FROM users WHERE id = 5000",
    "COUNT": "SELECT COUNT(*) FROM users",
    "AVG agregacija": "SELECT status, AVG(balance) FROM users GROUP BY status",
    "LIKE iskanje": "SELECT * FROM users WHERE email LIKE '%500%'",
    "Range poizvedba": "SELECT * FROM users WHERE balance BETWEEN 5000 AND 6000",
    "ORDER BY": "SELECT * FROM users ORDER BY balance DESC LIMIT 100",
}

print("\n" + "="*60)
print("BENCHMARK REZULTATI")
print("="*60)

print(f"\nINSERT operacije:")
print("-" * 60)
print(f"Fedora:  {fedora_insert:.2f}s")
print(f"FreeBSD: {freebsd_insert:.2f}s")
if fedora_insert < freebsd_insert:
    print(f"Fedora je hitrejši za {((freebsd_insert-fedora_insert)/freebsd_insert*100):.1f}%")
else:
    print(f"FreeBSD je hitrejši za {((fedora_insert-freebsd_insert)/fedora_insert*100):.1f}%")

for query_name, query in queries.items():
    print(f"\n{query_name}:")
    print("-" * 60)
    fedora_time = benchmark_query(fedora_conn, query, "Fedora")
    freebsd_time = benchmark_query(freebsd_conn, query, "FreeBSD")
    
    if fedora_time < freebsd_time:
        faster = "Fedora"
        diff_percent = ((freebsd_time - fedora_time) / freebsd_time * 100)
    else:
        faster = "FreeBSD"
        diff_percent = ((fedora_time - freebsd_time) / fedora_time * 100)
    
    print(f"{'':15} | {faster} je hitrejši za {diff_percent:.1f}%")

fedora_conn.close()
freebsd_conn.close()
