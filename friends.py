from tornado import Server
from friendsconstants import * 
from user import User
import sqlite3
import os

DATANAME = os.path.join("data","friends.sqlite")    

def _oneway_remove_friend(username, friend):
        if username in FRIENDS:
            friendslist = FRIENDS[username]
            if friend in friendslist:
                friendslist.remove(friend)
        else:
            friendslist = [friend]
        FRIENDS[username] = friendslist
        
def _remove_friend_local(username, friend):
        _oneway_remove_friend(friend, username)
        _oneway_remove_friend(username, friend)
        
def remove_friend(username, friend):
        _remove_friend_local(username, friend)
        cur.execute("DELETE FROM friends WHERE friend = ? AND partner = ?;",(username, friend))
        cur.execute("DELETE FROM friends WHERE friend = ? AND partner = ?;",(friend, username))
        conn.commit()


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

def add_friend(username, friend):
        if is_friend(username, friend):
            return 
        _add_friend_local(username, friend)
        cur.execute("INSERT INTO friends (friend, partner, status) VALUES (?, ?, 'f');",(username, friend))
        conn.commit()
                
def get_friends(username):
        if username in FRIENDS:
                friendslist = FRIENDS[username]
        else:
                friendslist = []
        return friendslist

def is_friend(username, friend):
    if username not in FRIENDS:
        return False
    else:
        if friend in FRIENDS[username]:
            return True
        else:
            return False

def get_friend_list(friends,bold='',sort=True):
        friendlist = ""
        if sort:
                friends.sort()
        for friend in friends:
                if friend in bold:
                        friendlist += "<a href='/profile/%s'><b><li>%s</li></b></a>"%(friend,friend)
                else:
                        friendlist += "<a href='/profile/%s'><li>%s</li></a>"%(friend,friend)
        return friendlist

def per_friends_list(response, friend):
        currentuser = response.get_field('user')
        users_friends = FRIENDS[friend]
        my_friends = FRIENDS[currentuser]
        mutual_friends = []
        for i in users_friends:
                if i in my_friends:
                        mutual_friends.append(i)
        htmlfriends = get_friend_list(users_friends)
        htmlmutual = get_friend_list(mutual_friends)
        response.write(MAINHTML % (currentuser,friend, htmlfriends,htmlmutual))

def my_friends_list(response):
        currentusername = response.get_field('user')
        currentuserobject = User.get(currentusername)
        if currentusername not in FRIENDS:
                if currentuserobject is None:
                        response.redirect("/signup")
        else:
                users_friends = FRIENDS[currentusername]
                htmlMyFriends = get_friend_list(users_friends)
                response.write(FRIENDHTML % (currentusername,htmlMyFriends,))

def show_all_friends(response):
        currentusername = response.get_field('user')    
        html = ""
        for i in FRIENDS.keys():
                html += "<a href='/friends/%s?user=%s'>%s</a><br />" % (i,currentuser,i)
        response.write(ALLFRIENDS % html)
    
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
for row in cur:
    _add_friend_local(str(row[0]), str(row[1]))

#add_friend('gman', 'svet')
#add_friend('gman', 'smythey')

#if __name__ == "__main__":
        #print "before add\n", FRIENDS
        #add_friend('gman', 'svet')
        #print "after add\n", FRIENDS
        #remove_friend('gman', 'svet')
        #print "after delete\n", FRIENDS
