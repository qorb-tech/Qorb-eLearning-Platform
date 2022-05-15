def course_directory_path(inst, file_name):
    return f"course_images/{inst.name}/{file_name}"


def subject_directory_path(inst, file_name):
    return f"course_matrial/{inst.course}/{inst.description}/{file_name}"


def report_directory_path(inst, file_name):
    return f"course_report/{inst.course}/{inst.description_report}/{file_name}"


def students_report_directory_path(inst, file_name):
    return f"student_report/{inst.student}/{inst.report}/{file_name}"
