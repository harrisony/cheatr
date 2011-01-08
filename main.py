from tornado import Server

# Import your module here
# e.g. import mymodule
import profile
import friends
if __name__ == "__main__":
    server = Server()
    # Register your urls here
    # e.g. server.register("/foo", mymodule.foohandler)

    server.register("/profile/(.*)", profile.profile)
    server.register("/signup",profile.signup)
    server.register("/update_info",profile.update)
    server.register('/globalfriendslist',friends.show_all_friends)
    server.register('/friends/', friends.my_friends_list)
    server.register('/friends/(.*)',friends.per_friends_list)
	
    server.run()
