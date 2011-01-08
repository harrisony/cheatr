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
Amount of Units or Credits
<input type="radio" name="unit" value="1"> 1
<input type="radio" name="unit" value="2"> 2
<input type="radio" name="unit" value="3"> 3
<input type="radio" name="unit" value="4"> 4
</p>
<p>
Description of the Course
</p>
<p>
<textarea rows="3" cols="50" name="description"> </textarea>
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
<p>Category- %s</p>
<p>Amount of HSC Units- %i </p>
<p>Overview- %s</p>
<form method="POST">
<input type="submit" value="Confirm Subject Creation">
</form>
</body>
</head>
</html>
"""

VIEW = """
<html>
<head>
<body>
<ul>
<li><a href="http://localhost:8888/subject" + %s></li>
<li></li>
<li></li>
<li></li>
</ul>
</body>
</head>
</html>
"""

subjects = {}

def subjectpage(response):
    if response.get_field("subjectname") == None:
        response.write(FORM)
    else:
        subjectname = response.get_field("subjectname")
        subjectunits = response.get_field("unit")
        subjectdescription = response.get_field("description")
        subjectcategory = response.get_field("subject")
        subjects[subjectname]=[subjectcategory,subjectunits,subjectdescription]
        response.write("Saved")

def viewsubject(response, subjectname):
    info = subjects[subjectname]
    response.write(HTML % (info[0], int(info[1]), info[2]))

def listsubject(response):
    response.write(VIEW % (subjectname))
   
    
