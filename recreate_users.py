import sqlite3

SQLSTATEMENT = """
DROP TABLE IF EXISTS "users";
CREATE TABLE "users" ("username" TEXT PRIMARY KEY  NOT NULL , "password" TEXT NOT NULL , "firstname" TEXT, 
                      "lastname" TEXT, "email" TEXT, "profilepicpath" TEXT, "School" TEXT);
-- INSERT INTO "users" VALUES('james',   'ilovejava', 'James',    'Curran',    'james@it.usyd.edu,au',     '', 'usyd');
INSERT INTO "users" VALUES('svet',    '22837024f941f67c2ff80c49e6bccf110c062149',    'Svetlana', 'Roshenkev', 'a@example.com',            '', 'school of fail');
INSERT INTO 'users' VALUES('gman',    '22b4468ae6dcf46c36c9622e292c7a3506bb0db4',       'Gustav',   'Olafsen',   'gustav@isacoolperson.com', '', 'unsw');
INSERT INTO 'users' VALUES('smythey', 'c70ad0b8c4ed390d54062024d514a3c94a5c1851', 'Johan',    'Smythe',    'smythey@usyd.edu.au',      '', 'usyd');
"""


conn = sqlite3.connect('users.sqlite')
conn.executescript(SQLSTATEMENT)
conn.commit()
conn.close()