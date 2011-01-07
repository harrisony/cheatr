from tornado import Server
import datetime,time
import sqlite3
#users = {'Jordan':['hello', 'world']}
header = """
<html>
<head>
<title>%s's Wall</title>
<script type="text/javascript" src="static_url(../jquery.js)"></script>
</head>
<body>
<form style="text-align:center" action="../submit" method=POST>
Post a message: <br /><textarea name="msg"></textarea><input type="hidden" value="%s" name="current_user"><input type="hidden" value="%s" name="current_Wall"><br /><input type="submit" value="Submit"></input>
<br />
"""

def adapt_datetime(ts):
	return time.mktime(ts.timetuple())

connection = sqlite3.connect('./db.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS "WALL" ("ID" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "username" TEXT NOT NULL , "target" TEXT NOT NULL , "date" DATETIME NOT NULL , "message" TEXT NOT NULL )')
def submit(response):
	current_Wall = response.get_field('current_Wall')
	current_user = response.get_field('current_user')
	current_message = response.get_field('msg')
	sqlite3.register_adapter(datetime.datetime, adapt_datetime)
	now = datetime.datetime.now()
	#users[current_Wall].append(current_user+' says ' + response.get_field('msg'))
	cursor.execute('INSERT INTO "WALL" ("username","target","date","message") VALUES ("%s","%s","%s","%s")' % (current_user, current_Wall, now, current_message))
	connection.commit()
	response.redirect('/wall/%s?username=%s' % (current_Wall,current_user)) 
def wall(response,current_Wall):
	final = ''
	current_user = response.get_field('username')
	
	#for i in users[current_Wall]:
		#final+=i+'<br />'
	
	response.write((header % (current_Wall, current_user, current_Wall)) +final)

server = Server()
server.register('/wall/(.*)',wall)
server.register('/submit',submit)



server.run()
