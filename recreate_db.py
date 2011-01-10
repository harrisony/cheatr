import os
import sqlite3
import recreate_comms_db
import recreate_users_db
import recreate_subjects_db


conn = sqlite3.connect(os.path.join("data", "commsdb.sqlite"))
conn.execute("DROP TABLE IF EXISTS WALL")
conn.commit()
conn.close()

conn = sqlite3.connect(os.path.join("data", "DB_Files.sqlite"))
conn.execute("DROP TABLE IF EXISTS Files")
conn.commit()
conn.close()

conn = sqlite3.connect(os.path.join("data", "friends.sqlite"))
conn.execute("DROP TABLE IF EXISTS friends")
conn.commit()
conn.close()

