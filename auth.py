from template_engine import template
from dbuser import User

def loginpage(response):
    username = response.get_cookie("User")
    page = response.get_field("page")
    if not page:
        page = "/"
    context = {"title":"Login", "output":"", "username":"", "page":page, "css":"login"}    
    if username:
        user = User.get(username)
        context["output"] = "Hello " + user.get_first_name()
        context["username"] = username
        context["firstname"] = user.get_first_name()
        response.redirect("/")
    else:
        username = response.get_field("username")
        if username:
            login(response, context)
    template.render_template("templates/login.html", context, response)

def login(response, context):
    #logout(response)
    page = response.get_field("page")
    if not page:
        page = "/"
    username = response.get_field("username")
    password = response.get_field("password")

    if User.exists(username):
        user = User.get(username)
        context["firstname"] = user.get_first_name()
        context["username"] = username
        context["css"] = "login"
        if user.password_correct(password):
            message = "username: " + username + " password: " + password
            firstname = user.get_first_name()
            context["output"] = message
            response.set_cookie("User",username)
            response.redirect(page)
        else:
            message = "Wrong Password"
            firstname = user.get_first_name()
            context["output"] = message
    else:
        message = "User does not exist"
        context["output"] = message
        response.redirect(page)

def logout(response):
    require_user(response)
    response.set_cookie("User","")
    response.redirect("/login")

def get_user(response):
    if response.get_cookie("User"):
        return User.get(response.get_cookie("User"))
    else:
        return None
    
def require_user(response):
    if get_user(response):
        return 
    else:
        response.redirect("/login?page=" + response.request.uri)
