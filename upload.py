from tornado import Server

from time import time
import os
import os.path
import mimetypes

# notice the HTTP method in the form has been changed to POST
ul_error_mgs = ""

FORM = """
<html>
<head><title>File Upload</title></head>
<body>
<form method="POST" enctype="multipart/form-data">
<input type="hidden" name="ul_flag" value="True"/>
<p><strong>%s</strong></p>
First name: <input type="text" name="firstname" />
<br />
Last name: <input type="text" name="lastname" />
<br />
<input type="file" name="to_upload" size="20">
<br />
Subject: <input type="text" name="subject" />
<br />
Description: <input type="text" name="subject" />
<br />
<input type="submit" name="submit" />
</form>
</body>
</html>
"""

RESULT = """
<html>
<head>
  <title>Hello %s</title>
</head>
<body>
<h1>Hello %s</h1>
<img src="/%s" />
</body>
</html>"""

ul_file = ""

def file_search(response):
    pass

def file_edit(response, fileid):
    pass

def chk_ul_fields(response):
    ul_error_mgs = ""
    filename, content_type, data = response.get_file('to_upload')
    if response.get_field("ul_flag") == "True":
        # we did submit a form
        if filename == None or content_type == None or data == None:
            ul_error_mgs = "Please select a file to upload."
        else:
            upload_page(response)
            return
    # we did not submit a form or it's wrong
    response.write(FORM % (ul_error_mgs))

def upload_page(response):
    global ul_file, content_type
    firstname = response.get_field('firstname')
    lastname = response.get_field('lastname')
    filename, content_type, data = response.get_file('to_upload')
    if firstname is None:
        response.write(FORM)
        #read from remote host nlp6.it.usyd.edu.au: Connection reset by peer
    else:
        currenttime = str(int(time()))
        while os.path.exists("static\\files\\" + currenttime):
            print "OS Path Exists"
            currenttime = str(int(time()))
        extension = mimetypes.guess_extension(content_type)
        ul_file = os.path.join('static', 'files', currenttime + extension)
        open(ul_file, 'wb').write(data)
        fullname = '%s %s' % (firstname, lastname)
        file_url = ul_file.replace("\\", "/") # URLs don't like backslashes
        response.write(RESULT % (fullname, fullname, file_url))

