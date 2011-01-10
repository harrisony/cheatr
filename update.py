from tornado import Server
from dbuser import User
import os
import mimetypes
import friends
import auth
from template_engine import template

def update(response):
    auth.require_user(response)
    user = auth.get_user(response)
    global photo, content_type
    username = response.get_field("username")
    firstname = response.get_field("firstname")
    lastname = response.get_field("lastname")
    email = response.get_field("email")
    password = response.get_field("password")
    school = response.get_field("school")
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
    if username and firstname and lastname:
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
        #context = {"title":title, "user":username, "username":username, "firstname":firstname,
        #           "lastname":lastname, "email":email, "school":school,"password":password}
        print "NEW USER: " + str(newUser)
        #user.set_first_name(firstname)
        user.set_multiple(newUser)
        #template.render_template("templates/update.html", context, response)
        response.redirect("/profile/")
    else:
        password = user.get_password_hash()
        firstname = user.get_first_name()
        lastname = user.get_last_name()
        email = user.get_email()
        #password = user.get_password()
        school = user.get_school()
        #response.write(UPDATE % (name,firstname,lastname,email,school))
        title = "Updating " + firstname + " " + lastname
        context = {"title":title, "user":username, "username":username, "username":username, "firstname":firstname,
                   "lastname":lastname, "email":email, "school":school,"password":password}
        template.render_template("templates/update.html", context, response)
