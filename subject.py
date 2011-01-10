from tornado import Server
from template_engine import template
import database_subject

class English(object):
    def __init__(self):
        self.id = 1
        self.name = "English"
        self.description = "Standard English course for Year 12 HSC students"
        self.jurisdiction = 'NSW'
        self.grade = 12
        self.kla = "English"

subjects = {"English":English()}
top_resources = ['top1','top2','top3']
all_resources = ['all1','all2','all3']
#subjects = {"English":[2,3,"ghahd"], "Maths 2 Unit":[2,3,"dfg"], "Maths Extension 1":[2,3,"dfg"], "Maths Extension 2":[2,3,"dfg"]}


def createsubject(response):
    if (not response.get_field("subjectname") or
        not response.get_field("subject") or 
        not response.get_field("unit") or 
        not response.get_field("description")):
        template.render_template("templates/subject_create_template.html",
                                {"notification":"One or more of the fields are missing! ","enablebutton":True},
                                response)
    else:
        subjectname = response.get_field("subjectname")
        subjectunits = response.get_field("unit")
        subjectdescription = response.get_field("description")
        subjectcategory = response.get_field("subject")
        database_subject.create_subject(subjectname,subjectcategory,subjectunits,subjectdescription)
        response.write("Saved")

def viewsubject(response, subjectname, resourcetype, page):
    if not resourcetype:
        resourcetype = 'all'
    if not page:
        page = 1
    #info = database_subject.get_subject(subjectname)
    lower = (int(page) - 1 )*10 + 1
    upper = int(page)*10
    #top_resources = database_subject.get_resources(subjectname,resourcetype,lower,upper,True)
    #all_resources = database_subject.get_resources(subjectname,resourcetype,lower,upper,False)
    template.render_template("templates/subject_view_template.html",{"subject":subjects[subjectname],"top_resources":top_resources,"all_resources":all_resources},response)

def listsubject(response):
    template.render_template("templates/subject_list_template.html",{"subjectlist":database_subject.list_of_subjects()},response)
    targetsubject=response.get_field("subjectselected")
