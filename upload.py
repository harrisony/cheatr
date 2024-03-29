from tornado import Server
from template_engine import template
from time import time
import os
import mimetypes
import dbfiles
import dbuser
import auth
import database_subject
ul_error_msg = ""
ul_file = ""
user = None
username = ""

def file_upload(response):
    auth.require_user(response)
    user = auth.get_user(response)
    if user == None:
        return
    else:
        username = user.get_username()    
    ul_error_msg = ""
    filename, content_type, data = response.get_file('to_upload')
    if response.get_field("ul_flag") == "True":
        # we did submit a form
        print"#####", response.get_field("subject")
        if data == None or response.get_field("subject") == None or response.get_field("category") == None or response.get_field("description") == None:
            ul_error_msg = "Make sure you have all fields filled in and have selected a file. If you have joined any subject(s), you cannot upload files."
        else:
            #A form was submitted with content. Proceed with upload
            print "a form was submitted"
            _do_upload(response)
            return
    # we did not submit a form or it's wrong
    print "loading page first time"
    listofsubjects = []
    for item in user.get_subjects():
        listofsubjects.append([item, database_subject.get_subject(item).get_name().replace("_", " ")])
        print "item", item
    context = {"css": "fileupload",
               "title": "File Uploader",
               "ul_err_msg": ul_error_msg,
               "ulsubjects": listofsubjects,
               "ulcategories": ["Notes", "Exam Paper","Exercises", "Solution"],
               "user": user}
    template.render_template("templates/fileupload.html", context, response)

def _do_upload(response):
    global ul_file, content_type
    sbjct = response.get_field('subject')
    categor = response.get_field('category')
    descr = response.get_field('description')
    filename, content_type, data = response.get_file('to_upload')
    currenttime = str(int(time()))
    while os.path.exists("static\\files\\" + currenttime):
        print "OS Path Exists"
        currenttime = str(int(time()))
    extension = "." + filename.split(".")[-1]
    serverfilename = currenttime + extension
    ul_file = os.path.join('static', 'files', serverfilename)
    #adding to list of all files
    user = auth.get_user(response)
    if user == None:
        return
    else:
        username = user.get_username()
    dbfiles.addFile(serverfilename, username, filename, sbjct, descr, categor)
    open(ul_file, 'wb').write(data)
    #Response after file upload success
    user = auth.get_user(response)
    context = {"css": "fileupload", "title": "File Uploader", "ori_file_name": filename, "server_file_location": currenttime+extension, "user": user}
    template.render_template("templates/uploadconfirmed.html", context, response)
##########################################################
    #dbfiles.increaseRank(serverfilename)

def file_search(response):
    auth.require_user(response)
    user = auth.get_user(response)
    if user == None:
        return
    else:
        username = user.get_username()

def file_edit(response, fileid):
    auth.require_user(response)
    user = auth.get_user(response)
    if user == None:
        return
    else:
        username = user.get_username()
    context = {"css": "fileupload",
               "title": "Edit File Info",
               "thefileid": fileid,
               "thefilename": all_files[fileid][0],
               "thefilesbjct": all_files[fileid][2],
               "thefiledescr": all_files[fileid][3]}
    template.render_template("templates/editfileinfo.html", context, response)

def listmyfiles(response):
    auth.require_user(response)
    user = auth.get_user(response)
    if user == None:
        return
    else:
        username = user.get_username()
    print username
    context = {"allfiles": dbfiles.getFilesUser(username), 'user':user, "css": "fileupload"}
    print context
    template.render_template("templates/listallfiles.html", context, response)
    
def listuserfiles(response):
    auth.require_user(response)
    user = auth.get_user(response)
    if user == None:
        return
    else:
        username = user.get_username()
    pass

def listsubjectfiles(response):
    auth.require_user(response)
    user = auth.get_user(response)
    if user == None:
        return
    else:
        username = user.get_username()
