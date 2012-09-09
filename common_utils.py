from cloudywebproject import *
import cloudywebproject 


def render_template(template, **kwargs):
    """Renders, the template with the given parameters """
    page_template = cloudywebproject.jinja_env.get_template(template)
    page_template = page_template.render(**kwargs)
    return page_template



