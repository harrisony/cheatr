from tornado import Server

# Import your module here
# e.g. import mymodule
import profile
import friends
import subject
import comms
import upload
import home
import auth


if __name__ == "__main__":
    server = Server()
    # Register your urls here
    # e.g. server.register("/foo", mymodule.foohandler)

    server.register("/", home.page)
    server.register("/login", auth.loginpage)
    server.register("/logout",auth.logout)
    server.register("/profile/(.*)", profile.profile)
    server.register("/signup",profile.signup)
    server.register("/update_info",profile.update)
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
    server.register("/files/upload", upload.chk_ul_fields)
    server.register("/files/search", upload.file_search)
    server.register("/files/edit/(.*)", upload.file_edit)
    server.register("/files", upload.listmyfiles) #lists all files for current user
    server.register("/files/user/(.*)", upload.listuserfiles)
    server.register("/files/subject/(.*)", upload.listsubjectfiles)
    server.run()
