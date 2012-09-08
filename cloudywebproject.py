import webapp2
import jinja2
from dbModels import BlogEntry 
from dbModels import blog_key
from google.appengine.ext import db
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('./templates/'),
                               autoescape = True )


class MainPageHandler(webapp2.RequestHandler):
    """ Handles the main page processing"""

    def get(self):
        
        mainPage = jinja_env.get_template("mainpage.html")
        self.response.out.write(mainPage.render())


class BlogHandler(webapp2.RequestHandler):
    """Handles the blog page processing"""

    def get(self):
        blogPage = jinja_env.get_template("blog.html")
        self.response.out.write(blogPage.render())

  
class NewEntryHandler(webapp2.RequestHandler):
    """Handles the submit page processing"""

    def get(self):
        submitPage = jinja_env.get_template('newentry.html')
        self.response.out.write(submitPage.render())

    def post(self):
        
        title = self.request.get('title')
        content = self.request.get('content')
        
        if title and content:
            be = BlogEntry(parent = blog_key(), title = title, content = content)
            be.put()
            permalink = str( be.key().id() )
            self.redirect('/blog/' + permalink)
        else:
            self.response.out.write(submitPage.render())
            

class EntryPageHandler(webapp2.RequestHandler):
    """Handles the permalink pages processing"""
    
    def get(self, entry_id):
        key = db.Key.from_path('BlogEntry', int(entry_id), parent=blog_key())
        entry = db.get(key)

        if entry:
            permalingPage =jinja_env.get_template('permalink.html') 
            self.response.out.write(permalingPage.render(entry = entry))
        else:
            self.error(404)


app = webapp2.WSGIApplication( [('/', MainPageHandler),
                                ('/blog/?',BlogHandler),
                                ('/blog/newentry/?', NewEntryHandler),
                                ('/blog/([0-9]+)/?', EntryPageHandler)
                              ]
                              ,
                              debug=True)


