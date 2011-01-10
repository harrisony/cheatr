import sqlite3

connection=sqlite3.connect("commsdb.sqlite")
connection.execute('DROP TABLE IF EXISTS "WALL"')

connection.execute('CREATE TABLE "WALL" ("ID" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "author" TEXT NOT NULL , "target" TEXT NOT NULL , "time" INTEGER NOT NULL , "message" TEXT NOT NULL )')

connection.commit()
connection.close() 
