import webapp2
import jinja2

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('./templates/') )


class MainPageHandler(webapp2.RequestHandler):
    """ Handles the main page proccesing"""

    def get(self):
        
        mainPage = jinja_env.get_template("mainpage.html")
        self.response.out.write(mainPage.render())


class BlogHandler(webapp2.RequestHandler):
    """Handles the blog page proccesing"""

    def get(self):
        blogPage = jinja_env.get_template("blog.html")
        self.response.out.write(blogPage.render())

  
  
app = webapp2.WSGIApplication( [('/', MainPageHandler),
                                ('/blog/?',BlogHandler),
                              ]
                              ,
                              debug=True)


