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
if __name__ == "__main__":
    connection=sqlite3.connect("subject_database.db")
    cursor=connection.cursor()
    cursor.execute("DROP table if exists subjectlist")
    cursor.execute("""CREATE TABLE subjectlist (
                       id INTEGER PRIMARY KEY,
                       subject STRING NOT NULL,
                       category INTEGER NOT NULL,
                       unit INTEGER NOT NULL,
                       description STRING NOT NULL);""")
    for subject in SAMPLE_DATA:
            cursor.execute("INSERT INTO subjectlist (subject, category, unit, description) VALUES %s" % repr(subject))

    connection.commit()
    cursor.close() 
