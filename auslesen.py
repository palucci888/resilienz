import sqlite3

conn = sqlite3.connect('anmeldungen.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM anmeldungen')
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
