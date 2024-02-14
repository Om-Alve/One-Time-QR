import sqlite3

# Database connection
conn = sqlite3.connect("qrcodes.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS qrcodes (
                    qr_id TEXT PRIMARY KEY,
                    scanned INTEGER DEFAULT 0
                 )''')
print(cursor.fetchone())

# Close database connection
conn.close()