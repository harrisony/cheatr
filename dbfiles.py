import os
import sqlite3

DATANAME = os.path.join("data","DB_Files.sqlite")

conn = sqlite3.connect(DATANAME)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS "Files" ("fileid" TEXT PRIMARY KEY  NOT NULL  UNIQUE ,
"userid" TEXT NOT NULL , "ori_filename" TEXT NOT NULL , "subjectid" NUMBER NOT NULL ,
"description" TEXT NOT NULL , "timestamp" DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP);
""")



#This code will convert the userid and subjectid to a string 
class UploadedFile(object):
    def __init__(self, fileid, userid, ori_filename, subjectid, description):
        self.fileid = fileid
        self.userid = str(userid)
        self.ori_filename = ori_filename
        self.subjectid = int(subjectid)
        self.description = description

    def __repr__(self):
        return """File Object
           Fileid: %s
           Userid: %s
Original Filename: %s
        SubjectID: %i
      Description: %s
_________________________________________
""" % (self.fileid, self.userid, self.ori_filename, self.subjectid, self.description)
    
def getFilesUser(userid):
    results_files = []
    for item in repo:
        if repo[item].userid == str(userid):
            results_files.append(getFile(item))
    return results_files

def getFilesSubject(subjectid):
    results_files = []
    for item in repo:
        if repo[item].subjectid == subjectid:
            results_files.append(item)
    return results_files

def _addFileLocal(fileid, userid, ori_filename, subjectid, description):
    repo[fileid] = UploadedFile(fileid, userid, ori_filename, subjectid, description)

def addFile(fileid, userid, ori_filename, subjectid, description):
    if fileid in repo:
        raise NameError('This File Already Exists')
    cur.execute("INSERT into Files (fileid, userid, ori_filename, subjectid, description) VALUES (?, ?, ?, ?, ?);",
                (fileid, userid, ori_filename, subjectid, description))
    conn.commit()
    _addFileLocal(fileid, userid, ori_filename, subjectid, description)
    
def changefileinfo(fileid, subjectid, description):
    if fileid in repo:
        getFile(fileid).subjectid = subjectid
        getFile(fileid).description = description
    else:
        NameError('This File Does Not Exist')

def getFile(fileid):
    if fileid in repo:
        return repo[fileid]
    else:
        return None

repo = {}
cur.execute("SELECT * FROM Files")

for row in cur:
    _addFileLocal(str(row[0]), str(row[1]), str(row[2]), int(row[3]), str(row[4]))

try:
    addFile("1294464681.png", "123", "appleconf.png", 2, "A Desc")
    addFile("1294532619.png", "123", "asdf.png", 2, "Another Desc")
    addFile("1294531867.png", "124", "bbbb.png", 2, "Desc of B")
    addFile("1294464894.png", "124", "cccc.png", 2, "Desc of C")
except NameError:
    pass

