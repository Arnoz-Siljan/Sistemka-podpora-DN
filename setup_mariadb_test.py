import psycopg2
import mysql.connector
import time
import random

# Število zapisov za test
NUM_RECORDS = 100000

print("Povezovanje z bazami...")

# PostgreSQL connection
pg_conn = psycopg2.connect(
    host="localhost",
    database="testdb",
    user="postgres",
    password="testpass"
)

# MariaDB connection (uporablja isti driver kot MySQL)
mariadb_conn = mysql.connector.connect(
    host="localhost",
    database="testdb",
    user="testuser",
    password="testpass"
)

print("✓ Povezava uspešna\n")

def create_tables():
    """Ustvari tabele v vseh bazah"""
    
    print("Ustvarjam tabele...")
    
    # PostgreSQL
    pg_cursor = pg_conn.cursor()
    pg_cursor.execute("DROP TABLE IF EXISTS orders CASCADE")
    pg_cursor.execute("DROP TABLE IF EXISTS users CASCADE")
    
    pg_cursor.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20),
            balance DECIMAL(10,2)
        )
    """)
    
    pg_cursor.execute("""
        CREATE TABLE orders (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount DECIMAL(10,2),
            status VARCHAR(20)
        )
    """)
    pg_conn.commit()
    print("  ✓ PostgreSQL tabele ustvarjene")
    
    # MariaDB
    mariadb_cursor = mariadb_conn.cursor()
    mariadb_cursor.execute("DROP TABLE IF EXISTS orders")
    mariadb_cursor.execute("DROP TABLE IF EXISTS users")
    
    mariadb_cursor.execute("""
        CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20),
            balance DECIMAL(10,2)
        ) ENGINE=InnoDB
    """)
    
    mariadb_cursor.execute("""
        CREATE TABLE orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount DECIMAL(10,2),
            status VARCHAR(20),
            FOREIGN KEY (user_id) REFERENCES users(id)
        ) ENGINE=InnoDB
    """)
    mariadb_conn.commit()
    print("  ✓ MariaDB tabele ustvarjene\n")

def generate_test_data(num_records):
    """Generira testne podatke"""
    print(f"Generiram {num_records} testnih zapisov...")
    users = []
    for i in range(num_records):
        username = f"user_{i}"
        email = f"user_{i}@example.com"
        status = random.choice(['active', 'inactive', 'suspended'])
        balance = round(random.uniform(0, 10000), 2)
        users.append((username, email, status, balance))
    print("✓ Podatki generirani\n")
    return users

def insert_data_postgresql(data):
    """Vstavi podatke v PostgreSQL"""
    print("Vstavljam podatke v PostgreSQL...")
    start_time = time.time()
    
    pg_cursor = pg_conn.cursor()
    pg_cursor.executemany(
        "INSERT INTO users (username, email, status, balance) VALUES (%s, %s, %s, %s)",
        data
    )
    pg_conn.commit()
    
    elapsed = time.time() - start_time
    print(f"✓ PostgreSQL INSERT: {elapsed:.2f}s ({len(data)/elapsed:.0f} records/s)\n")
    return elapsed

def insert_data_mariadb(data):
    """Vstavi podatke v MariaDB"""
    print("Vstavljam podatke v MariaDB...")
    start_time = time.time()
    
    mariadb_cursor = mariadb_conn.cursor()
    mariadb_cursor.executemany(
        "INSERT INTO users (username, email, status, balance) VALUES (%s, %s, %s, %s)",
        data
    )
    mariadb_conn.commit()
    
    elapsed = time.time() - start_time
    print(f"✓ MariaDB INSERT: {elapsed:.2f}s ({len(data)/elapsed:.0f} records/s)\n")
    return elapsed

# Glavni program
print("="*60)
print("SETUP TESTNIH PODATKOV - PostgreSQL vs MariaDB")
print("="*60)
print()

create_tables()
test_data = generate_test_data(NUM_RECORDS)

pg_time = insert_data_postgresql(test_data)
mariadb_time = insert_data_mariadb(test_data)

print("="*60)
print("REZULTATI INSERT OPERACIJ:")
print("="*60)
print(f"PostgreSQL: {pg_time:.2f}s")
print(f"MariaDB:    {mariadb_time:.2f}s")
if pg_time < mariadb_time:
    print(f"PostgreSQL je hitrejši za {((mariadb_time-pg_time)/mariadb_time*100):.1f}%")
else:
    print(f"MariaDB je hitrejši za {((pg_time-mariadb_time)/pg_time*100):.1f}%")
print("="*60)

pg_conn.close()
mariadb_conn.close()
