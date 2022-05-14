def student_directory_path(inst, file_name):
    return f'student_profile_images/{inst.user}/{file_name}'


def teacher_directory_path(inst, file_name):
    return f'teacher_profile_images/{inst.user}/{file_name}'
