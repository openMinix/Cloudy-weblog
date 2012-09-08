import webapp2


class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Hello World!')


app = webapp2.WSGIApplication( [('/', MainPageHandler)]
                              ,
                              debug=True)


