from tornado import Server

Users = { "Nicholas": {"firstname":"Nicholas","lastname":"Cooke","email":"nicholas.cooke1@gmail.com","password":"abc123","school":"Model Farms High"},
          "Jennifer": {"firstname":"Jennifer","lastname":"Truong","email":"jenni_truong@hotmail.com","password":"password","school":"St George Girls High"}}

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
<form method="POST" action="update_info"> 
<input type="hidden" value="%s" name="username" /><br />
First Name: <input type="text" value="%s" name="firstname" /><br />
Last Name: <input type="text" value="%s" name="lastname" /><br />
Email: <input type="text" value="%s" name="email" /><br />
Create a Password: <input type="password" value="%s" name="password" /><br />
Current School: <input type="text" value="%s" name="school" /><br />
<input type="Submit" value="Update" name="submit" />
</form>
</body>
</html>
"""

def profile(response, username):
    #print username
    if username in Users:
        firstname = Users[username]["firstname"]
        lastname = Users[username]["lastname"]
        email = Users[username]["email"]
        school = Users[username]["school"]
        response.write(OUTPUT % (username,username,firstname,lastname,email,school,username))
    else:
        response.write(SIGNUP)
        
def signup(response):
    username = response.get_field("username")
    firstname = response.get_field("firstname")
    lastname = response.get_field("lastname")
    email = response.get_field("email")
    password = response.get_field("password")
    school = response.get_field("school")
    if username:
        newUser = {"firstname":firstname,"lastname":lastname,"email":email,"password":password,"school":school}
        Users[username] = newUser
        response.redirect("/profile/" + username)
    else:
        response.write(SIGNUP)
    #print Users

def clean(string):
    if string == None:
        return None
    string = string.replace('"',"'").replace('<','>')
    return string

def update(response):
    username = clean(response.get_field("username"))
    firstname = clean(response.get_field("firstname"))
    lastname = clean(response.get_field("lastname"))
    email = clean(response.get_field("email"))
    password = clean(response.get_field("password"))
    school = clean(response.get_field("school"))
    name = clean(response.get_field("name"))
    print username
    if username:
        newUser = {"firstname":firstname,"lastname":lastname,"email":email,"password":password,"school":school}
        Users[username] = newUser
        response.redirect("/profile/" + username)
    else:
        response.write(UPDATE % (name,Users[name]["firstname"],
                                 Users[name]["lastname"],Users[name]["email"],
                                 Users[name]["password"],Users[name]["school"]))
