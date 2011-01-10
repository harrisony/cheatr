from tornado import Server
from template_engine import template
import database_subject
import auth

def createpage(response):
	
	if auth.get_user(response):
		
		if (not response.get_field("name") or
			not response.get_field("KLA") or 
			not response.get_field("grade") or 
			not response.get_field("jurisdiction") or 
			not response.get_field("description")):
			template.render_template("templates/subject_create_template.html",
									 {"notification":
										  "One or more of the fields are missing! ","enablebutton":True},
									 response)
		else:
			name = response.get_field("name")       
			KLA = response.get_field("KLA")
			grade = response.get_field("grade")
			jurisdiction = response.get_field("jurisdiction")
			description = response.get_field("description")
			database_subject.create_subject(name,KLA,grade,jurisdiction,description)
			response.write("Saved")
	else:
		response.write("You are not logged in")

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

def viewsubject(response, subjectid, resourcetype, page):
    if not resourcetype:
        resourcetype = 'all'
    if not page:
        page = 1
    info = database_subject.get_subject(subjectid)
    lower = (int(page) - 1 )*10 + 1
    upper = int(page)*10
    top_resources = ['top1','top2','top3']
	#top_resources = database_subject.get_resources(subject,resourcetype,lower,upper,True)
    all_resources = ['all1','all2','all3']
	#all_resources = database_subject.get_resources(subject,resourcetype,lower,upper,False)
    template.render_template("templates/subject_view_template.html",{"subject":info,"top_resources":top_resources,"all_resources":all_resources},response)

def listsubject(response):
    template.render_template("templates/subject_list_template.html",{"subjectlist":database_subject.list_of_subjects()},response)
    targetsubject=response.get_field("subjectselected")
