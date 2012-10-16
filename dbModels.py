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
    def login(cls, username, password):
        """Verifies user credentials"""

        user = cls.get_by_name(username)
        
        if user and sha256_crypt.verify(password, user.password):
            return user

    def vote(self, blog_entry, vote_kind):
        """Mark the blog entry as voted by this user"""

        vote = BlogEntryVote( blog_entry = blog_entry,
                      user_voted = self, vote_kind = vote_kind)
        vote.put()

        
    def has_voted(self, blog_entry):
        """Verifies if the user has voted the blog entry
        blog_entry"""
         
        for vote in self.blogentries_votes:
            if blog_entry.key().id() == vote.blog_entry.key().id():
                return True 

        return False 
            


    def is_unvoting(self, blog_entry, sign):
        """Checks if the user wants to unvote"""

        vote = self.blogentries_votes. \
            filter('blog_entry =', blog_entry). \
            filter('user_voted =', self)[0]
        
        if sign == vote.vote_kind:
            return True
        else:
            return False
    
    def unvote(self, blog_entry):
        """Unvotes a voted post"""
         
        vote = self.blogentries_votes. \
            filter('blog_entry =', blog_entry). \
            filter('user_voted =', self)[0]
        
        if vote.vote_kind == "plus":
            blog_entry.votes -= 1
        elif vote.vote_kind == "minus":
            blog_entry.votes += 1
        else:
            pass
        
        blog_entry.put()
        vote.delete()  

    def is_changing_vote(self, blog_entry, sign):
        """Checks if user wants to change his vote"""
        vote = self.blogentries_votes. \
            filter('blog_entry =', blog_entry). \
            filter('user_voted =', self)[0]
        
        if sign != vote.vote_kind:
            return True
        else:
            return False

    def change_vote(self, blog_entry):
        """Unvotes a voted post"""
         
        vote = self.blogentries_votes. \
            filter('blog_entry =', blog_entry). \
            filter('user_voted =', self)[0]
        
        if vote.vote_kind == "plus":
            blog_entry.votes -= 2
            vote.vote_kind = "minus"
        elif vote.vote_kind == "minus":
            blog_entry.votes += 2
            vote.vote_kind = "plus"
        else:
            pass
       
        vote.put() 
        blog_entry.put()

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

    if name.isdigit():
        name = int(name)

    return db.Key.from_path('Blog', name)


class BlogEntry(db.Model):
    """Model for a blog entry""" 

    blog = db.ReferenceProperty(Blog, collection_name="blog_entries")   
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    date = db.DateTimeProperty(auto_now_add = True)
    votes = db.IntegerProperty( default = 0 )

    def render(self):
        return common_utils.render_template('blogentry.html', entry = self )
    
    
class BlogEntryVote(db.Model):
    """ Model for a blog entry vote"""

    blog_entry = db.ReferenceProperty(BlogEntry, collection_name="blogentries_votes")
    user_voted = db.ReferenceProperty(User, collection_name="blogentries_votes")
    vote_kind = db.StringProperty()
   
    
