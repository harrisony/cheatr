from tornado import Server
from template_engine import template
from time import time
import os
import mimetypes
import dbfiles
import auth
username = "svet"
ul_error_msg = ""
ul_file = ""

def chk_ul_fields(response):
    ul_error_msg = ""
    filename, content_type, data = response.get_file('to_upload')
    if response.get_field("ul_flag") == "True":
        # we did submit a form
        if filename == None or content_type == None or data == None:
            ul_error_msg = "Please select a file to upload."
            print "no file"
        else:
            #A form was submitted with content. Proceed with upload
            "a form was submitted"
            upload(response)
            return
    # we did not submit a form or it's wrong
    print "loading page first time"
    context = {"css": "fileupload", "title": "File Uploader", "ul_err_msg": ul_error_msg}
    template.render_template("templates/fileupload.html", context, response)

def upload(response):
    global ul_file, content_type
    sbjct = response.get_field('subject')
    descr = response.get_field('description')
    filename, content_type, data = response.get_file('to_upload')
    currenttime = str(int(time()))
    while os.path.exists("static\\files\\" + currenttime):
        print "OS Path Exists"
        currenttime = str(int(time()))
    extension = mimetypes.guess_extension(content_type)
    serverfilename = currenttime + extension
    ul_file = os.path.join('static', 'files', serverfilename)
    #adding to list of all files
    dbfiles.addFile(serverfilename, username, filename, sbjct, descr)
    open(ul_file, 'wb').write(data)
    #Response after file upload success
    context = {"css": "fileupload", "title": "File Uploader", "ori_file_name": filename, "server_file_location": currenttime+extension}
    template.render_template("templates/uploadconfirmed.html", context, response)

def file_search(response):
    pass

def file_edit(response, fileid):
    context = {"css": "fileupload",
               "title": "Edit File Info",
               "thefileid": fileid,
               "thefilename": all_files[fileid][0],
               "thefilesbjct": all_files[fileid][2],
               "thefiledescr": all_files[fileid][3]}
    template.render_template("templates/editfileinfo.html", context, response)

def listmyfiles(response):
    context = {"allfiles": dbfiles.getFilesUser("124")}
    print context
    template.render_template("templates/listallfiles.html", context, response)
    
def listuserfiles(response):
    pass

def listsubjectfiles(response):
    pass
