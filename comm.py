from tornado import Server
users = {'Jordan':['hello', 'world']}
header = """

<html>
<head>
<title>%s's Wall</title>
<script type="text/javascript" src="../jquery.js"></script>
</head>
<body>
<form style="text-align:center" action="../submit" method=POST>
Post a message: <br /><textarea name="msg"></textarea><input type="hidden" value="%s" name="current_user"><input type="hidden" value="%s" name="current_Wall"><br /><input type="submit" value="Submit"></input>
<br />
"""
def submit(response):
	current_Wall = response.get_field('current_Wall')
	current_user = response.get_field('current_user')
	users[current_Wall].append(current_user+' says ' + response.get_field('msg'))
	
	response.redirect('/wall/%s' % current_Wall) 
def wall(response,current_Wall):
	final = ''
	current_user = response.get_field('username')
	
	for i in users[current_Wall]:
		final+=i+'<br />'
	
	response.write((header % (current_Wall, current_user, current_Wall)) +final)

server = Server()
server.register('/wall/(.*)',wall)
server.register('/submit',submit)


server.run()