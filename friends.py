from tornado import Server

MAINHTML = """<html>
<head><title>Friends!</title></head>
<body>
<h1>Hello %s. You are viewing %s's friends</h1>
<ul>
%s
</ul>
<h1>The friends you have in common are</h1>
<ul>
%s
</ul>
</body>
</html>
"""
FRIENDS = {'a':['a','b','d'], 'b':['a','c','d'], 'c':['c','d'], 'd': ['a','b']}
LIELEMENT = "<li>%s</li>"

def get_friend_list(friends,bold):
    friendlist = ""
    for i in friends:
        if i in bold:
            friendlist += "<b>" + LIELEMENT %i + "</b>"
        else:
            friendlist += LIELEMENT % i
    return friendlist

def per_friends_list(response, friend):
	currentuser = response.get_field('user')
	users_friends = FRIENDS[friend]
	my_friends = FRIENDS[currentuser]
	mutual_friends = []
	for i in users_friends:
		if i in my_friends:
			mutual_friends.append(i)
	htmlfriends = get_friend_list(users_friends,mutual_friends)
	response.write(MAINHTML % (currentuser,friend, htmlfriends, mutual_friends))


if __name__ == "__main__":
    server = Server()
    server.register(r'/friends/(.*)',per_friends_list)
    server.run()
    
