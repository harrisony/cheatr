from tornado import Server
from time import time
from dbuser import User
from friends import *
import auth
from template_engine import template
import sqlite3
#users = {'Jordan':['hello', 'world']}


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
		if elapsed.split()[1] in ['day','days','hour','hours','minute','minutes']:
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
		self.connection = sqlite3.connect('./commsdb.sqlite')
		self.cursor = self.connection.cursor()
		self.cursor.execute('CREATE TABLE IF NOT EXISTS "WALL" ("ID" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "author" TEXT NOT NULL , "target" TEXT NOT NULL , "time" INTEGER NOT NULL , "message" TEXT NOT NULL )')
	def set_wall(self, m):
		
		#users[current_Wall].append(author+' says ' + response.get_field('msg'))
		#m.message = m.message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
		try:
			self.cursor.execute('INSERT INTO "WALL" ("author","target","time","message") VALUES ("%s","%s","%s","%s")' % (m.author, self.current_Wall, m.time,m.message))
			self.connection.commit()
			return True	
		except sqlite3.OperationalError, e:
			return e.args[0]
	def get_wall(self):
		
		final = []
		data = self.cursor.execute('SELECT * FROM WALL ORDER BY time DESC')
		if not data:
			return 0
		for row in data:
			current_Row = [[row[0],row[1],row[1],row[4],age(int(row[3])),'']];
			if row[2] == self.current_Wall:
				
				author = User.get(row[1])
				fullname = author.get_first_name() + " " + author.get_last_name()
				path = author.get_profile_pic_path()
				if not path:
					current_Row[0][5] = '/static/images/default_avatar.jpeg'
				else:
					current_Row[0][5] = path
				
				current_Row[0][1] = fullname
				final.append(current_Row[0])
			
		
		return final
		
class FeedConnection: 
	def __init__(self, response):
		self.currentUserObject = auth.get_user(response);
		self.current_User = self.currentUserObject.get_username()
		self.connection = sqlite3.connect('./commsdb.sqlite')
		self.cursor = self.connection.cursor()
		self.cursor.execute('CREATE TABLE IF NOT EXISTS "WALL" ("ID" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "author" TEXT NOT NULL , "target" TEXT NOT NULL , "time" INTEGER NOT NULL , "message" TEXT NOT NULL )')
	def get_feed(self):
		
		final = []
		friendsList = get_friends(self.current_User)
		
		data = self.cursor.execute('SELECT * FROM WALL ORDER BY time DESC LIMIT 15;')
		if not data:
			return 0
		for row in data:
			current_Row = [[row[0],row[1],row[1],row[4],age(int(row[3])),'']]		
			for user in friendsList:
				if user.get_username() == row[1]:
					if current_Row not in final:
						
						

						fullname = user.get_first_name() + " " + user.get_last_name()
						current_Row[0][1] = fullname
						#set the picture
						path = user.get_profile_pic_path()
						
						if not path:
							current_Row[0][5] = '/static/images/default_avatar.jpeg'
							
						else:
							current_Row[0][5] = path
						final.append(current_Row[0])
						
						
			if self.currentUserObject.get_username() == row[1]:
				currentuser = self.currentUserObject
				fullname = currentuser.get_first_name() + " " + currentuser.get_last_name()
				current_Row[0][1] = fullname
				path = currentuser.get_profile_pic_path()
				if not path:
					current_Row[0][5] = '/static/images/default_avatar.jpeg'
						
				else:
					current_Row[0][5] = path				
				final.append(current_Row[0])
				
						
				#	elif row[0] not in final[0]:
				#		print final[0]
		
		return final
		
		
def _getWallData(response):

	current_Wall = response.get_field('current_Wall')

	w = WallConnection(current_Wall)

	context = {"posts":w.get_wall()}

	template.render_template('templates/wallcontent.html', context, response)
		
		
	#final = header % (fullname+'\'s Wall', currentUrl) 
	#final += str(w.get_wall()) + '</div>'
		
		
def _getFeedData(response):
	
	f = FeedConnection(response)
	context = {"posts":f.get_feed()}
	template.render_template('templates/wallcontent.html', context, response)
	

def _submit(response):

	now = time()
	m = Message(auth.get_user(response).get_username(), now, response.get_field('msg'))
	w = WallConnection(response.get_field('current_Wall'))
	w.set_wall(m)
	return
	 
