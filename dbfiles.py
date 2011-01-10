import os
import sqlite3

DATANAME = os.path.join("data","DB_Files.sqlite")

conn = sqlite3.connect(DATANAME)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS "Files" ("fileid" TEXT PRIMARY KEY  NOT NULL  UNIQUE ,
"userid" TEXT NOT NULL , "ori_filename" TEXT NOT NULL , "subjectid" NUMBER NOT NULL ,
"description" TEXT NOT NULL , "timestamp" DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP,
"category" TEXT NOT NULL  DEFAULT "Notes" , "rank" FLOAT NOT NULL  DEFAULT 0);
""")



#This code will convert the userid and subjectid to a string 
class UploadedFile(object):
    def __init__(self, fileid, userid, ori_filename, subjectid, description, category, rank):
        self.fileid = fileid
        self.userid = str(userid)
        self.ori_filename = ori_filename
        self.subjectid = int(subjectid)
        self.description = description
        self.category = category
        self.rank = rank

    def __repr__(self):
        return """File Object
           Fileid: %s
           Userid: %s
Original Filename: %s
        SubjectID: %i
      Description: %s
         Category: %s
             Rank: %f
_________________________________________
""" % (self.fileid, self.userid, self.ori_filename, self.subjectid, self.description, self.category, self.rank)
    
def getFilesUser(userid):
    results_files = []
    for item in repo:
        if repo[item].userid == str(userid):
            results_files.append(repo[item])
    return results_files

def getFilesSubject(subjectid):
    results_files = []
    for item in repo:
        if repo[item].subjectid == subjectid:
            results_files.append(repo[item])
    return results_files

def _addFileLocal(fileid, userid, ori_filename, subjectid, description, category, rank):
    repo[fileid] = UploadedFile(fileid, userid, ori_filename, subjectid, description, category, rank)

def addFile(fileid, userid, ori_filename, subjectid, description, category):
    if fileid in repo:
        raise NameError('This File Already Exists')
    cur.execute("INSERT into Files (fileid, userid, ori_filename, subjectid, description, category, rank) VALUES (?, ?, ?, ?, ?, ?, 0.0);",
                (fileid, userid, ori_filename, subjectid, description, category))
    conn.commit()
    _addFileLocal(fileid, userid, ori_filename, subjectid, description, category, 0.0)
    
def changefileinfo(fileid, subjectid, description, category):
##############################################################################
    #make sure this modifies the database and dictionary
    if fileid in repo:
        getFile(fileid).subjectid = subjectid
        getFile(fileid).category = category
        getFile(fileid).description = description
    else:
        NameError('This File Does Not Exist')

def getFile(fileid):
    if fileid in repo:
        return repo[fileid]
    else:
        return None

def increaseRank(fileid):
    if fileid in repo:
        getFile(fileid).rank += 1.0
        cur.execute("UPDATE Files SET rank = (rank + 1) WHERE fileid = ?;", (str(fileid)))
        conn.commit()
    else:
        NameError('This File Does Not Exist')

repo = {}
cur.execute("SELECT * FROM Files")

for row in cur:
    _addFileLocal(str(row[0]), str(row[1]), str(row[2]), int(row[3]), str(row[4]), str(row[6]), float(row[7]))

