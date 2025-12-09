import psycopg2
import mysql.connector
import time
import statistics

def benchmark_query(conn, query, db_name, iterations=10):
    """Izvede benchmark za določeno poizvedbo"""
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
    min_time = min(times)
    max_time = max(times)
    
    print(f"{db_name:12} | Avg: {avg_time*1000:7.2f}ms | Min: {min_time*1000:7.2f}ms | Max: {max_time*1000:7.2f}ms")
    
    return avg_time

def run_benchmarks():
    # Connections
    pg_conn = psycopg2.connect(
        host="localhost", database="testdb",
        user="postgres", password="testpass"
    )
    
    mariadb_conn = mysql.connector.connect(
        host="localhost", database="testdb",
        user="testuser", password="testpass"
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
    print("BENCHMARK REZULTATI - PostgreSQL vs MariaDB")
    print("="*80)
    
    for query_name, query in queries.items():
        print(f"\n{query_name}:")
        print("-" * 80)
        pg_time = benchmark_query(pg_conn, query, "PostgreSQL")
        mariadb_time = benchmark_query(mariadb_conn, query, "MariaDB")
        
        if pg_time < mariadb_time:
            faster = "PostgreSQL"
            diff_percent = ((mariadb_time - pg_time) / mariadb_time * 100)
        else:
            faster = "MariaDB"
            diff_percent = ((pg_time - mariadb_time) / pg_time * 100)
        
        print(f"{'':12} | {faster} je hitrejši za {diff_percent:.1f}%")
    
    pg_conn.close()
    mariadb_conn.close()

if __name__ == "__main__":
    run_benchmarks()
