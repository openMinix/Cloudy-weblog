from google.appengine.ext import db
import common_utils 
from cloudywebproject import *
from passlib.hash import sha256_crypt

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class BlogEntry(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    date = db.DateTimeProperty(auto_now_add = True)

    def render(self):
        return common_utils.render_template('blogentry.html', entry = self )


def user_key(group = 'default'):
    return db.Key.from_path('users',group)

class User(db.Model):
    username = db.StringProperty( required = True )
    password = db.StringProperty( required = True )
    email = db.StringProperty()

    @classmethod
    def get_by_name(cls, username):
        return cls.all().filter('username = ', username).get()
    
    @classmethod
    def register(cls, username, password, email = None):

        passwd_hash = sha256_crypt.encrypt(password) 

        return User( parent = user_key(), username = username,
                    password = passwd_hash, email = email)

    @classmethod
    def login (cls, username, password):
        user = cls.get_by_name(username)
        
        if user and sha256_crypt.verify(password, user.password):
                return user

    def render(self):
        pass
