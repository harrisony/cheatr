import sqlite3

#count_id = 5
#subjects = {"1":["English",2,3,"dfg"], "2":["Maths 2 Unit",2,3,"dfg"], "3":["Maths Extension 1",2,3,"dfg"], "4":["Maths Extension 2",2,3,"dfg"]}

#auth.require_user

class subject:
	def __init__(self,row):
		self.row = row

	def get_id(self):
		return self.row[0]
		
	def get_name(self):
		return self.row[1]
		
	def get_KLA(self):
		return self.row[2]
		
	def get_grade(self):
		return self.row[3]
		
	def get_jurisdiction(self):
		return self.row[4]
		
	def get_description(self):
		return self.row[5]

def get_subject(subjectsid):
        connection=sqlite3.connect("subject_database.db")
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM subjectlist WHERE id = '%s';" % subjectsid)
        result = cursor.fetchall()
        return subject(result[0])
##	output = []
##	for row in result:
##		output.append(subject(row))
##	cursor.close() 
##	return output
			 
def create_subject(name, KLA, grade, jurisdiction, description):
	connection=sqlite3.connect("subject_database.db")
	cursor=connection.cursor()
	#global count_id
	#subjects[str(count_id)] = [name, category, unit, description]
	#count_id += 1
	cursor.execute("INSERT INTO subjectlist (name, KLA, grade, jurisdiction, description) VALUES ('%s', '%s', '%s', '%s', '%s')" % (name, KLA, grade, jurisdiction, description)) 
	connection.commit()
	cursor.close() 
	
def list_of_subjects():
	connection=sqlite3.connect("subject_database.db")
	cursor=connection.cursor()
	cursor.execute("SELECT * FROM subjectlist")
	result = cursor.fetchall()
	tempoutput = []
	for row in result:
		tempoutput.append(subject(row))
	cursor.close() 
	return tempoutput
	