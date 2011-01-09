import tornado
from template_engine import template

class User:
   def __init__(self, name, age):
      self.name = name
      self.age = age

def index(response):
   user = User("James", 11)
   context = {'user':user}
   template.render_template('templates/test_template_engine.html', context, response)
   
server = tornado.Server()
server.register('/', index)
server.run()
