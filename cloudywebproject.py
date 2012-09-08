import webapp2
import jinja2

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('./templates/') )
class MainPageHandler(webapp2.RequestHandler):
    """ Handles the main page proccesing"""

    def get(self):
        
        mainPage = jinja_env.get_template("mainpage.html")
        self.response.out.write(mainPage.render())


app = webapp2.WSGIApplication( [('/', MainPageHandler)]
                              ,
                              debug=True)


