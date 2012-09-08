from google.appengine.ext import db


def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)


class BlogEntry(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    
