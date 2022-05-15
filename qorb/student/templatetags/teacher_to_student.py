from django import template

register = template.Library()


@register.filter()
def teacher_to_student(value):
    return value.replace("teacher", "student")
