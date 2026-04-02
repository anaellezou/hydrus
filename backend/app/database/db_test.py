import sqlite3

conn = sqlite3.connect("kanji_database.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM kanji LIMIT 5")
results = cursor.fetchall()
for row in results:
    print(row)

conn.close()
