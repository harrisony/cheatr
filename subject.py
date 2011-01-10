from tornado import Server
from template_engine import template
import database_subject
import auth
import dbfiles
from operator import itemgetter, attrgetter

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
		response.redirect("/")

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

def rankcmp(file1, file2):
    if file1.rank < file2.rank:
        return -1
    elif file1.rank > file2.rank:
        return 1
    else:
        return 0
		
def viewsubject(response, subjectid, resourcetype, page):
    auth.require_user(response)
    if not resourcetype:
        resourcetype = 'All'
    if not page:
        page = 1
    user = auth.get_user(response)
    info = database_subject.get_subject(int(subjectid))
    lower = (int(page) - 1 )*10
    upper = int(page)*10 - 1
    
    top_resources = dbfiles.getFilesSubject(int(subjectid))
    sorted(top_resources, key=attrgetter('rank'), reverse=True)
    #eliminate those without the correct type
    new_top = []
    if len(top_resources):
        for s in top_resources:
            if s.category == resourcetype or resourcetype == 'All':
                new_top.append(s)
        top_resources = new_top[lower:upper]

    all_resources = dbfiles.getFilesSubject(int(subjectid))
    sorted(all_resources, key=attrgetter('ori_filename'))
    if len(all_resources):
        new_all = []
        for s in all_resources:
            if s.category == resourcetype or resourcetype == 'All':
                new_all.append(s)
        all_resources = new_all[lower:upper]

    template.render_template("templates/subject_view_template.html",{"user":user,"subject":info,"top_resources":top_resources,"all_resources":all_resources},response)

def mysubjects(response):
	pass

def listsubject(response):
    user = auth.get_user(response)
    template.render_template("templates/subject_list_template.html",{"user":user,"subjectlist":database_subject.list_of_subjects()},response)
    targetsubject=response.get_field("subjectselected")


	
	