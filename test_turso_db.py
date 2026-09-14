import turso_db

url = "libsql://apexhost-db-public0gamer.aws-ap-south-1.turso.io"
token = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3ODk0MDkyNzIsImlkIjoiMDFhMGExMTktZWMwMS03ZTg4LTkyNWUtOTUzODNmM2YxMWExIiwia2lkIjoiVUgyM0NGSTZFaTFmVlVwQ3dzOUlnTDZjR3R6REpMR2lKby1xeGJPUjhEQSIsInJpZCI6IjFiNDdlZjgxLWRmZWEtNDhhYi04YzgyLTQwZDYwYmEyY2Q4MSJ9._Zvwg006u3eBp-XYfP-p1iSjMRzh4QdvOoHmCI2USNtFoGHAj5ouSC7xIuu1ePmQ-1U9YhzRMbDx1mgpF8CaCg"

conn = turso_db.connect(url, token)
cursor = conn.cursor()

# Test table creation
cursor.execute("CREATE TABLE IF NOT EXISTS test_users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
print("Created table.")

# Test insertion
cursor.execute("INSERT INTO test_users (name, age) VALUES (?, ?)", ("Alice", 25))
print("Inserted Alice. LastRowId:", cursor.lastrowid)

# Test select
cursor.execute("SELECT * FROM test_users")
row = cursor.fetchone()
print("Fetched:", row)
if row:
    print("Name via dict:", row['name'])
    print("Name via attr:", row.name)
    print("Name via index:", row[1])

# Test executemany
cursor.executemany("INSERT INTO test_users (name, age) VALUES (?, ?)", [("Bob", 30), ("Charlie", 35)])
print("Executemany done.")

cursor.execute("SELECT COUNT(*) FROM test_users")
print("Count:", cursor.fetchone()[0])
