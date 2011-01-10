import sqlite3

if __name__ == "__main__":
    connection=sqlite3.connect("subject_database.db")
    cursor=connection.cursor()
    print 'hello'
    cursor.execute("DROP table subjectlist")
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
