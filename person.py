class Person:
    self.friends = []
    self.username = ''
    self.first_name = ''
    self.last_name = ''
    self.subjects = []
    def __init__(self, args):
        
        self.username = args['username']
        self.first_name = args['firstname']
        self.last_name = args['lastname']
        self.email = args['email']
        #self.last_name = name[1]
        #self.subjects = list(subjects)
    def __repr__(self):
        n = self.first_name, self.last_name
        return "<Person uid:%s name:%s>" % (self.uid, n)
    # Python 2.6 provides @properties. We're using python 2.5, grr
    def uid(self):
        return str(self.uid)
    def name(self):
        return (self.first_name,self.last_name)
    def subjects(self):
        return tuple(self.subjects)
    def add_friend(self,uid):
        return NotImplementedError
    def remove_friend(self, uid)
        return NotImplementedError
    def friends(self):
        return NotImplementedError
        
#example_person1 = Person(0,('James', 'Curran'), ('English', 'Maths', 'Science'))
#example_person2 = Person(1,('Tara', 'Murphy'), ('Computing', 'Maths'))
#example_person3 = Person(2,('Alan', 'Su'), ('History', 'Maths'))
example_person1 = Person({'firstname': 'James', 'lastname':'Curran', 'school': 'usyd', 'email':'god@it.usyd.edu.au'})