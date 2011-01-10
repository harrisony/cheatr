from hashlib import sha1
import sqlite3
class User(object):
    @staticmethod
    def exists(username): 
        conn = sqlite3.connect('users.sqlite')
        cur = conn.cursor()
        q = cur.execute('SELECT 1 FROM users WHERE username=?',[username])
        if q.fetchone():
            return True
        else:
            return False
        cur.close()
        conn.close()
    @staticmethod
    def get(username):
        if User.exists(username):
            return User(username)
        else:
            return None
    @staticmethod
    def add(args):
        if 'username' not in args:
            raise Exception('No username provided')
        elif User.exists(args['username']):
            raise Exception('There is already a user called "%s"' % (args['username']))
        else:          
            q = User(args,nu=True)
            return True

    def __init__(self, inp,nu=False):
        if nu:
            print inp
            self._run_db("INSERT INTO users VALUES(?,?,?,?,?,?,?);", (inp['username'], sha1(inp['password']).hexdigest(), inp['firstname'], inp['lastname'], inp['email'], '', inp['school']))
        else:
            self._username = inp
            self._update_db(inp)
    def _run_db(self, command, variables):
        conn = sqlite3.connect('users.sqlite')
        c = conn.cursor()
        x = c.execute(command,variables)
        conn.commit()
        p = x.fetchall()
        c.close()
        conn.close()
        return p
    def _update_db(self,username):
        self._set_blank()
        x = self._run_db("SELECT * FROM users WHERE username = ?;", (username,))
        (self._username, self._passwordhash, self._firstname, self._lastname, self._email, self._profilepicpath, self._school) = x[0]
    def _set_blank(self):
        self._args = {}
        self._username = ''
        self._firstname = ''
        self._lastname = ''
        self._email = ''
        self._school = ''
        self._passwordhash = ''
        self._profilepath = ''
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
        return self._passwordhash
    def get_profile_pic_path(self):
        return self._profilepath
    def set_mutiple(self, args):
        mapping = {'firstname': self.set_first_name, 'lastname': self.set_last_name, 'email': self.set_email, 'school': self.set_school,
                   'password': self.set_password, 'profilepath': self.set_profile_pic_path}
        if 'username' in args: 
            args.pop('username')
        for k,v in args.items():
            func = mapping[k]
            func(v)
    def set_email(self, email):
        self._run_db("UPDATE users SET email = ?;", (email,))
        self._email = email
    def set_first_name(self, fname):
        self._run_db("UPDATE users SET firstname = ?;", (fname,))
        self._firstname = fname
    def set_last_name(self, lname):
        self._run_db("UPDATE users SET lastname = ?;", (lname,))
        self._lastname = lname
    def set_profile_pic_path(self, path):
        self.run_db("UPDATE users SET profilepath = ?;", (profilepath,))
        self._profile_pic_path = path
    def set_school(self, school):
        self._run_db("UPDATE users SET school = ?;", (school,))
        self._school = school
    def set_password(self, pword):
        self._run_db("UPDATE users SET 'passwordhash = ?;", (sha1(pword).hexdigest()),)
        self._passwordhash = sha1(pword).hexdigest()
    def password_correct(username, password):
        if sha1(password).hexdigest() == self.get_password_hash():
           return True
        else:
            return False