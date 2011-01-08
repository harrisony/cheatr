from tornado import Server
import datetime,time
import sqlite3
#users = {'Jordan':['hello', 'world']}
header = """
<html>
<head>
<title>%s's Wall</title>

</head>
<body>
<form style="text-align:center" action="../submit" method=POST>
Post a message: <br /><textarea name="msg"></textarea><input type="hidden" value="%s" name="current_user"><input type="hidden" value="%s" name="current_Wall"><br /><input type="submit" value="Submit"></input>
<br />
"""

def adapt_datetime(ts):
	return time.mktime(ts.timetuple())

connection = sqlite3.connect('./commsdb.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS "WALL" ("ID" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "username" TEXT NOT NULL , "target" TEXT NOT NULL , "date" DATETIME NOT NULL , "message" TEXT NOT NULL )')
class Wall:
	def __init__(self, current_user, current_Wall):
		self.current_user = current_user
		self.current_Wall = current_Wall
		
	def set_wall(self, current_message):
	
		sqlite3.register_adapter(datetime.datetime, adapt_datetime)
		now = datetime.datetime.now()
		#users[current_Wall].append(current_user+' says ' + response.get_field('msg'))
    
		current_message = current_message.replace("&", "&amp;") 
		current_message = current_message.replace("<", "&lt;")
		current_message = current_message.replace(">", "&gt;")
		current_message = current_message.replace('"', "&quot;")
		
		cursor.execute('INSERT INTO "WALL" ("username","target","date","message") VALUES ("%s","%s","%s","%s")' % (self.current_user, self.current_Wall, now, current_message))
		connection.commit()
		
	def get_wall(self):
	
		final = ''
		data = cursor.execute('SELECT * FROM WALL WHERE WALL.target = "%s" ORDER BY ID DESC' % self.current_Wall)
		for row in data:
			final+= row[1] + row[4]
			final += row[3]+'<br/>'
		
		return final

		

def _wall(response,current_Wall):
	w = Wall(response.get_field('username'),current_Wall)
	final = header % (w.current_Wall, w.current_user, w.current_Wall) 
	response.write(final + w.get_wall())
def _submit(response):
	w = Wall(response.get_field('current_user'),response.get_field('current_Wall'))
	w.set_wall(response.get_field('msg'))
	response.redirect('/wall/%s?username=%s' % (w.current_Wall, w.current_user)) 
	
