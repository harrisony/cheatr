repo = {}
#This code will convert the userid and subjectid to a string 
class UploadedFile(object):
    def __init__(self, fileid, userid, ori_filename, subjectid, description):
        self.fileid = fileid
        self.userid = str(userid)
        self.ori_filename = ori_filename
        self.subjectid = str(subjectid)
        self.description = description
    
def getFilesUser(userid):
    results_files = []
    for item in repo:
        if repo[item].userid == str(userid):
            results_files.append(getFile(item))
    return results_files

def getFilesSubject(subjectid):
    results_files = []
    for item in repo:
        if repo[item].subjectid == str(subjectid):
            results_files.append(item)
    return results_files

def addFile(fileid, userid, ori_filename, subjectid, description):
    if fileid in repo:
        raise NameError('This File Already Exists')
    repo[fileid] = UploadedFile(fileid, userid, ori_filename, subjectid, description)

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


if __name__ == "__main__":
    addFile("applefinf.jpe", "123", "appleconf.jpg", 2, "A Desc")
    addFile("asdf.jpe", "123", "asdf.jpg", 2, "Another Desc")
    addFile("bbbb.jpe", "124", "bbbb.jpg", 2, "Desc of B")
    addFile("cccc.jpe", "124", "cccc.jpg", 2, "Desc of C")

