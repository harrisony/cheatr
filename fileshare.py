from tornado import Server
import os
import mimetypes

dct = {"David": ["1.doc", "2.doc", "a.jpg"],
       "Chris":["3.doc","4.doc","8.jpg"]}

FORM2 = """
<!DOCTYPE html>
<html>
<head>
	<link rel="shortcut icon" href="/favicon.ico" />
	<title>File Sharing</title>
</head>
<body>
<h1>hello %s, you are viewing %s's files</h1>
%s
</body>
</html>
"""

FORM = """
<html>
<head><title>Hello %s</title></head>
<body>
<form method="POST" enctype="multipart/form-data">
First name: <input type="text" name="firstname" />
<br />
Last name: <input type="text" name="lastname" />
<br />
<input type="file" name="photo" size="20">
<br />
Description: <input type="text" name="description" />
<input type="submit" name="submit" />
<br />
</form>
</body>
</html>
"""

def index(response):
    global photo, content_type
    firstname = response.get_field('firstname')
    lastname = response.get_field('lastname')
    filename, content_type, data = response.get_file('photo')
    if firstname is None:
        response.write(FORM)
        #read from remote host nlp6.it.usyd.edu.au: Connection reset by peer
    else:
        extension = mimetypes.guess_extension(content_type)
        photo = os.path.join('static', 'images', str(counter) + extension)
        open(photo, 'wb').write(data)
        fullname = '%s %s' % (firstname, lastname)
        photo_url = photo.replace("\\", "/") # URLs don't like backslashes
        response.write(RESULT % (fullname, fullname, photo_url))

def index(response, otherusr):
    name1 = response.get_field("name")
    links = "<ul>\n"
    for i in dct[otherusr]:
    links += '\t<li><a href="' + i + '">' + i + '</a></li>\n'
    links += "</ul>"
    response.write(FORM % (name1, otherusr, links))

server = Server()
server.register("/notes/(.*)", index)
server.run()
