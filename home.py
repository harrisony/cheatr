from template_engine import template
from tornado import Server
import user

def page(response):
    currentuser = user.User.get(response.get_field("user"))
    if currentuser == None:
        response.redirect("/signup")
    else:        
        context = {'title': 'Home Page',
                   'user': currentuser.get_username(),
                   'firstname': currentuser.get_first_name(),
                   'lastname' : currentuser.get_last_name(),
                   'subjects' : ['maths', 'english', 'physics', 'chemistry']}
        
        template.render_template("templates/home.html", context, response)

