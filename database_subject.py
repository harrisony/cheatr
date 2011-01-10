import sqlite3

SAMPLE_DATA = [('2_Unit_Maths','Maths',2,'Cool stuff'),
('3_Unit_Maths','Maths',3,'More cool stuff'),
('4_Unit_Maths','Maths',4,'Cool stuff'),
('2_Unit_English','English',2,'...'),
('3_Unit_English','English',3,'....'),
('4_Unit_English','English',4,'.....'),
('Software','Computing',2,'.'),
('Information','Computing',2,'.'),
('Physics','Science',2,'.'),
('Chemistry','Science',2,'.'),
('Biology','Science',2,'.'),
('Engineering','Maths',2,'.')]

#count_id = 5
#subjects = {"1":["English",2,3,"dfg"], "2":["Maths 2 Unit",2,3,"dfg"], "3":["Maths Extension 1",2,3,"dfg"], "4":["Maths Extension 2",2,3,"dfg"]}

def get_subject(subjectsid):
    connection=sqlite3.connect("subject_database.db")
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM subjectlist WHERE id = '%s';" % subjectsid)
    result = cursor.fetchall()
    cursor.close() 
    return result
             
def create_subject(name, category, unit, description):
    connection=sqlite3.connect("subject_database.db")
    cursor=connection.cursor()
    #global count_id
    #subjects[str(count_id)] = [name, category, unit, description]
    #count_id += 1
    cursor.execute("INSERT INTO subjectlist (subject, category, unit, description) VALUES ('%s', '%s', %i, '%s')" % (name, category, unit, description)) 
    connection.commit()
    cursor.close() 
    
def list_of_subjects():
    connection=sqlite3.connect("subject_database.db")
    cursor=connection.cursor()
    cursor.execute("SELECT id, subject FROM subjectlist")
    result = cursor.fetchall()
    cursor.close() 
    return result



