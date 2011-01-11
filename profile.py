from tornado import Server
from dbuser import User
import os
import mimetypes
import friends
from friends import *
import auth
from template_engine import template


def profile(response, username):
    auth.require_user(response)
    user = auth.get_user(response)
    if user == None:
        return
    if not username:
        username = user
    else:
        username = User.get(username)
    if user is not None:
        firstname = username.get_first_name()
        lastname = username.get_last_name()
        email = username.get_email()
        school = username.get_school()
        interests = {"activities":None, "tv":None}
        about = {"birthday":None, "age":None, "website":None}
        education = {"school":None,"subjects":None,"state":None,"grade":None}
        picture = username.get_profile_pic_path()
        if not picture:
            picture = "/static/images/default_avatar.jpeg"
        print "PICTURE IS: " + picture
        fullname = firstname + " " + lastname
        
        context = {"title":fullname, 'wallorfeed':'wallupdate',
                   "username":username.get_username(),'current_Wall':username.get_username(), "profile_pic_location":picture,
                   "email":email, "school":school, "css": "profile", "friends":friends.get_friends(username.get_username()), "user": user,
                   "interests": interests, "about": about, "education":education,"user":user,'can_use_wall':can_use_wall(user,username.get_username())}
        template.render_template("templates/profile.html", context, response)
        
def signup(response):
    username = response.get_field("username")
    firstname = response.get_field("firstname")
    lastname = response.get_field("lastname")
    email = response.get_field("email")
    password = response.get_field("password")
    school = response.get_field("school")
    print username
    if username and email and firstname and lastname and password and not User.exists(username):
        newUser = {"username": username, "firstname":firstname,"lastname":lastname,"email":email,"password":password,"school":school}
        User.add(newUser)
        print " I am here"
        x = User.get(username)
        print x
        # we're going to be hacky, and manually set a cookie, which shouldn't happen -
        # but we want to prevent the user from being redirected to the login page, straight
        # after signing up.
        response.set_cookie("User", username)
        response.redirect("/profile/" + username)
    else:
        #response.write(SIGNUP)
        title = "Sign Up"
        context = {"title":title, "css":"signup", "user":None}
        template.render_template("templates/signup.html", context, response)

def clean(string):
    if string == None:
        return None
    string = string.replace('"',"'").replace('<','>')
    return string

photo = ''
update = """
def update(response):
    auth.require_user(response)
    user = auth.get_user(response)
    global photo, content_type
    username = clean(user.get_username())
    firstname = clean(response.get_field("firstname"))
    lastname = clean(response.get_field("lastname"))
    email = clean(response.get_field("email"))
    #password = clean(response.get_field("password"))
    password = "gus"
    school = clean(response.get_field("school"))
    filename, content_type, data = response.get_file('photo')
    print "content_type: " + str(content_type)
    if content_type == None:
        photo_url = user.get_profile_pic_path()
    else:
        extension = mimetypes.guess_extension(content_type)
        photo_path = os.path.join('static', 'photos', username + extension)
        print "updating.."
        open(photo_path, 'wb').write(data)
        photo_url = '/' + photo_path.replace("\\","/")
        print photo_url
    if user:
        #extension = mimetypes.guess_extension(content_type)
        #photo_path = os.path.join('static', 'photos', username + extension)
        #print "updating.."
        #open(photo_path, 'wb').write(data)
        #photo_url = '/' + photo_path.replace("\\","/")
        #print photo_url
        #user.set_profile_pic_path(photo_url)
        fullname = '%s %s' % (firstname, lastname)
        newUser = {"username": username, "firstname":firstname,"lastname":lastname,
                   "email":email,"password":password,"school":school, "profilepath":photo_url}
        context = {"title":title, "user":username, "username":username, "firstname":firstname,
                   "lastname":lastname, "email":email, "school":school,"password":password}
        print "NEW USER: " + str(newUser)
        #user.set_first_name(firstname)
        user.set_multiple(newUser)
        template.render_template("templates/update.html", context, response)
        #response.redirect("/profile/")
    else:
        password = user.get_password_hash()
        firstname = user.get_first_name()
        lastname = user.get_last_name()
        email = user.get_email()
        #password = user.get_password()
        school = user.get_school()
        #response.write(UPDATE % (name,firstname,lastname,email,school))
        title = "Updating " + firstname + " " + lastname
        context = {"title":title, "user":username, "username":username, "firstname":firstname,
                   "lastname":lastname, "email":email, "school":school,"password":password}
        template.render_template("templates/update.html", context, response)
"""
