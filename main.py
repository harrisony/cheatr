from tornado import Server

# Import your module here
# e.g. import mymodule
import profile
import friends
import subject
import comms
import upload
import home


if __name__ == "__main__":
    server = Server()
    # Register your urls here
    # e.g. server.register("/foo", mymodule.foohandler)

    server.register("/", home.page)
    server.register("/profile/(.*)", profile.profile)
    server.register("/signup",profile.signup)
    server.register("/update_info",profile.update)
    server.register('/globalfriendslist',friends.show_all_friends)
    server.register('/friends/', friends.my_friends_list)
    server.register('/friends/(.*)',friends.per_friends_list)
    server.register("/subject", subject.subjectpage)
    server.register("/subject/(.*)", subject.viewsubject)
    server.register("/subjects", subject.listsubject)
    server.register('/wall/(.*)',comms._wall)
    server.register('/wallupdate',comms._getWallData)
    server.register('/feedupdate',comms._getFeedData)
    server.register('/feed/',comms._feed)
    server.register('/feed',comms._feed)
    server.register('/submit',comms._submit)


    # file upload stuff
    server.register("/fileupload", upload.chk_ul_fields)
    server.register("/filesearch", upload.file_search)
    server.register("/fileedit/(.*)", upload.file_edit)        
    server.register("/listallfiles", upload.listallfiles) 
    server.run()
