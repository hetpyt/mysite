from django import template
from django.utils.html import mark_safe, format_html

register = template.Library()

class SideMenu(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name
        
    def render(self, context):
        context[self.var_name] = [
            {'url' : 'carefreg:index', 'title' : 'Оказанные услуги'},
            {'url' : 'carefreg:services', 'title' : 'Услуги'},
#            {'url' : 'devices/', 'title' : 'Устройства'},
#            {'url' : 'cartridges/', 'title' : 'Картриджи'},
        ]
        return ''

@register.tag()
def get_side_menu(parser, token):
    try:
        tag_name, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires one argument - name of template variable" % token.contents.split()[0])
    return SideMenu(var_name)