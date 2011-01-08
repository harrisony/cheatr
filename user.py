_user_table = {}
class User:
    @staticmethod
    def get(username):
        if username in _user_table:
            return User(_user_table[username])
        else:
            return Exception('No user: "%s"' % (username))
    @staticmethod
    def add(args):
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

User.add({'username': 'james', 'firstname': 'James', 'lastname':'Curran', 'school': 'usyd', 'email':'god@it.usyd.edu.au'})

