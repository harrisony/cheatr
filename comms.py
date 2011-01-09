from tornado import Server
from time import time
from user import User
from friends import *
from template_engine import template
import sqlite3
#users = {'Jordan':['hello', 'world']}
header = """
<html>
	<head>
		<title>%s</title>
<script src="../static/js/prototype.js"></script>	
		
	</head>
<body>
	<form id="message" style="text-align:center" action="/submit?user=%s" method=POST></input><br />
	Post a message: <br /><textarea name="msg"></textarea><input type="hidden" value="%s" name="current_Wall"><br /><input type="submit" value="Submit" ></input>
	<br />
</body>

	<script type="text/javascript">	
	Event.observe(window, 'load',init,false);
	function init(){
	Event.observe('message','submit',submit);
	}
	
		function submit(e){
			$('message').request({
				onComplete: function(){ 
				
				}
			}); 
			Event.stop(e)
		}
		new Ajax.PeriodicalUpdater('content', '/%s', {
			method: 'get', frequency: 20, decay: 0
		});

		
			</script>
			<div id ="content">
"""

def age(old):
	try:
		UNITS = {86400:'day', 3600:'hour', 60:'minute', 1:'second'}
		duration = int(time())-old
		elapsed = ""
		for unit in UNITS:
			quotient = duration/unit
			if quotient == 1:
				elapsed += """%s %s """ % (str(quotient),UNITS[unit])
			elif quotient > 1:
				elapsed += """%s %ss """ % (str(quotient), UNITS[unit])
			duration = duration % unit
		if elapsed.split()[1] in ['day','days','hour','hours']:
			print elapsed.split()
			elapsed = " ".join(elapsed.split()[:2]) + ' '
		return elapsed + 'ago'
	except:
		return 'moments ago'

	
	

class Message:
	def __init__(self, author='', time='', message=''):
		self.author = author
		self.time = time
		self.message = message
		
	def __cmp__(self, other):
		if self.time < other.time:
			return -1 
		elif self.time > other.time:
			return 1
		elif self.time == other.time:
			return 0

	def display(self):
		return self.author + ": " + self.message
			 
class WallConnection:
	def __init__(self, current_Wall):
		
		self.current_Wall = current_Wall	
		self.connection = sqlite3.connect('./commsdb.db')
		self.cursor = self.connection.cursor()
		self.cursor.execute('CREATE TABLE IF NOT EXISTS "WALL" ("ID" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "author" TEXT NOT NULL , "target" TEXT NOT NULL , "time" INTEGER NOT NULL , "message" TEXT NOT NULL )')
	def set_wall(self, m):
		
		#users[current_Wall].append(author+' says ' + response.get_field('msg'))
		m.message = m.message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
		try:
			self.cursor.execute('INSERT INTO "WALL" ("author","target","time","message") VALUES ("%s","%s","%s","%s")' % (m.author, self.current_Wall, m.time,m.message))
			self.connection.commit()
			return True	
		except sqlite3.OperationalError, e:
			return e.args[0]
	def get_wall(self):
		
		final = []
		data = self.cursor.execute('SELECT * FROM WALL WHERE WALL.target = "%s" ORDER BY time DESC' % self.current_Wall)
		for row in data:
			
			final.append([row[1], row[4], age(int(row[3]))])
			
		
		return final
		
class FeedConnection: 
	def __init__(self, current_User):
		self.current_User = current_User	
		self.connection = sqlite3.connect('./commsdb.db')
		self.cursor = self.connection.cursor()
		self.cursor.execute('CREATE TABLE IF NOT EXISTS "WALL" ("ID" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "author" TEXT NOT NULL , "target" TEXT NOT NULL , "time" INTEGER NOT NULL , "message" TEXT NOT NULL )')
	def get_feed(self):
		
		final = []
		friendsList = get_friends(self.current_User)
		data = self.cursor.execute('SELECT * FROM WALL ORDER BY time DESC')
		for row in data:
			for i in friendsList:
				if i == row[1] or row[1] == self.current_User:  
					final.append([row[1], row[4], age(int(row[3]))])		
		return final

def _wall(response,current_Wall):
	user = User.get(current_Wall)
	if user == False:
		response.redirect("/signup")
	else:
		w = WallConnection(current_Wall)
		fullname = user.get_first_name() + " " + user.get_last_name() 
		currentUrl = 'wall/'+current_Wall+'?user='+response.get_field('user')
		
		final = header % (fullname+'\'s Wall', response.get_field('user'), current_Wall, currentUrl) 
		final += str(w.get_wall()) + '</div>'
		#context = {'wall':w}
		#template.render_template('static/html/test.html', context, response)
		response.write(final)

def _submit(response):
	now = time()
	m = Message(response.get_field('user'), now, response.get_field('msg'))
	w = WallConnection(response.get_field('current_Wall'))
	print w.set_wall(m)
	response.redirect('/wall/%s?user=%s' % (w.current_Wall,response.get_field('user'))) 

def _feed(response):
	user = User.get(response.get_field('user'))
	if user == False:
		response.redirect("/signup")
	else:
		f = FeedConnection(response.get_field('user'))
		fullname = user.get_first_name() + " " + user.get_last_name() 
		currentUrl = 'feed/'+'?user='+response.get_field('user')
		final = header % ('News Feed',response.get_field('user'), response.get_field('user'), currentUrl) 
		final += str(f.get_feed()) + '</div>'
		#context = {'wall':w}
		#template.render_template('static/html/test.html', context, response)
		response.write(final)