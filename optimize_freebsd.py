import psycopg2
import time

def optimize_db(conn, name):
    """Dodaj indekse"""
    cursor = conn.cursor()
    
    print(f"{name} optimizacija...")
    
    indexes = [
        ("idx_users_email", "CREATE INDEX idx_users_email ON users(email)"),
        ("idx_users_status", "CREATE INDEX idx_users_status ON users(status)"),
        ("idx_users_balance", "CREATE INDEX idx_users_balance ON users(balance)"),
    ]
    
    for idx_name, idx_sql in indexes:
        try:
            start = time.time()
            cursor.execute(idx_sql)
            conn.commit()
            elapsed = time.time() - start
            print(f"  ✓ {idx_name}: {elapsed:.3f}s")
        except Exception as e:
            print(f"  ✗ {idx_name}: {e}")
    
    cursor.execute("ANALYZE users")
    conn.commit()
    print(f"  ✓ ANALYZE completed\n")
    cursor.close()

# Fedora
fedora_conn = psycopg2.connect(
    host="localhost", database="testdb",
    user="postgres", password="testpass"
)

# FreeBSD
freebsd_conn = psycopg2.connect(
    host="192.168.0.12", database="testdb",
    user="postgres", password="testpass"
)

print("="*60)
print("OPTIMIZACIJA - Fedora vs FreeBSD")
print("="*60)
print()

optimize_db(fedora_conn, "Fedora")
optimize_db(freebsd_conn, "FreeBSD")

fedora_conn.close()
freebsd_conn.close()
