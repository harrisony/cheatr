import os
import sqlite3
import recreate_users

conn = sqlite3.connect(os.path.join("data", "DB_Files.sqlite"))
conn.execute("DROP TABLE IF EXISTS Files")
conn.commit()
conn.close()

conn = sqlite3.connect(os.path.join("data", "friends.sqlite"))
conn.execute("DROP TABLE IF EXISTS friends")
conn.commit()
conn.close()
