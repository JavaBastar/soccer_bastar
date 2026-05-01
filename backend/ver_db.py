import sqlite3
import json

conn = sqlite3.connect("partidos.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT id, timestamp, data 
    FROM partidos 
    ORDER BY id DESC 
    LIMIT 5
""")

rows = cursor.fetchall()

for r in rows:
    print("\n====================")
    print("ID:", r[0])
    print("Fecha:", r[1])
    print("Data:")

    data = json.loads(r[2])
    print(json.dumps(data, indent=2, ensure_ascii=False))

conn.close()
