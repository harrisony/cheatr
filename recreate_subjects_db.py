import sqlite3
SAMPLE_DATA = [('Mathematics','Maths','Year 11','NSW', 'Maths course'),
('3_Unit_Maths','Maths','Year 11','NSW', 'An extension of the maths course'),
('4_Unit_Maths','Maths','Year 12', 'NSW', 'Another extension of the maths course - not for the light-hearted'),
('Advanced_English','English','Year 11', 'NSW','Boring'),
('3_Unit_English','English','Year 11','NSW','Very boring'),
('4_Unit_English','English','Year 12','NSW','My goodness, boring'),
('Software, Design and Development','Computing','Year 11','NSW','Concentrates on programming'),
('Information Processes and Technology','Computing','Year 11','NSW','Focuses on the business side of IT'),
('Physics','Science','Year 11','NSW','Maths and science...'),
('Chemistry','Science','Year 11','NSW','6.0223*10^23'),
('Biology','Science','Year 11','NSW','Genes and stuff.. '),
('Engineering_Studies','Maths','Year 11','NSW','The study of engineering')]
connection=sqlite3.connect("subject_database.db")
cursor=connection.cursor()
cursor.execute("DROP table if exists subjectlist")
cursor.execute("""CREATE TABLE subjectlist (
                   id INTEGER PRIMARY KEY,
                   name STRING NOT NULL,
                   KLA INTEGER NOT NULL,
                   grade STRING NOT NULL,
                   jurisdiction STRING NOT NULL,
                   description STRING NOT NULL);""")
for subject in SAMPLE_DATA:
        cursor.execute("INSERT INTO subjectlist (name, KLA, grade, jurisdiction, description) VALUES %s" % repr(subject))

connection.commit()
cursor.close() 
