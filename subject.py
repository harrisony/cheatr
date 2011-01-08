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
Amount of HSC Units
<input type="radio" name="unit" value=1> 1
<input type="radio" name="unit" value=2> 2
<input type="radio" name="unit" value=3> 3
<input type="radio" name="unit" value=4> 4
</p>
<p>
Description of the Course
</p>
<p>
<textarea rows="3" cols="50"> </textarea>
</p>
<p>There are 
60
character's left</p>
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
<p>Amount of HSC Units- %i </p>
<p>Category- %s</p>
<p>Overview- %s</p>
<form method="POST">
<input type="submit" value="Confirm Subject Creation">
</form>
</body>
</head>
</html>
"""

units = 2
overview = "This is a subject"
category = "Mathematics"

subjects = []

def subjectpage(response):
    if response.get_field("subjectname") == None:
        response.write(FORM)
    else:
        subjectname = response.get_field("subjectname")
        subjects.append(subjectname)


def viewsubject(response, subjectname):
    response.write(HTML % (units, category, overview))

