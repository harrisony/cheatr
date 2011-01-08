import tornado
from template_engine import template

class User:
   def __init__(self, name, age):
      self.name = name
      self.age = age

def index(response):
   user = User("James", 10)
   context = {'user':user}
   template.render_template('static/html/template.html', context, response)
   
server = tornado.Server()
server.register('/', index)
server.run()
