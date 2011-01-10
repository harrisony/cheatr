from template_engine import template
from tornado import Server
import user
import auth

def page(response):
    #user = User.get(username)
    auth.require_user(response)
    user = auth.get_user(response)
    print "name: " + str(user)
    if user == None:
        response.redirect("/login")
    else:        
        context = {'title': 'Home Page',
                   
                   'firstname': user.get_first_name(),
                   'lastname' : user.get_last_name(),
                   'subjects' : ['maths', 'english', 'physics', 'chemistry'],
				   'wallorfeed':'feedupdate',
				   'user':user,
				   'current_Wall':user.get_username()
				   }

                   

        
        template.render_template("templates/home.html", context, response)

