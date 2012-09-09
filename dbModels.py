from google.appengine.ext import db
from common_utils import render_template
from cloudywebproject import *


def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)


class BlogEntry(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)

    def render(self):
        return render_template('blogentry.html', entry = self )
    
