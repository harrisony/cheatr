from tornado import Server
from template_engine import template

subjects = {}
subjectlist=["English", "Maths 2 Unit", "Maths Extension 1", "Maths Extension 2"]

def subjectpage(response):
    if (not response.get_field("subjectname") or
        not response.get_field("subject") or 
        not response.get_field("unit") or 
        not response.get_field("description")):
        template.render_template("templates/subject_create_template.html",
                                 {"notification":
                                      "One or more of the fields are missing! "},
                                 response)
    else:
        subjectname = response.get_field("subjectname")
        subjectunits = response.get_field("unit")
        subjectdescription = response.get_field("description")
        subjectcategory = response.get_field("subject")
        subjects[subjectname]=[subjectcategory,subjectunits,subjectdescription]
        response.write("Saved")

def viewsubject(response, subjectname):
    info = subjects[subjectname]
    template.render_template("templates/subject_view_template.html",
                             {"info1":info[0], "info2":int(info[1]),
                              "info3":info[2]},
                             response)

def listsubject(response):
    template.render_template("templates/subject_list_template.html",{"subject_name":subjectname},response)
    #info = subjects[subjectname]
    targetsubject=response.get_field("subjectselected")
