from tornado import Server
import template

class User:
   def __init__(self, name, age):
      self.name = name
      self.age = age

def index(response):
   user = User("James", 10)
   context = {'user':user}
   index_template = open('test.html', 'rU').read()
   response.write(template.render_view(index_template, context))
   
server = Server()
server.register('/', index)
server.run()