from tornado import Server
from dbuser import User
import os
import mimetypes
import friends
from template_engine import template


SIGNUP = """
<html>
<head><title>SIGN UP NOW!</title></head>
<body>
<h1>SIGN UP!</h1>
<h1>Create a user here</h1>
<form method="POST" action="signup"> 
Username: <input type="text" name="username" /><br />
First Name: <input type="text" name="firstname" /><br />
Last Name: <input type="text" name="lastname" /><br />
Email: <input type="text" name="email" /><br />
Create a Password: <input type="password" name="password" /><br />
Current School: <input type="text" name="school" /><br />
<input type="Submit" value="Sign Up" name="submit" />
</form>
</body>
</html>
"""

UPDATE = """
<html>
<head><title>Update Info</title></head>
<body>
<h1>Update Info</h1>
<form method="POST" action="update_info" enctype="multipart/form-data"> 
<input type="text" value="%s" name="username" hidden="true" /><br />
First Name: <input type="text" value="%s" name="firstname" /><br />
Last Name: <input type="text" value="%s" name="lastname" /><br />
Email: <input type="text" value="%s" name="email" /><br />
Create a Password: <input type="password" value="" name="password" /><br />
Current School: <input type="text" value="%s" name="school" /><br />
<br>
<br>
Upload Profile Picture:<br>

<input type="file" name="photo" size="20">

<br>
<input type="Submit" value="Update" name="submit" />
</form>
</body>
</html>
"""

def profile(response, username):
    user = User.get(username)
    name = clean(response.get_field("user"))

    print username
    if user is not None:
        firstname = user.get_first_name()
        lastname = user.get_last_name()
        email = user.get_email()
        school = user.get_school()
        #picture = user.get_profile_pic_path()
        picture = "/static/photos/gman.jpe"
        print "PICTURE IS: " + picture
        fullname = firstname + " " + lastname
        #response.write(OUTPUT % (username,username, picture,firstname,lastname,email,school,username))
        context = {"title":fullname, "user":username, "content":"Content", "profile_pic_location":picture,
                   "email":email, "school":school, "css": "profile", "friends":friends.get_friends(username), "User": User}
        template.render_template("templates/profile.html", context, response)
        
        
    else:
        response.redirect("/signup")
        
def signup(response):
    username = response.get_field("username")
    firstname = response.get_field("firstname")
    lastname = response.get_field("lastname")
    email = response.get_field("email")
    password = response.get_field("password")
    school = response.get_field("school")
    print username
    if username:
        newUser = {"username": username, "firstname":firstname,"lastname":lastname,"email":email,"password":password,"school":school}
        User.add(newUser)
        print " I am here"
        x = User.get(username)
        print x
        response.redirect("/profile/" + username)
    else:
        #response.write(SIGNUP)
        title = "Sign Up"
        context = {"title":title,}
        template.render_template("templates/signup.html", context, response)

def clean(string):
    if string == None:
        return None
    string = string.replace('"',"'").replace('<','>')
    return string

photo = ''

def update(response):
    global photo, content_type
    username = clean(response.get_field("username"))
    firstname = clean(response.get_field("firstname"))
    lastname = clean(response.get_field("lastname"))
    email = clean(response.get_field("email"))
    password = clean(response.get_field("password"))
    school = clean(response.get_field("school"))
    filename, content_type, data = response.get_file('photo')
        
    if username:
        try:
            extension = mimetypes.guess_extension(content_type)
            photo_path = os.path.join('static', 'photos', username + extension)
            open(photo_path, 'wb').write(data)
            photo_url = photo_path.replace("\\","/")
        except:
            photo_url = "/static/photos/default_male.jpg"
        fullname = '%s %s' % (username, lastname)
        
        user = User.get(username)
	#print user
        newUser = {"username": username, "firstname":firstname,"lastname":lastname,
                   "email":email,"password":password,"school":school, "profilepath":photo_url}
        print "NEW USER: " + str(newUser)
        #user = User.get(username)
        #print "User is " + user
        user.set_first_name(firstname)
        #User.add(newUser)
        #set_mutiple
        #x = User.get(username)
        
        response.redirect("/profile/" + username)
    else:
        name = response.get_field("name")
        user = User.get(name)
        password = user.get_password_hash()
        firstname = user.get_first_name()
        lastname = user.get_last_name()
        email = user.get_email()
        #password = user.get_password()
        school = user.get_school()
        #response.write(UPDATE % (name,firstname,lastname,email,school))
        title = "Updating " + firstname + " " + lastname
        context = {"title":title, "user":name, "username":name, "firstname":firstname,
                   "lastname":lastname, "email":email, "school":school,"password":password}
        template.render_template("templates/update.html", context, response)



   # def index(response):
    

    #else:
     #   response.write(RESULT %(username, username, photo_url))
        
