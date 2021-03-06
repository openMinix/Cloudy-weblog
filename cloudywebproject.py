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
            self.user = dbModels.User.get_by_id( int(uid),
                                           parent = dbModels.group_key() )
        else:
            self.user = uid

    def render(self, template, **kwargs):
        """Writes to the response the formatted webpage"""
        kwargs['user'] = self.user

        
        page_template = jinja_env.get_template(template)
        page_template = page_template.render(**kwargs)
        self.response.out.write(page_template)
    
    def set_cookie(self, name, value):
        """Sets a cookie with the name 'name' and the value 'value'"""

        self.response.headers.add_header('Set-Cookie',
                                         '%s=%s; Path=/' % (name, value)
                                         )
    def get_cookie(self, name):
        """Gets the cookie with the name 'name'""" 

        cookie_value = self.request.cookies.get(name)
        return cookie_value

    def login(self, username):
        """Sets the 'user_id' cookie"""
        self.set_cookie('user_id', str(username.key().id()))

    def logout(self):
        """Removes the 'user_id" cookie"""
        self.set_cookie('user_id',"")



class MainPageHandler(BaseHandler):
    """ Handles the main page processing"""

    def get(self):
        self.render("newmainpage.html")

class MainBlogHandler(BaseHandler):
    """ Handles blog main page """

    def get(self):
        entries = dbModels.BlogEntry.all().order('-votes').order('-date')

        if self.user:
           blog_id = str( self.user.blog[0].key().id() )
        else:
           blog_id = None

        self.render("blogmain.html", entries = entries, blog_id = blog_id)
     

class BlogHandler(BaseHandler):
    """Handles the blog page processing"""

    def get(self, blog_id="default"):

        b_key = dbModels.blog_key(blog_id)
        blog = db.get(b_key)

        entries =  ( dbModels.BlogEntry.all().filter('blog = ', blog).  
            order('-votes').order('-date') )

        self.render('blog.html', entries = entries, blog_id = blog_id,
            blog = blog)


class NewEntryHandler(BaseHandler):
    """Handles the submit page processing"""

    def get(self, blog_id):
        if self.user:
            self.render('newentry.html')
        else:
            self.redirect("/login")

    def post(self,blog_id):
        
        title = self.request.get('title')
        content = self.request.get('content')
        
        if title and content:
            b_key = dbModels.blog_key( blog_id)
            blog = db.get(b_key)

            be = dbModels.BlogEntry(parent = dbModels.blog_key(),
                title = title, content = content, blog = blog)
            be.put()

            permalink = str( be.key().id() )
            self.redirect('/blog/page' + blog_id +'/' + permalink)
        else:
            self.render('newentry.html')
            

class EntryPageHandler(BaseHandler):
    """Handles the permalink pages processing"""
    
    def get(self,blog_id, entry_id):
        key = db.Key.from_path('BlogEntry', int(entry_id), parent=dbModels.blog_key())
        entry = db.get(key)

        if entry:
            self.render('permalink.html', entry = entry, blog_id = blog_id)
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
        
        if self.email and not dv.validate_email(self.email):
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

            blog = dbModels.Blog( blog_owner = user , blog_title ='Def title',)
            blog.put()
            blog_page = str( blog.key().id() )
                 
            self.login(user)

            self.redirect('/blog/page' + blog_page)


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
            blog_page = str(user.blog.get().key().id()) 
            self.redirect('/blog/page' + blog_page)
        else:
            invalid_data = "No such username or wrong password. Your guess!"
            self.render("login.html", invalid_data = invalid_data)


class LogoutHandler(BaseHandler):
    """Handles the logout processing"""
      
    def get(self):
        self.logout()
        self.redirect('/blog')


class VoteHandler(BaseHandler):
   """Handles the blogEntry posts voting"""

   def get(self):
       votes = self.request.get("votes")
       sign = self.request.get("sign")
       entry_id = self.request.get("entry")

       blog_entry = dbModels.BlogEntry.get_by_id( int(entry_id),
                                           parent = dbModels.blog_key() )

       if (not self.user) or self.user.has_voted(blog_entry):
           if self.user.is_unvoting(blog_entry, sign):
               self.user.unvote(blog_entry)
               self.response.out.write( str(blog_entry.votes))
           elif self.user.is_changing_vote(blog_entry, sign):
               self.user.change_vote(blog_entry)
               self.response.out.write( str(blog_entry.votes))
           else:
               self.response.out.write( str(votes) )

           return
       else:
           self.user.vote(blog_entry, sign)
           

       if sign == "plus":
           votes =int(votes) + 1
       elif sign == "minus":
           votes = int(votes) - 1
       else:
           pass

       blog_entry.votes = votes;
       blog_entry.put(); 

       self.response.out.write( str(votes) )



app = webapp2.WSGIApplication( [('/', MainPageHandler),
                                ('/blog/?',MainBlogHandler),
                                ('/blog/page([0-9]+)/?', BlogHandler),
                                ('/blog/newentry/?', NewEntryHandler),
                                ('/blog/page([0-9]+)/newentry/?', NewEntryHandler),
                                ('/blog/page([0-9]+)/([0-9]+)/?', EntryPageHandler),
                                ('/signup', SignupHandler),
                                ('/login' , LoginHandler),
                                ('/logout' , LogoutHandler),
                                ('/blog/votes.*', VoteHandler)
                              ],
                              debug=True)


