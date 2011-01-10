from tornado import Server
from template_engine import template
import database_subject


#subjects = {"English":[2,3,"ghahd"], "Maths 2 Unit":[2,3,"dfg"], "Maths Extension 1":[2,3,"dfg"], "Maths Extension 2":[2,3,"dfg"]}


def subjectpage(response):
    if (not response.get_field("subjectname") or
        not response.get_field("subject") or 
        not response.get_field("unit") or 
        not response.get_field("description")):
        template.render_template("templates/subject_create_template.html",
                                 {"notification":
                                      "One or more of the fields are missing! ","enablebutton":True},
                                 response)
    else:
        subjectname = response.get_field("subjectname")
        subjectunits = response.get_field("unit")
        subjectdescription = response.get_field("description")
        subjectcategory = response.get_field("subject")
        database_subject.create_subject(subjectname,subjectcategory,subjectunits,subjectdescription)
        response.write("Saved")

def viewsubject(response, subjectname):
    info = database_subject.get_subject(subjectname)
    template.render_template("templates/subject_view_template.html",
                             {"subjectname":subjectname, "info":info, "subjectlist":subjects.keys()},
                             response)

def listsubject(response):
    template.render_template("templates/subject_list_template.html",{"subjectlist":database_subject.list_of_subjects()},response)
    targetsubject=response.get_field("subjectselected")
