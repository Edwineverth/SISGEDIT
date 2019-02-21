from django import template
from registropersonal.sistema.models import Actividad
register = template.Library()


@register.simple_tag
def ActividadCount():
    return Actividad.objects.count()

@register.tag(name='counter')
def do_counter(parser, token):
    """ 
    Counter tag. Can be used to output and increment a counter.

    Usage:
    - {% counter %} to output and post-increment the counter variable
    - {% counter reset %} to reset the counter variable to 1
    - {{ counter_var %} to access the last counter variable without incrementing

    """
    try:
        tag_name, reset = token.contents.split(None, 1)
    except ValueError:
        reset = False
    else:
        if reset == 'reset':
            reset = True
    return CounterNode(reset)


class CounterNode(template.Node):
    def __init__(self, reset):
        self.reset = reset

    def render(self, context):
        # When initializing or resetting, set counter variable in render_context to 1.
        if self.reset or ('counter' not in context.render_context):
            context.render_context['counter'] = 1

        # Set the counter_var context variable
        context['counter_var'] = context.render_context['counter']

        # When resetting, we don't want to return anything
        if self.reset:
            return ''

        # Increment counter. This does not affect the return value!
        context.render_context['counter'] += 1
        numero = int(context['counter_var'])
        # Return counter number
        return ""
