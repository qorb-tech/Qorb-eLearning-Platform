from django import template

register = template.Library()


@register.filter()
def edit_report_grades_url(value):
    url_ = value.replace("media/course_report/", "teacher/report-grades-view/")
    r_str = url_[url_.rindex("/") :]
    url_ = url_.replace(r_str, "")
    return url_
