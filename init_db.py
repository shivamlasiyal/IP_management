import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''
          CREATE TABLE ip_records
          (id INTEGER PRIMARY KEY AUTOINCREMENT,
          machine_name TEXT NOT NULL,
          ip_address TEXT NOT NULL)
          ''')
conn.commit()
conn.close()
