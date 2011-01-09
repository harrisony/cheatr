from tornado import Server
from template_engine import template

subjects = {}
subjectlist=["English", "Maths 2 unit", "Maths Extension 1", "Maths Extension 2"]

def subjectpage(response):
    if response.get_field("subjectname") == None:
        template.render_template("templates/subject_create_template.html",{},response)
    else:
        subjectname = response.get_field("subjectname")
        subjectunits = response.get_field("unit")
        subjectdescription = response.get_field("description")
        subjectcategory = response.get_field("subject")
        subjects[subjectname]=[subjectcategory,subjectunits,subjectdescription]
        response.write("Saved")

def viewsubject(response, subjectname):
    info = subjects[subjectname]
    template.render_template("templates/subject_view_template.html",{"info1":info[0], "info2":int(info[1]), "info3":info[2]},response)
    #response.write(HTML % (info[0], int(info[1]), info[2]))
        

def listsubject(response):
    template.render_template("templates/subject_list_template.html",{"subject_name":subjectname},response)
    #response.write(VIEW % (subjectname))
    targetsubject=response.get_field("subjectselected")
