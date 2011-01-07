from tornado import Server
from friendsconstants import * 
from person import Person, example_person1, example_person2, example_person3    
def get_friend_list(friends,bold='',sort=True):
    friendlist = ""
    if sort:
        friends.sort()
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
    htmlfriends = get_friend_list(users_friends)
    htmlmutual = get_friend_list(mutual_friends)
    response.write(MAINHTML % (currentuser,friend, htmlfriends,htmlmutual))

def my_friends_list(response):
    currentuser = response.get_field('user')
    users_friends = FRIENDS[currentuser]
    htmlMyFriends =  get_friend_list(users_friends)
    response.write(FRIENDHTML % (currentuser,htmlMyFriends))
def show_all_friends(response):
    currentuser = response.get_field('user')
    html = ""
    for i in FRIENDS.keys():
        html += "<a href='/friends/%s?user=%s'>%s</a><br />" % (i,currentuser,i)
    response.write(ALLFRIENDS % html)
    
if __name__ == "__main__":
    server = Server()
    server.register(r'/globalfriendslist',show_all_friends)
    server.register(r'/friends/', my_friends_list)
    server.register(r'/friends/(.*)',per_friends_list)
    server.run()

