import sqlite3

self.connection = sqlite3.connect('./commsdb.sqlite')
self.cursor = self.connection.cursor()


connection=sqlite3.connect("commsdb.sqlite")
cursor=connection.cursor()
cursor.execute("DROP table if exists WALL")
self.cursor.execute('CREATE TABLE "WALL" ("ID" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "author" TEXT NOT NULL , "target" TEXT NOT NULL , "time" INTEGER NOT NULL , "message" TEXT NOT NULL )')

connection.commit()
cursor.close() 
