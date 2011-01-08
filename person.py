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
        if User.exists(username)
            return User(_user_table[username])
        else:
            return Exception('No user: "%s"' % (username))
    @staticmethod
    def add(args):
        if User.exists(args['username'])
            return Exception('There is already a user called "%s"' % (args['username']))
        else:
            _user_table[args['username']] = args
    def __init__(self, args):
        self._args = args
        self._username = args['username']
        self._first_name = args['firstname']
        self._last_name = args['lastname']
        self._email = args['email']
        self._school = args['school']
        self._password_hash = sha256(args['password'])
    def __repr__(self):
        return "<Person username:%s>" % self._username
    def get_username(self):
        return self._username
    def get_first_name(self):
        return self._first_name
    def get_last_name(self):
        return self._last_name
    def get_email(self):
        return self._email
    def get_school(self):
        return self._school
    def get_password_hash(self):
        #TODO: this should be encrypted in some shape or form
        return self._password_hash
    def set_first_name(self, fname):
        self._args['firstname'] = fname
        self._firstname = self._args['firstname']
   def password_correct(self, password):
       if sha256(password) == self.get_password_hash():
           return True
        else:
            return False
User.add({'username': 'james', 'firstname': 'James', 'lastname':'Curran', 'school': 'usyd', 'email':'god@it.usyd.edu.au', 'password': 'ilovejava'})

