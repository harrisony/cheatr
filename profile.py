from tornado import Server

Users = { "Katie": { "firstname": "Katie", "lastname": "Bell", "Biography": "Loves programming"},
          "Nicholas": {"firstname": "Nicholas", "lastname": "Cooke", "Biography": "Loves apple"},
          "Jennifer": {"firstname": "Jennifer", "lastname": "Truong", "Biography": "Loves singing"}}

OUTPUT = """
<html>
<head><title>%s's Profile</title>
<nav>
<ul>
<li><a href='/'>Home</a></li>
<li>Resources
<ul>
<li><a href='/'>Notes</a></li>
<li><a href='/'>Past Papers</a></li>
</ul>
</head>
<body>
<h1>%s's Profile</h1>
<p>First Name: %s</p>
<p>Last Name: %s</p>
<p>Bio: %s</p>
</body>
</html>
"""

USERNOTFOUND = """
<html>
<head><title>User Not Found</title></head>
<body>
<h1>Error. User not found.</h1>
</body>
</html>
"""

def fun(response, username):
    print username
    if username in Users:
        firstname = Users[username]["firstname"]
        lastname = Users[username]["lastname"]
        bio = Users[username]["Biography"]
        response.write(OUTPUT % (username,username,firstname,lastname,bio))
    else:
        response.write(USERNOTFOUND)
        

server = Server()
server.register("/profile/(.*)", fun)
server.run()
