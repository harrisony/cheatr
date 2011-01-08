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
    def __repr__(self):
        return "<Person username:%s>" % self._username
    def get_username(self):
        return self._username
    def get_first_name(self):
        return self._first_name
    def get_last_name(self):
        return self._last_name

User.add({'username': 'james', 'firstname': 'James', 'lastname':'Curran', 'school': 'usyd', 'email':'god@it.usyd.edu.au'})

