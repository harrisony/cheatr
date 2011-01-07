from tornado import Server

FORM = """
<html>
<head><title>Hello %s</title></head>
<body>
<form method="POST">
First name: <input type="text" name="firstname" />
Last name: <input type="text" name="lastname" />
DOB: <input type="text" name="dob" />
<input type="submit" name="submit />
</form>
</body>
</html>
"""

RESULT = """
<html>
<head><title>Hello %s</title></head>
<body>
<h1>Hello %s</h1>
</body>
</html>"""

def something(response):
   firstname = response.get_field('firstname')
   lastname = response.get_field('lastname')
   dob = response.get_field('dob')
   if firstname is None:
      response.write(FORM)
   else:
      fullname = '%s %s' % (firstname, lastname)
      response.write(RESULT % (fullname, lastname))
  
server = Server()
server.register('/', something)
server.run()