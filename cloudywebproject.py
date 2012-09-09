import webapp2
import jinja2

from dbModels import BlogEntry 
from dbModels import blog_key
from common_utils import render_template

from google.appengine.ext import db

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('./templates/'),
                               autoescape = True )


class BaseHandler(webapp2.RequestHandler):
    """ Base class for handlers"""
        
    def render(self, template, **kwargs):
        page_template = jinja_env.get_template(template)
        page_template = page_template.render(**kwargs)
        self.response.out.write(page_template)


class MainPageHandler(BaseHandler):
    """ Handles the main page processing"""

    def get(self):
        self.render('mainpage.html')


class BlogHandler(BaseHandler):
    """Handles the blog page processing"""

    def get(self):
        entries = BlogEntry.all().order('-date') 
        self.render('blog.html', entries = entries)


class NewEntryHandler(BaseHandler):
    """Handles the submit page processing"""

    def get(self):
        self.render('newentry.html')

    def post(self):
        
        title = self.request.get('title')
        content = self.request.get('content')
        
        if title and content:
            be = BlogEntry(parent = blog_key(), title = title, content = content)
            be.put()
            permalink = str( be.key().id() )
            self.redirect('/blog/' + permalink)
        else:
            self.render('newentry.html')
            

class EntryPageHandler(BaseHandler):
    """Handles the permalink pages processing"""
    
    def get(self, entry_id):
        key = db.Key.from_path('BlogEntry', int(entry_id), parent=blog_key())
        entry = db.get(key)

        if entry:
            self.render('permalink.html', entry = entry)
        else:
            self.error(404)


class SignupHandler(BaseHandler):
    def get(self):
        self.render('signup.html')
    
    def post(self):
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')
        redirect('/signup')

app = webapp2.WSGIApplication( [('/', MainPageHandler),
                                ('/blog/?',BlogHandler),
                                ('/blog/newentry/?', NewEntryHandler),
                                ('/blog/([0-9]+)/?', EntryPageHandler),
                                ('/signup', SignupHandler)
                              ],
                              debug=True)


