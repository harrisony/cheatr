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

count_id = 5
subjects = {"1":["English",2,3,"dfg"], "2":["Maths 2 Unit",2,3,"dfg"], "3":["Maths Extension 1",2,3,"dfg"], "4":["Maths Extension 2",2,3,"dfg"]}

def get_subject(subjectsid):
    cursor.execute("SELECT * FROM subjectlist WHERE id = '%s';" % subjectsid)
    result = cursor.fetchall()
def create_subject(name, category, unit, description):
    global count_id
    subjects[str(count_id)] = [name, category, unit, description]
    count_id += 1

def list_of_subjects():
    return subjects.keys()

if __name__ == "__main__":

    connection=sqlite3.connect("subject_database.sqlite")
    cursor=connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS subjectlist (
               id INTEGER AUTO_INCREMENT,
               subject STRING,
               category INTEGER,
               unit INTEGER,
               description STRING,
               PRIMARY KEY(id));""")
    for subject in SAMPLE_DATA:
        cursor.execute("INSERT INTO subjectlist (subject, category, unit, description) VALUES %s" % repr(subject))



