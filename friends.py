from tornado import Server
from friendsconstants import * 
from dbuser import User
import sqlite3
import os
import auth
from template_engine import template

DATANAME = os.path.join("data","friends.sqlite")    

def _oneway_remove_friend(username, friend):
    print "one way remove before: " , FRIENDS
    if username in FRIENDS:
        friendslist = FRIENDS[username]
        if friend in friendslist:
            friendslist.remove(friend)
    else:
        friendslist = [friend]
    FRIENDS[username] = friendslist
    print "one way remove after: " , FRIENDS
        
def _remove_friend_local(username, friend):
    _oneway_remove_friend(friend, username)
    _oneway_remove_friend(username, friend)
        
def remove_friend(username, friend_username):
    _remove_friend_local(username, friend_username)
    print username, friend_username
    cur.execute("DELETE FROM friends WHERE friend = ? AND partner = ?;",(username, friend_username))
    cur.execute("DELETE FROM friends WHERE friend = ? AND partner = ?;",(friend_username, username))
    conn.commit()
    print "After full remove complete: " , FRIENDS
    
def _oneway_add_friend(username, friend):
        if username in FRIENDS:
                friendslist = FRIENDS[username]
                if friend not in friendslist:
                        friendslist.append(friend)
        else:
                friendslist = [friend]
        FRIENDS[username] = friendslist

def _add_friend_local(username, friend):
        _oneway_add_friend(friend, username)
        _oneway_add_friend(username, friend)

def add_friend(username, friend_username):
    if is_friend(username, friend_username):
        return 
    _add_friend_local(username, friend_username)
    cur.execute("INSERT INTO friends (friend, partner, status) VALUES (?, ?, 'f');",(username, friend_username))
    conn.commit()
    
def get_friends(username):
        print "IN BLOODY GET_FRIENDS"
        print "In get friends: " , FRIENDS
        friendlist = []
        if username in FRIENDS:
            for friend in FRIENDS[username]: 
                friendlist.append(User.get(friend))
        return friendlist

def is_friend(username, friend):
    if username not in FRIENDS:
        return False
    else:
        if friend in FRIENDS[username]:
            return True
        else:
            return False
    
def add_friend_handler(response, friend_username):
    raise Exception('Error!')
        
def add_friend_email(response):
        auth.require_user(response)
        user = auth.get_user(response)
        if user == None:
            return
        friend = User.get_from_email(response.get_field("email"))
        if friend == None:
            pass
        else:
            add_friend(user.get_username(), friend.get_username())
        context = {'user':user, 'friend':friend}
        template.render_template('templates/addconfirmation.html', context, response)
                
def remove_friend_handler(response, friend_username):
        print "IN REMOVE_FRIEND_HANDLER"
        auth.require_user(response)
        user = auth.get_user(response)
        if user == None:
            return
        username = user.get_username()
        print '\n\n',username, friend_username, '\n\n'
        friend = User.get(friend_username)
        remove_friend(username, friend_username)
        context = {'user':user, 'friend':friend}
        template.render_template('templates/confirmation.html', context, response)

def my_friends(response):
        print 'IN MY_FRIENDS'
        auth.require_user(response)
        user = auth.get_user(response)
        if user == None:
            return
        friends = get_friends(user.get_username())
        context = {'user':user, 'friends':friends}
        template.render_template('templates/friend_list_template.html', context, response)

def show_all_friends(response):
        currentusername = response.get_field('user')    
        html = ""
        for i in FRIENDS.keys():
            html += "<a href='/friends/%s?user=%s'>%s</a><br />" % (i,currentuser,i)
        response.write(ALLFRIENDS % html)
def can_use_wall(user,userorsubject):
	#user = User object
	#userorsubject = string or int
	if user.is_in_subject(userorsubject):
		return True
	elif is_friend(user.get_username(),userorsubject):
		return True
	elif user.get_username() == userorsubject:
		return True
	else:
		return False
	
	
conn = sqlite3.connect(DATANAME)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS "friends"  ("friend" TEXT NOT NULL , "partner" TEXT NOT NULL ,
    "status" TEXT NOT NULL , "date" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("friend", "partner"));
""")

FRIENDS ={}

cur.execute("""
SELECT friend, partner
FROM friends
WHERE status ='f';
""")
print "loading data"
for row in cur:
    _add_friend_local(str(row[0]), str(row[1]))

add_friend('gman', 'svet')
add_friend('gman', 'smythey')
print "loading sample data"

if __name__ == "__main__":
        print "before add\n", FRIENDS
        add_friend('gman', 'svet')
        print "after add\n", FRIENDS
        remove_friend('gman', 'svet')
        print "after delete\n", FRIENDS

		