from google.appengine.ext import db
from common_utils import render_template
from cloudywebproject import *


def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)


class BlogEntry(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    date = db.DateTimeProperty(auto_now_add = True)

    def render(self):
        return render_template('blogentry.html', entry = self )


def user_key(group = 'default'):
    return db.Key.from_path('users',group)

class User(db.Model):
    username = db.StringProperty( required = True )
    password = db.StringProperty( required = True )
    email = db.StringProperty()

    def render(self):
        pass
