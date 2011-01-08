from hashlib import sha256
_user_table = {}
class User:
    @staticmethod
    def exists(username):
        if username in _user_table:
            return True
        else:
            return False
    @staticmethod
    def get(username):
        if User.exists(username):
            return User(_user_table[username])
        else:
            return None
    @staticmethod
    def add(args):
        if 'username' not in args:
            return Exception('No username provided')
        elif User.exists(args['username']):
            return Exception('There is already a user called "%s"' % (args['username']))
        else:
            _user_table[args['username']] = args
    def __init__(self, args):
        self._set_blank()
        for k,v in args.items():
            exec "self._%s = '%s'" % (k,v)
        #self._args = args
        #self._username = args['username']
        #self._first_name = args['firstname']   
        #self._last_name = args['lastname']
        #self._email = args['email']
        #self._school = args['school']
        #self._password_hash = sha256(args['password'])
    def _set_blank(self):
        self._args = {}
        self._username = ''
        self._firstname = ''
        self._lastname = ''
        self._email = ''
        self._school = ''
        self._passwordhash = ''
        self._profilepicpath = ''
    def __repr__(self):
        return "<Person username:%s>" % self._username
    def get_username(self):
        return self._username
    def get_first_name(self):
        return self._firstname
    def get_last_name(self):
        return self._lastname
    def get_email(self):
        return self._email
    def get_school(self):
        return self._school
    def get_password_hash(self):
        return self._password_hash.hexdigest()
    def get_profile_pic_path(self):
        return self._profilepicpath
    def set_mutiple(self, args):
        mapping = {'firstname': self.set_first_name, 'lastname': self.set_last_name, 'email': self.set_email, 'school': self.set_school,
                   'password': self.set_password}
        for k,v in args.items():
            func = mapping[k]
            func(v)
    def set_email(self, email):
        self._args['email'] = email
        self._email = email
    def set_first_name(self, fname):
        self._args['firstname'] = fname
        self._firstname = fname
    def set_last_name(self, lname):
        self._args['lastname'] = lname
        self._lastname = lname
    def set_profile_pic_path(self, path):
        self._args['profilepath'] = path
        self._profile_pic_path = path
    def set_school(self, school):
        self._args['school'] = school
        self._school = school
    def set_password(self, pword):
        self._args['password'] = sha256(password).hexdigest()
        self._password = sha256(password).hexdigest()
    def password_correct(self, password):
        if sha256(password).hexdigest() == self.get_password_hash():
           return True
        else:
            return False
            
User.add({'username': 'james', 'firstname': 'James', 'lastname':'Curran', 'school': 'usyd', 'email':'god@it.usyd.edu.au', 'password': 'ilovejava'})
User.add({'username': 'gman', 'firstname':'Gustav', 'lastname': 'Olafsen', 'school': 'unsw', 'email': 'gustav@isacoolperson.com', 'password': 'gus'})
User.add({'username': 'smythey', 'firstname': 'Johan', 'lastname': 'Smythe', 'school': 'usyd', 'email': 'smythey@usyd.edu.au', 'password': 'iloveusyd'})
User.add({'username': 'svet', 'firstname': 'Svetlana', 'lastname': 'Roshenkev', 'school': 'school of fail', 'email': 'a@example.com', 'password': 'ytrewq'})