from tornado import Server

FORM="""
<html>
<head>
<title>New Subject</title>
<body>
<h1>Subject Creation Field</h1>
<form method="POST">
<input type="text" name="subjectname" /> :Subject Name
<p>
<input type="radio" name="subject" value=1> Mathematics
</p>
<p>
<input type="radio" name="subject" value=2> Computing
</p>
<p>
<input type="radio" name="subject" value=3> Science
</p>
<p>
<input type="radio" name="subject" value=4> Social Science
</p>
<p>
<input type="radio" name="subject" value=5> English/Philosophy
</p>
<p>
<input type="radio" name="subject" value=6> Languages
</p>
<p>
<input type="radio" name="subject" value=7> Other
</p>
<p>
<input type="reset" name="reset" value=Reset>
<p>
<input type='submit' value='Submit Selection'>
</p>
</form>
</body>
</head>
</html>
"""

HTML = """
<html>
<head>
<body>
<p>%i </p>
<p>%s</p>
<p>%s</p>
</body>
</head>
</html>
"""

units = 2
overview = "this is a subject"
category = "Mathematics"

subjects = []

def subjectpage(response):
    if response.get_field("subjectname") == None:
        response.write(FORM)
    else:
        subjectname = response.get_field("subjectname")
        subjects.append(subjectname)


def viewsubject(response, subjectname):
    response.write(HTML % (units, overview, category))

