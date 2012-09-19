import cloudywebproject 
import re

def render_template(template, **kwargs):
    """Renders the template with the given parameters """
    page_template = cloudywebproject.jinja_env.get_template(template)
    page_template = page_template.render(**kwargs)
    return page_template


EMAIL_RE = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain
      

class DataValidator(object):
    """ Validates user data """

    def validate_username(self, username):
        """ Validates username from user"""
        if username:
            return True

    def validate_email(self,email):
        """ Validates email format """
        return EMAIL_RE.match(email) 

    def validate_password(self, password):
        """ Validates password format """
        if password:
            return True

