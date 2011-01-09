import tornado
from template_engine import template

class User:
   def __init__(self, name, age, friends):
      self.name = name
      self.age = age
      self.friends = friends

def index(response):
   user = User("James", 11, [User('Gustav', 400, []), User('Svetlana', 21, []), User('Johan', 37, [])])
   context = {'user':user}
   template.render_template('templates/test_template_engine.html', context, response)
   
server = tornado.Server()
server.register('/', index)
server.run()
