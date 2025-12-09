import psycopg2
import mysql.connector
import time

def optimize_postgresql():
    """Dodaj indekse v PostgreSQL"""
    conn = psycopg2.connect(
        host="localhost", database="testdb",
        user="postgres", password="testpass"
    )
    cursor = conn.cursor()
    
    print("PostgreSQL optimizacija...")
    
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
    print("  ✓ ANALYZE completed\n")
    
    cursor.close()
    conn.close()

def optimize_mysql():
    """Dodaj indekse v MySQL"""
    conn = mysql.connector.connect(
        host="localhost", database="testdb",
        user="testuser", password="testpass"
    )
    cursor = conn.cursor()
    
    print("MySQL optimizacija...")
    
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
    
    cursor.execute("OPTIMIZE TABLE users")
    cursor.fetchall()
    conn.commit()
    print("  ✓ OPTIMIZE completed\n")
    
    cursor.close()
    conn.close()

def show_table_sizes():
    """Prikaži velikosti tabel"""
    print("="*60)
    print("VELIKOSTI TABEL")
    print("="*60)
    
    # PostgreSQL
    pg_conn = psycopg2.connect(
        host="localhost", database="testdb",
        user="postgres", password="testpass"
    )
    pg_cursor = pg_conn.cursor()
    pg_cursor.execute("""
        SELECT 
            pg_size_pretty(pg_total_relation_size('users')) as users_size,
            pg_size_pretty(pg_total_relation_size('orders')) as orders_size
    """)
    pg_sizes = pg_cursor.fetchone()
    print(f"\nPostgreSQL:")
    print(f"  users:  {pg_sizes[0]}")
    print(f"  orders: {pg_sizes[1]}")
    pg_conn.close()
    
    # MySQL
    mysql_conn = mysql.connector.connect(
        host="localhost", database="testdb",
        user="testuser", password="testpass"
    )
    mysql_cursor = mysql_conn.cursor()
    mysql_cursor.execute("""
        SELECT 
            table_name,
            ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
        FROM information_schema.TABLES
        WHERE table_schema = 'testdb'
        ORDER BY table_name
    """)
    print(f"\nMySQL:")
    for row in mysql_cursor.fetchall():
        print(f"  {row[0]}: {row[1]} MB")
    mysql_conn.close()
    print()

if __name__ == "__main__":
    print("="*60)
    print("OPTIMIZACIJA BAZ PODATKOV")
    print("="*60)
    print()
    
    optimize_postgresql()
    optimize_mysql()
    show_table_sizes()
