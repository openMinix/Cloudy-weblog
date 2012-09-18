import webapp2
import jinja2

import dbModels  
import common_utils 

from google.appengine.ext import db

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('./templates/'),
                               autoescape = True )


class BaseHandler(webapp2.RequestHandler):
    """ Base class for handlers"""
        
    def initialize(self, *args, **kwargs):
        webapp2.RequestHandler.initialize(self, *args, **kwargs)
        uid = self.get_cookie('user_id')
        if uid:
            self.user = dbModels.User.get_by_id( int(uid), parent = dbModels.user_key() )
        else:
            self.user = uid

    def render(self, template, **kwargs):
        kwargs['user'] = self.user

        page_template = jinja_env.get_template(template)
        page_template = page_template.render(**kwargs)
        self.response.out.write(page_template)
    
    def set_cookie(self, name, value):
        self.response.headers.add_header('Set-Cookie',
                                         '%s=%s; Path=/' % (name, value)
                                         )
    def get_cookie(self, name):
        cookie_value = self.request.cookies.get(name)
        return cookie_value

    def login(self, username):
        self.set_cookie('user_id', str(username.key().id()))

    def logout(self):
        self.set_cookie('user_id',"")



class MainPageHandler(BaseHandler):
    """ Handles the main page processing"""

    def get(self):
        self.render('mainpage.html')


class BlogHandler(BaseHandler):
    """Handles the blog page processing"""

    def get(self):
        entries = dbModels.BlogEntry.all().order('-date') 
        self.render('blog.html', entries = entries)


class NewEntryHandler(BaseHandler):
    """Handles the submit page processing"""

    def get(self):
        if self.user:
            self.render('newentry.html')
        else:
            self.redirect("/login")

    def post(self):
        
        title = self.request.get('title')
        content = self.request.get('content')
        
        if title and content:
            be = dbModels.BlogEntry(parent = dbModels.blog_key(), title = title, content = content)
            be.put()
            permalink = str( be.key().id() )
            self.redirect('/blog/' + permalink)
        else:
            self.render('newentry.html')
            

class EntryPageHandler(BaseHandler):
    """Handles the permalink pages processing"""
    
    def get(self, entry_id):
        key = db.Key.from_path('BlogEntry', int(entry_id), parent=dbModels.blog_key())
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
       
        invalid_data={} 
        dv = common_utils.DataValidator() 
        
        if not dv.validate_username(self.username):
            invalid_data["invalid_username"]="Sorry, not a valid username."

        if not dv.validate_password(self.password):
            invalid_data["invalid_passowrd"]="Sorry, not a valid password."
        elif self.password != self.verify:
            invalid_data["invalid_verify"] = "Passwords do not match!"
        
        if not dv.validate_email(self.email):
            invalid_data["invalid_email"] = "Sorry, not a valid e-mail address."

        user = dbModels.User.get_by_name(self.username)
        if user:
           invalid_data["invalid_username"]= "This username is already taken." 
         
        if len(invalid_data):
           self.render("signup.html", **invalid_data) 
        else:
        
            user = dbModels.User.register(self.username,
                                     self.password, self.email)
            user.put()

            self.login(user)
            self.redirect("/blog")


class LoginHandler(BaseHandler):
    """Handles the login page processing"""

    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        
        user = dbModels.User.login(username, password)
        if user:
            self.login(user)
            self.redirect('/blog')
        else:
            invalid_data = "No such username or wrong password. Your guess!"
            self.render("login.html", invalid_data = invalid_data)


class LogoutHandler(BaseHandler):
    """Handles the logout processing"""
      
    def get(self):
        self.logout()
        self.redirect('/blog')



app = webapp2.WSGIApplication( [('/', MainPageHandler),
                                ('/blog/?',BlogHandler),
                                ('/blog/newentry/?', NewEntryHandler),
                                ('/blog/([0-9]+)/?', EntryPageHandler),
                                ('/signup', SignupHandler),
                                ('/login' , LoginHandler),
                                ('/logout' , LogoutHandler)
                              ],
                              debug=True)


