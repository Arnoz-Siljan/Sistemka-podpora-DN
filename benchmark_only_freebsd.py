import psycopg2
import time
import statistics

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

# Fedora PostgreSQL
fedora_conn = psycopg2.connect(
    host="localhost",
    database="testdb",
    user="postgres",
    password="testpass"
)

# FreeBSD PostgreSQL
freebsd_conn = psycopg2.connect(
    host="192.168.0.12",
    database="testdb",
    user="postgres",
    password="testpass"
)

queries = {
    "Simple SELECT": "SELECT * FROM users WHERE id = 5000",
    "COUNT": "SELECT COUNT(*) FROM users",
    "AVG agregacija": "SELECT status, AVG(balance) FROM users GROUP BY status",
    "LIKE iskanje": "SELECT * FROM users WHERE email LIKE '%500%'",
    "Range poizvedba": "SELECT * FROM users WHERE balance BETWEEN 5000 AND 6000",
    "ORDER BY": "SELECT * FROM users ORDER BY balance DESC LIMIT 100",
}

print("\n" + "="*80)
print("BENCHMARK PO OPTIMIZACIJI - Fedora vs FreeBSD PostgreSQL")
print("="*80)

for query_name, query in queries.items():
    print(f"\n{query_name}:")
    print("-" * 80)
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
