from tornado import Server
dct={"David": ["1.doc", "2.doc", "a.jpg"],
     "Chris":["3.doc","4.doc","8.jpg"]}

FORM = """
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
