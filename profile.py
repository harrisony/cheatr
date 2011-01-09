from tornado import Server
from user import User
import os
import mimetypes
from template_engine import template

Users = { "Nick": {"firstname":"Nicholas","lastname":"Cooke","email":"nicholas.cooke1@gmail.com","password":"abc123","school":"Model Farms High"},
          "Jennifer": {"firstname":"Jennifer","lastname":"Truong","email":"jenni_truong@hotmail.com","password":"password","school":"St George Girls High"}}


newUser = {"username": "Nick", "firstname":"Nick","lastname":"Cooke","email":"email","password":"password","school":"school"}
User.add(newUser)

OUTPUT = """
<html>
<head><title>%s's Profile</title>
<style>
p {
    padding:0;
    margin:0;
}
</style>
<nav>
<ul>
<li><a href='/'>Home</a></li>
<li>Resources
<ul>
<li><a href='/'>Notes</a></li>
<li><a href='/'>Past Papers</a></li>
</ul>
</head>
<body>
<h1>%s's Profile</h1>
<img src='%s'>
<p>First Name: %s</p>
<p>Last Name: %s</p>
<p>Email: %s</p>
<p>School: %s</p>
<p><a href="../update_info?name=%s" >Update Info</a></p>
</body>
</html>
"""

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
    if user is not None:
        firstname = user.get_first_name()
        lastname = user.get_last_name()
        email = user.get_email()
        school = user.get_school()
        picture = user.get_profile_pic_path()
        fullname = firstname + " " + lastname
        #response.write(OUTPUT % (username,username, picture,firstname,lastname,email,school,username))
        context = {"title":fullname, "user":username, "content":"<p>Hello</p>"}
        template.render_template("templates/profile.html", context, response)
    else:
        response.redirect("../signup")
        
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
        response.write(SIGNUP)

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
        print "username is " + username
        
        extension = mimetypes.guess_extension(content_type)
        photo_path = os.path.join('static', 'photos', username + extension)
        open(photo_path, 'wb').write(data)
        fullname = '%s %s' % (username, lastname)
        photo_url = photo_path.replace("\\","/")
        
        newUser = {"username": username, "firstname":firstname,"lastname":lastname,"email":email,"password":password,"school":school}
        #user = User.get(username)
        #print "User is " + user
        user.set_mutiple(newUser)
        #User.add(newUser)
        #set_mutiple
        #x = User.get(username)
        
        response.redirect("/profile/" + username)
    else:
        name = response.get_field("name")
        user = User.get(name)
        firstname = user.get_first_name()
        lastname = user.get_last_name()
        email = user.get_email()
        #password = user.get_password()
        school = user.get_school()
        response.write(UPDATE % (name,firstname,lastname,email,school))




   # def index(response):
    

    #else:
     #   response.write(RESULT %(username, username, photo_url))
        
