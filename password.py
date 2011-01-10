from tornado import Server
from dbuser import User
import auth
from template_engine import template

def change_password(response):
    auth.require_user(response)
    user = auth.get_user(response)
    if user == None:
        return
    old_password = response.get_field("old_password")
    new_password1 = response.get_field("new_password1")
    new_password2 = response.get_field("new_password2")
    output = ""
    context = {"title":"Change Your Password", "css":"password", "user":user}
    if old_password:
        if user.password_correct(old_password):
            if new_password1 == new_password2:
                user.set_password(new_password1)
                response.redirect("/profile/")
            else:
                context = {"title":"Change Your Password", "css":"password"}
                output = "Your password's did not match"
        else:
            output = "Incorrect password entered"
    context = {"title":"Change Your Password", "css":"password","output":output, "user":user}
    template.render_template("templates/change_password.html", context, response)
