from google.appengine.ext import db
import common_utils 
from cloudywebproject import *
from passlib.hash import sha256_crypt


class Group:
    pass


def group_key(group = 'default'):
    return db.Key.from_path('Group',group)


class User(db.Model):
    """Model for a user"""

    username = db.StringProperty( required = True )
    password = db.StringProperty( required = True )
    email = db.StringProperty()
    

    @classmethod
    def get_by_name(cls, username):
        """Returns the instance of User that matches the username"""
        return cls.all().filter('username = ', username).get()
    
    @classmethod
    def register(cls, username, password, email = None):
        """Returns new instance of User"""
        passwd_hash = sha256_crypt.encrypt(password) 

        return User( parent = group_key(), username = username,
                    password = passwd_hash, email = email)

    @classmethod
    def login (cls, username, password):
        """Verifies user credentials"""
        user = cls.get_by_name(username)
        
        if user and sha256_crypt.verify(password, user.password):
                return user

    def render(self):
        pass



class Blog(db.Model):
    """Model for a blog"""   
    
    blog_owner = db.ReferenceProperty(User, collection_name="blog",
                                     required = True) 
    blog_title = db.StringProperty(required = True)
    start_date = db.DateTimeProperty(auto_now_add = True)  

    def render():
        pass

    
def blog_key(name = 'default'):
    """Returns the key of the blog with the ID name"""
    return db.Key.from_path('Blog', name)


class BlogEntry(db.Model):
    """Model for a blog entry""" 

    blog = db.ReferenceProperty(Blog, collection_name="blog_entries")   
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    date = db.DateTimeProperty(auto_now_add = True)

    def render(self):
        return common_utils.render_template('blogentry.html', entry = self )
 
