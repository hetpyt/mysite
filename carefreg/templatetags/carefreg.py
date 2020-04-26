from django import template
from django.utils.html import mark_safe, format_html

register = template.Library()

class SideMenu(template.Node):
    def __init__(self, var_name, title = ''):
        self.var_name = var_name
        self.title = title

    def render(self, context):
        context[self.var_name] = [
            {'url' : 'carefreg:index', 'title' : 'Оказанные услуги'},
            {'url' : 'carefreg:services', 'title' : 'Услуги'},
            {'url' : 'carefreg:devices', 'title' : 'Устройства'},
            {'url' : 'carefreg:cartridges', 'title' : 'Картриджи'},
        ]
        context['menu_title'] = self.title
        return ''

@register.tag()
def get_side_menu(parser, token):
    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError("%r tag requires at least one argument - name of template variable" % token.contents.split()[0])
    var_name = args[1]
    menu_title = ''
    if len(args) > 2:
        menu_title = args[2]
    # try:
    #     #tag_name, var_name = token.split_contents()
    # except ValueError:
    #     raise template.TemplateSyntaxError("%r tag requires one argument - name of template variable" % token.contents.split()[0])
    return SideMenu(var_name, menu_title)
    
@register.inclusion_tag('carefreg/table_row.html')
def table_row(obj, fields_list):
    try:
        if isinstance(obj, dict):
            data = {field : obj[field] for field in fields_list}
        else:
            data = {field : getattr(obj, field) for field in fields_list}
    except:
        raise template.TemplateSyntaxError("not all fields of %r exists in given object %r" % (fields_list, obj))
    return {'table_row' : data}